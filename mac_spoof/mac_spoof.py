import subprocess
import random
import platform
import argparse
import re
import os
import sys
import ctypes
import time

def is_windows():
    """Detecteer of het systeem Windows is"""
    return platform.system().lower() == "windows"

def check_admin():
    """Controleer of het script met verhoogde rechten wordt uitgevoerd"""
    if is_windows():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0

def generate_mac():
    """Genereer een willekeurig MAC-adres"""
    mac = [random.randint(0, 255) for _ in range(6)]
    # Zorg ervoor dat het eerste octet even is (universeel/lokaal bit)
    mac[0] &= 0xfe
    return ":".join(f"{x:02x}" for x in mac)

def run_command(command, error_message="Fout bij uitvoeren commando"):
    """Voer een shell commando uit met foutafhandeling"""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {error_message}: {e.stderr}")
        return None
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        return None

def get_current_mac_linux(interface):
    """Haal het huidige MAC-adres op Linux op"""
    try:
        output = run_command(["ip", "link", "show", interface], 
                            f"Kan informatie van interface {interface} niet ophalen")
        if output:
            mac_search = re.search(r'link/ether ([0-9a-f:]{17})', output)
            return mac_search.group(1) if mac_search else None
        return None
    except Exception as e:
        print(f"❌ Fout bij het ophalen van het MAC-adres: {e}")
        return None

def get_current_mac_windows(adapter_name):
    """Haal het huidige MAC-adres op Windows op"""
    try:
        # Gebruik wmic voor actieve netwerkadapters
        output = run_command(["wmic", "nic", "where", "NetEnabled=true", "get", "Name,MACAddress"],
                           "Kan MAC-adressen niet ophalen")
        
        if not output:
            return None
            
        lines = output.strip().split('\n')
        
        for line in lines[1:]:  # Skip header
            if adapter_name in line:
                # Zoek het MAC-adres in de output
                mac_match = re.search(r'([0-9A-F]{2}[:-][0-9A-F]{2}[:-][0-9A-F]{2}[:-][0-9A-F]{2}[:-][0-9A-F]{2}[:-][0-9A-F]{2})', line)
                if mac_match:
                    # Normaliseer naar formaat met dubbele punten
                    return mac_match.group(1).replace('-', ':')
        
        # Als niet gevonden via actieve adapters, probeer alle adapters
        output = run_command(["getmac", "/v", "/fo", "csv"], 
                           "Kan MAC-adressen niet ophalen via getmac")
        
        if output:
            for line in output.splitlines():
                if adapter_name in line:
                    mac_match = re.search(r'([0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2})', line)
                    if mac_match:
                        return mac_match.group(1).replace('-', ':')
        
        return None
    except Exception as e:
        print(f"❌ Fout bij het ophalen van het MAC-adres: {e}")
        return None

def change_mac_linux(interface, new_mac):
    """Wijzig MAC-adres op Linux"""
    try:
        if run_command(["sudo", "ip", "link", "set", "dev", interface, "down"],
                      f"Kan interface {interface} niet uitschakelen") is None:
            return False
            
        if run_command(["sudo", "ip", "link", "set", "dev", interface, "address", new_mac],
                      f"Kan MAC-adres niet wijzigen") is None:
            # Probeer de interface weer in te schakelen voordat we false teruggeven
            run_command(["sudo", "ip", "link", "set", "dev", interface, "up"],
                       f"Kan interface {interface} niet inschakelen")
            return False
            
        if run_command(["sudo", "ip", "link", "set", "dev", interface, "up"],
                      f"Kan interface {interface} niet inschakelen") is None:
            return False
            
        return True
    except Exception as e:
        print(f"❌ Fout bij het wijzigen van MAC-adres: {e}")
        return False

def get_adapter_index_windows(adapter_name):
    """Haal de adapter index op via verschillende methodes"""
    # Methode 1: via naam
    try:
        output = run_command(["wmic", "nic", "where", f"Name='{adapter_name}'", "get", "InterfaceIndex"],
                           f"Kan index van adapter {adapter_name} niet vinden")
        
        if output:
            index_match = re.search(r'(\d+)', output.strip())
            if index_match:
                return index_match.group(1)
    except:
        pass
    
    # Methode 2: via MAC-adres
    try:
        current_mac = get_current_mac_windows(adapter_name)
        if current_mac:
            # Formatteer MAC-adres terug naar Windows formaat met streepjes
            current_mac_win = current_mac.replace(':', '-').upper()
            output = run_command(["wmic", "nic", "where", f"MACAddress='{current_mac_win}'", "get", "InterfaceIndex"],
                               f"Kan index via MAC-adres niet vinden")
            
            if output:
                index_match = re.search(r'(\d+)', output.strip())
                if index_match:
                    return index_match.group(1)
    except:
        pass
    
    # Methode 3: lijst alle adapters en laat gebruiker kiezen
    try:
        output = run_command(["wmic", "nic", "get", "Name,InterfaceIndex"],
                           "Kan adapter lijst niet ophalen")
        
        if output:
            print("\n⚠️ Kan adapter index niet automatisch vinden. Selecteer handmatig:")
            
            lines = output.strip().split('\n')
            valid_indices = []
            
            for i, line in enumerate(lines[1:], 1):  # Skip header
                index_match = re.search(r'(\d+)', line)
                if index_match and adapter_name in line:
                    index = index_match.group(1)
                    print(f"  {i}: Index {index} - {line.strip()}")
                    valid_indices.append(index)
            
            if valid_indices:
                choice = get_user_choice(1, len(valid_indices))
                return valid_indices[choice - 1]
    except:
        pass
    
    return None

def change_mac_windows(adapter_name, new_mac):
    """Wijzig MAC-adres op Windows met netsh en registry"""
    try:
        # Haal interface-index op
        interface_index = get_adapter_index_windows(adapter_name)
        
        if not interface_index:
            print(f"❌ Kan interface-index niet vinden voor {adapter_name}")
            return False
        
        # Probeer eerst met netsh
        print(f"🔄 Uitschakelen van interface {adapter_name}...")
        
        try:
            # Schakel interface uit met netsh
            run_command(["netsh", "interface", "set", "interface", adapter_name, "admin=disable"],
                       f"Kan interface {adapter_name} niet uitschakelen")
            
            # Bereid MAC-adres voor (verwijder scheidingstekens voor Windows)
            new_mac_no_colons = new_mac.replace(':', '')
            
            # Probeer MAC-adres te wijzigen via registry
            registry_path = f"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\{int(interface_index):04d}"
            run_command(["reg", "add", registry_path, "/v", "NetworkAddress", "/d", new_mac_no_colons, "/f"],
                       "Kan MAC-adres niet instellen in registry")
            
            # Schakel interface weer in
            print(f"🔄 Inschakelen van interface {adapter_name}...")
            run_command(["netsh", "interface", "set", "interface", adapter_name, "admin=enable"],
                       f"Kan interface {adapter_name} niet inschakelen")
            
            # Wacht even zodat de wijziging effect heeft
            time.sleep(3)
            
            return True
        except Exception as e:
            print(f"⚠️ Netsh methode gefaald: {e}")
            print("⚠️ Fallback naar alternatieve methode...")
            
            # Fallback naar wmic methode
            run_command(["wmic", "path", "win32_networkadapter", "where", f"index={interface_index}", "call", "disable"],
                       f"Kan interface niet uitschakelen")
            
            # Bereid MAC-adres voor
            new_mac_no_colons = new_mac.replace(':', '')
            
            # Wijzig het MAC-adres via registry
            registry_path = f"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\{int(interface_index):04d}"
            run_command(["reg", "add", registry_path, "/v", "NetworkAddress", "/d", new_mac_no_colons, "/f"],
                       "Kan MAC-adres niet instellen in registry")
            
            # Schakel adapter weer in
            run_command(["wmic", "path", "win32_networkadapter", "where", f"index={interface_index}", "call", "enable"],
                       f"Kan interface niet inschakelen")
            
            # Wacht even zodat de wijziging effect heeft
            time.sleep(3)
            
            return True
    except Exception as e:
        print(f"❌ Fout bij het wijzigen van MAC-adres: {e}")
        return False

def verify_mac_change(interface, new_mac, is_win=False):
    """Verifieer of het MAC-adres succesvol is gewijzigd"""
    # Wacht even zodat de wijziging effect heeft
    time.sleep(3)
    
    if is_win:
        current_mac = get_current_mac_windows(interface)
    else:
        current_mac = get_current_mac_linux(interface)
    
    if current_mac:
        # Normaliseer MAC-adres formaat voor vergelijking
        current_mac = current_mac.lower()
        new_mac = new_mac.lower()
        
        if current_mac == new_mac:
            print(f"✅ MAC-adres is succesvol gewijzigd naar {new_mac}")
            return True
        else:
            print(f"⚠️ MAC-adres wijzigen mislukt. Huidig MAC: {current_mac}")
            return False
    else:
        print("⚠️ Kan het huidige MAC-adres niet ophalen voor verificatie")
        return False

def get_available_interfaces():
    """Haal beschikbare netwerkinterfaces op, afhankelijk van het besturingssysteem"""
    interfaces = []
    
    if is_windows():
        # Gebruik wmic voor betrouwbaardere resultaten
        try:
            output = run_command(["wmic", "nic", "where", "NetEnabled=true", "get", "Name,MACAddress"],
                               "Kan actieve netwerkadapters niet ophalen")
            
            if output:
                lines = output.strip().split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        mac_match = re.search(r'([0-9A-F]{2}[:-][0-9A-F]{2}[:-][0-9A-F]{2}[:-][0-9A-F]{2}[:-][0-9A-F]{2}[:-][0-9A-F]{2})', line)
                        if mac_match:
                            mac = mac_match.group(1)
                            name = line.replace(mac, '').strip()
                            interfaces.append((name, name))
        except Exception as e:
            print(f"⚠️ Fout bij ophalen interfaces: {e}")
    else:  # Linux
        try:
            output = run_command(["ip", "link", "show"], "Kan netwerkinterfaces niet ophalen")
            
            if output:
                lines = output.strip().split('\n')
                for i in range(0, len(lines), 2):
                    if i < len(lines):
                        match = re.search(r'^\d+: ([^:@]+)', lines[i])
                        if match and not match.group(1).startswith('lo'):
                            interfaces.append((match.group(1), match.group(1)))
        except Exception as e:
            print(f"⚠️ Fout bij ophalen interfaces: {e}")
    
    return interfaces

def get_user_choice(min_val, max_val, prompt="Kies een optie"):
    """Vraag om gebruikersinvoer met validatie"""
    while True:
        try:
            choice = int(input(f"\n{prompt} ({min_val}-{max_val}): "))
            if min_val <= choice <= max_val:
                return choice
            print(f"❌ Kies een nummer tussen {min_val} en {max_val}")
        except ValueError:
            print("❌ Voer een geldig nummer in")
        except KeyboardInterrupt:
            print("\n⚠️ Operatie geannuleerd door gebruiker")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Cross-platform MAC-adres wijziger')
    parser.add_argument('-i', '--interface', help='Netwerkinterface om te wijzigen')
    parser.add_argument('-m', '--mac', help='Nieuw MAC-adres (willekeurig indien niet opgegeven)')
    parser.add_argument('-l', '--list', action='store_true', help='Toon beschikbare interfaces')
    args = parser.parse_args()
    
    is_win = is_windows()
    os_name = "Windows" if is_win else "Linux"
    
    print(f"🖥️ Besturingssysteem gedetecteerd: {os_name}")
    
    # Controleer admin/root rechten
    if not check_admin():
        print(f"⚠️ Dit script vereist {'administratorrechten' if is_win else 'root-rechten'}!")
        print(f"Start het script opnieuw met {'Run as administrator' if is_win else 'sudo'}")
        sys.exit(1)
    
    if args.list:
        print("Beschikbare netwerkinterfaces:")
        interfaces = get_available_interfaces()
        for idx, (id, name) in enumerate(interfaces, 1):
            print(f"[{idx}] {name}")
        return
    
    # Als geen interface opgegeven, toon beschikbare interfaces en vraag om keuze
    if not args.interface:
        print("Beschikbare netwerkinterfaces:")
        interfaces = get_available_interfaces()
        
        if not interfaces:
            print("❌ Geen actieve netwerkinterfaces gevonden")
            sys.exit(1)
            
        for idx, (id, name) in enumerate(interfaces, 1):
            print(f"[{idx}] {name}")
        
        choice = get_user_choice(1, len(interfaces))
        interface_id, interface_name = interfaces[choice - 1]
    else:
        # Als interface wel opgegeven, gebruik die
        interface_id = args.interface
        interface_name = args.interface
    
    # Genereer nieuw MAC-adres als niet opgegeven
    new_mac = args.mac if args.mac else generate_mac()
    
    print(f"🔄 MAC-adres wijzigen op {interface_name}...")
    
    # Haal huidige MAC-adres op
    if is_win:
        current_mac = get_current_mac_windows(interface_name)
    else:
        current_mac = get_current_mac_linux(interface_id)
    
    if current_mac:
        print(f"Huidige MAC: {current_mac}")
    else:
        print("⚠️ Kan het huidige MAC-adres niet ophalen")
    
    print(f"Nieuw MAC: {new_mac}")
    
    # Wijzig MAC-adres
    if is_win:
        success = change_mac_windows(interface_name, new_mac)
    else:
        success = change_mac_linux(interface_id, new_mac)
    
    if success:
        # Verifieer de wijziging
        verify_mac_change(interface_name if is_win else interface_id, new_mac, is_win)
    else:
        print(f"❌ MAC-adres wijziging mislukt!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Operatie geannuleerd door gebruiker")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Onverwachte fout: {e}")
        sys.exit(1)
