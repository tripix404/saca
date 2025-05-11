import subprocess
import random
import platform
import re
import os
import sys
import ctypes
import time
from typing import List, Tuple

if platform.system().lower() == "windows":
    import winreg

def is_windows() -> bool:
    """
    Controleer of het script op een Windows-systeem draait.

    Returns:
        bool: True als het systeem Windows is, anders False.
    """
    return platform.system().lower() == "windows"

def check_admin() -> bool:
    '''
    Controleer of het script met administratorrechten draait.'''
    if is_windows():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0

def generate_valid_mac() -> str:
    '''
    Genereer een willekeurige, geldige MAC-adres.'''
    first_byte = random.randint(0x02, 0xFE) | 0b00000010  # Lokaal beheerd
    return ":".join(
        [f"{first_byte:02X}"] + 
        [f"{random.randint(0x00, 0xFF):02X}" for _ in range(5)]
    )

def run_command(command: list, shell: bool = False) -> str:
    '''
    Voer een shell-opdracht uit en retourneer de uitvoer.'''
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            shell=shell,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return ""

def get_adapters() -> List[Tuple[str, str, str, str]]:
    '''
    Verkrijg een lijst van netwerkadapters en hun details.'''
    adapters = []
    if is_windows():
        try:
            key_path = r"SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as root_key:
                for i in range(winreg.QueryInfoKey(root_key)[0]):
                    subkey_name = winreg.EnumKey(root_key, i)
                    if subkey_name.isdigit():
                        with winreg.OpenKey(root_key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, "DriverDesc")[0]
                                component_id = winreg.QueryValueEx(subkey, "ComponentId")[0].lower()
                                guid = winreg.QueryValueEx(subkey, "NetCfgInstanceId")[0]
                                
                                if any(s in component_id for s in ["tap", "virtual", "vmxnet", "vpn", "wan"]):
                                    continue
                                
                                try:
                                    mac = winreg.QueryValueEx(subkey, "NetworkAddress")[0]
                                except FileNotFoundError:
                                    mac = "Geen MAC geregistreerd"
                                
                                adapters.append((name, subkey_name, guid, mac))
                            except FileNotFoundError:
                                continue
        except Exception as e:
            print(f"❌ Registry fout: {str(e)}")
    return adapters

def verify_mac_change(guid: str, expected_mac: str) -> bool:
    '''
    Controleer of de MAC-adreswijziging succesvol was.'''
    try:
        key_path = fr"SYSTEM\CurrentControlSet\Control\Class\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\{guid}"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            current_mac = winreg.QueryValueEx(key, "NetworkAddress")[0]
            return current_mac.replace(':', '').upper() == expected_mac.replace(':', '').upper()
    except:
        return False

def change_mac(interface_key: str, new_mac: str, guid: str) -> bool:
    '''
    Wijzig de MAC-adres van de opgegeven netwerkadapter.'''
    try:
        # Schrijf MAC naar registry
        key_path = fr"SYSTEM\CurrentControlSet\Control\Class\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\{interface_key}"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, new_mac.replace(':', ''))
        
        # Herstart adapter via GUID (meer betrouwbaar dan naam)
        ps_commands = [
            f'Disable-NetAdapter -InterfaceGuid "{guid}" -Confirm:$false',
            f'Enable-NetAdapter -InterfaceGuid "{guid}"'
        ]
        
        for cmd in ps_commands:
            result = run_command(["powershell", "-Command", cmd])
            if "No MSFT_NetAdapter" in result:
                run_command(f'netsh interface set interface "{guid}" admin=disable', shell=True)
                time.sleep(1)
                run_command(f'netsh interface set interface "{guid}" admin=enable', shell=True)
                break
        
        # Verifieer wijziging
        time.sleep(3)
        return verify_mac_change(interface_key, new_mac)
        
    except Exception as e:
        print(f"❌ Kritieke fout: {str(e)}")
        return False

def interactive_mode():
    if not check_admin():
        print("⚠️ Draai als administrator!")
        return

    adapters = get_adapters()
    if not adapters:
        print("❌ Geen compatibele adapters gevonden")
        return

    print("\nBeschikbare netwerkinterfaces:")
    for idx, (name, _, _, mac) in enumerate(adapters):
        print(f"[{idx}] {name.ljust(40)} - Huidig MAC: {mac}")
    
    print("\n[99] Afsluiten")

    try:
        choice = input("\nKeuze: ").strip()
        if choice == "99":
            return
        
        choice_idx = int(choice)
        selected = adapters[choice_idx]
    except:
        print("❌ Ongeldige invoer")
        return

    new_mac = input("Voer MAC in (leeg = willekeurig): ").strip()
    if not new_mac:
        new_mac = generate_valid_mac()
        print(f"Gegenereerde MAC: {new_mac}")
    elif not re.match(r"^([0-9A-F]{2}:){5}[0-9A-F]{2}$", new_mac, re.I):
        print("❌ Ongeldig formaat!")
        return

    if change_mac(selected[1], new_mac, selected[2]):
        print(f"\n✅ Succes! Nieuwe MAC: {new_mac}")
        print("⚠️ Mogelijk moet je de netwerkverbinding handmatig herstarten")
    else:
        print("\n❌ Wijziging mislukt - Controleer administratorrechten")

if __name__ == "__main__":
    interactive_mode()
