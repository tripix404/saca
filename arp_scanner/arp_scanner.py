import datetime
import socket
import base64
import json
from scapy.all import ARP, Ether, srp, get_working_ifaces
import paramiko
from pathlib import path
import platform

def sace_results(data, filename="scan_results"):
    """ opslagen van resultaten in een JSON-bestand """"

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = base64.b64encode(f"{filename}_{timestamp}".encode()).decode()
    path = path(f"./{safe_name}.json")
    with open(path, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "data": data
        }, f, indent=2)
    print(f"[+] resultaten opgeslagen in {path.name}")

def arp_scan(target_ip="192.168.1.0/24"):
    """scant het netwerk voor actieve devices met Scapy"""
    print("[+]  ARP-scan uitvoeren...")

    # Toon alle beschikbare interfaces
    available_ifaces = [iface.name for iface in get_working_ifaces()]
    print(f" [+] Beschikbare interfaces:")
    for idx, iface in enumerate(available_ifaces):
        print(f"    {idx}: {iface}")
    
    # vraag gebruiker om een interface te kiezen
    while true:
        try:
            iface_idx = int(input(f"Kies het nummer om een interface te kiezen (0-{len(available_ifaces)-1}): "))
            iface = available_ifaces[iface_idx]
            break
        except (ValueError, IndexError):
            print("Ongeldige keuze, kies opnieuw;")
        
    print(f"[+] Gekozen interfqce: {iface}")
    print(f"[+] Gekozen IP adres: {target_ip}")

    try:
        arp = ARP(pdst=target_ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp
        print("[DEBUG] ARP-pakket wordt verstuurd...")
        result = srp(packet, iface=iface, timeout=5, verbose=False)[0]

        devices = []
        for sent, received in result:
            devices.append({'IP' : received.psrc, 'MAC' : received.hwsrc})

        if not devices:
            print("[!] Geen apparaten gevonden. Mogelijke oorzaken:")
            print("- Verkeerde interface gekozen")
            print("- Gekozen IP netwerk komt niet overeen met eigen subnet")
            print("- Firewall blokkeert ARP-verkeer")
        else:
            print(f"[+] {len(devices)} apparaten gevonden.")
    
        return devices
    except Exception as e:
        print(f"[-] Kritieke fout tijdens ARP-scan: {str(e)}")
        print("[+] Voer het script uit als Administrator en of controleer je firewall instellingen")
        return []
        