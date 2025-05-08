import subprocess
import random
import platform
import re
import os
import sys
import ctypes

if platform.system().lower() == "windows":
    import winreg

def is_windows():
    return platform.system().lower() == "windows"

def check_admin():
    if is_windows():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0

def generate_valid_mac():
    first_byte = random.randint(0x00, 0xFE) & 0xFE
    return ":".join(f"{random.randint(0x00, 0xFF):02x}" for _ in range(6)).upper()

def run_command(command, shell=False):
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
        print(f"❌ Fout: {e.stderr}")
        return None

def get_adapters():
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
                                try:
                                    mac = winreg.QueryValueEx(subkey, "NetworkAddress")[0]
                                except FileNotFoundError:
                                    mac = "Geen MAC geregistreerd"
                                adapters.append((name, subkey_name, mac))
                            except FileNotFoundError:
                                continue
        except Exception as e:
            print(f"❌ Windows fout: {e}")
    else:
        try:
            output = run_command(["ip", "-o", "link", "show"])
            if output:
                for line in output.splitlines():
                    if "loopback" not in line:
                        match = re.search(r"\d+: ([^:]+):.*link/ether ([\da-fA-F:]+)", line)
                        if match:
                            adapters.append((match.group(1), match.group(2)))
        except Exception as e:
            print(f"❌ Linux fout: {e}")
    return adapters

def change_mac(interface, new_mac):
    if is_windows():
        try:
            key_path = fr"SYSTEM\CurrentControlSet\Control\Class\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\{interface}"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, new_mac.replace(':', ''))
                run_command(["powershell", "Restart-NetAdapter", "-Name", interface], shell=True)
                return True
        except Exception as e:
            print(f"❌ Windows fout: {e}")
            return False
    else:
        try:
            run_command(["ip", "link", "set", "dev", interface, "down"])
            run_command(["ip", "link", "set", "dev", interface, "address", new_mac])
            run_command(["ip", "link", "set", "dev", interface, "up"])
            return True
        except Exception as e:
            print(f"❌ Linux fout: {e}")
            return False

def interactive_mode():
    """Interactieve modus met terugkeeroptie"""
    if not check_admin():
        print("⚠️ Draai dit script als administrator/sudo!")
        return

    adapters = get_adapters()
    if not adapters:
        print("❌ Geen interfaces gevonden")
        return

    print("\nBeschikbare netwerkinterfaces:")
    for idx, adapter in enumerate(adapters):
        if is_windows():
            name, subkey, mac = adapter
            print(f"[{idx}] {name} - Huidig MAC: {mac}")
        else:
            name, mac = adapter
            print(f"[{idx}] {name} - Huidig MAC: {mac}")
    
    print("\n[99] Terug naar hoofdmenu")

    try:
        user_input = input("\nKies een interface nummer (of 99 om terug te keren): ")
        if user_input == "99":
            return
        
        choice = int(user_input)
        if choice < 0 or choice >= len(adapters):
            print("❌ Ongeldige keuze")
            return
    except ValueError:
        print("❌ Voer een geldig nummer in")
        return

    interface = adapters[choice][1] if is_windows() else adapters[choice][0]
    
    new_mac = input("Voer MAC-adres in (leeg voor willekeurig): ").strip()
    if not new_mac:
        new_mac = generate_valid_mac()
        print(f"Generated MAC: {new_mac}")

    if not re.match(r"^([0-9A-F]{2}:){5}[0-9A-F]{2}$", new_mac, re.IGNORECASE):
        print("❌ Ongeldig MAC-formaat")
        return

    if change_mac(interface, new_mac):
        print(f"✅ MAC succesvol gewijzigd naar {new_mac}")
    else:
        print("❌ Wijzigen mislukt")

if __name__ == "__main__":
    interactive_mode()
