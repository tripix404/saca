import os
import sys
import importlib.util

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def import_script(script_path):
    """Import a Python script as a module."""
    spec = importlib.util.spec_from_file_location("module", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_ddos_attack():
    """Run the DDoS attack script."""
    print("\nStarting DDoS Attack Tool...\n")
    script_path = os.path.join("ddos_attack", "ddos_attack.py")
    try:
        module = import_script(script_path)
        # If the script has a main function, call it
        if hasattr(module, "main"):
            module.main()
        # Otherwise, the script was executed during import
    except Exception as e:
        print(f"Error running DDoS attack script: {e}")
    input("\nPress Enter to return to main menu...")

def run_web_scraper():
    """Run the web scraper script."""
    print("\nStarting Web Scraper Tool...\n")
    script_path = os.path.join("web_scraper", "web_scraper.py")
    try:
        module = import_script(script_path)
        # If the script has a main function, call it
        if hasattr(module, "main"):
            module.main()
        # Otherwise, the script was executed during import
    except Exception as e:
        print(f"Error running Web Scraper script: {e}")
    input("\nPress Enter to return to main menu...")

def run_mac_spoofer():
    """Run the MAC spoofer script."""
    print("\nStarting MAC Spoofer Tool...\n")
    script_path = os.path.join("mac_spoof", "mac_spoof.py")
    try:
        module = import_script(script_path)
        # If the script has a main function, call it
        if hasattr(module, "main"):
            module.main()
        # Otherwise, the script was executed during import
    except Exception as e:
        print(f"Error running MAC spoofer script: {e}")
    input("\nPress Enter to return to main menu...")

def run_arp_scanner():
    """Run the ARP scanner script."""
    print("\nStarting ARP Scanner Tool...\n")
    script_path = os.path.join("arp_scanner", "arp_scanner.py")
    try:
        module = import_script(script_path)
        # If the script has a main function, call it
        if hasattr(module, "main"):
            module.main()
        # Otherwise, the script was executed during import
    except Exception as e:
        print(f"Error running ARP scanner script: {e}")
    input("\nPress Enter to return to main menu...")

def display_menu():
    """Display the main menu of the ethical hacking toolkit."""
    clear_screen()
    print("=" * 50)
    print("        ETHICAL HACKING TOOLKIT - HOWEST")
    print("=" * 50)
    print("1. DDoS Attack Tool")
    print("2. Web Scraper Tool")
    print("3. MAC Spoofer Tool")
    print("4. ARP Scanner Tool")
    print("0. Exit")
    print("=" * 50)
    return input("Selecteer een tool (0-4): ")

def main():
    """Main function that runs the ethical hacking toolkit."""
    while True:
        choice = display_menu()
        
        if choice == "1":
            run_ddos_attack()
        elif choice == "2":
            run_web_scraper()
        elif choice == "3":
            run_mac_spoofer()
        elif choice == "4":
            run_arp_scanner()
        elif choice == "0":
            print("\nBedankt voor het gebruiken van de Ethical Hacking Toolkit. Tot ziens!")
            break
        else:
            print("\nOngeldige keuze. Probeer opnieuw.")
            input("Druk op Enter om verder te gaan...")

if __name__ == "__main__":
    main()
