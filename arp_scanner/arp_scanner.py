import datetime
import socket
import base64
import json
from scapy.all import ARP, Ether, srp, get_working_ifaces
import paramiko
from pathlib import path
import platform

def sace_results(data, filename="scan_results"):

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = base64.b64encode(f"{filename}_{timestamp}".encode()).decode()
    path = path(f"./{safe_name}.json")
    with open(path, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "data": data
        }, f, indent=2)
    print(f"[+] resultaten opgeslagen in {path.name}")

