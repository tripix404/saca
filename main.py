import os
import sys
import subprocess
from colorama import init, Fore, Back, Style

init(autoreset=True)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
   

def run_script(script_path):
    """Run a Python script using subprocess."""
    print(f"\nStarting {script_path}...\n")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
    except FileNotFoundError:
        print(f"Script not found: {script_path}")
    input("\nPress Enter to return to main menu...")

import os
from colorama import init, Fore, Back, Style

init(autoreset=True)

def display_menu():
    """Display the main menu of the ethical hacking toolkit."""
    clear_screen()
    # Definieer de banner EERST
    banner = r"""
                                                 
                                                 
    .d8888b   8888b.   .d8888b  8888b.           
    88K          "88b d88P"        "88b          
    "Y8888b. .d888888 888      .d888888          
         X88 888  888 Y88b.    888  888          
    88888P' "Y888888  "Y8888P "Y888888           
                                                 
                                                 
                                                 
888                      888 888      d8b 888    
888                      888 888      Y8P 888    
888                      888 888          888     
888888  .d88b.   .d88b.  888 888  888 888 888888 
888    d88""88b d88""88b 888 888 .88P 888 888    
888    888  888 888  888 888 888888K  888 888    
Y88b.  Y88..88P Y88..88P 888 888 "88b 888 Y88b.  
 "Y888  "Y88P"   "Y88P"  888 888  888 888  "Y888 
"""
    width = os.get_terminal_size().columns

    # Print elke regel van de banner gecentreerd en gekleurd
    for line in banner.splitlines():
        print(Style.BRIGHT + Fore.RED + Back.BLACK + line.center(width) + Style.RESET_ALL)

    # Print de rest van het menu, ook gecentreerd als je dat mooi vindt:
    print(Style.BRIGHT + Fore.MAGENTA + "=" * width + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.YELLOW + "ETHICAL HACKING TOOLKIT - HOWEST - by Georges Devos".center(width) + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.MAGENTA + "=" * width + Style.RESET_ALL)
    print("1. DDoS Attack Tool".center(width))
    print("2. Web Scraper Tool".center(width))
    print("3. MAC Spoofer Tool".center(width))
    print("4. ARP Scanner Tool".center(width))
    print("0. Exit".center(width))
    print(Style.BRIGHT + Fore.MAGENTA + "=" * width + Style.RESET_ALL)
    return input("Selecteer een tool (0-4): ".center(width))



def main():
    """Main function that runs the ethical hacking toolkit."""
    while True:
        choice = display_menu()
        
        if choice == "1":
            run_script(os.path.join("ddos_attack", "ddos_attack.py"))
        elif choice == "2":
            run_script(os.path.join("web_scraper", "web_scraper.py"))
        elif choice == "3":
            run_script(os.path.join("mac_spoof", "mac_spoof.py"))
        elif choice == "4":
            run_script(os.path.join("arp_scanner", "arp_scanner.py"))
        elif choice == "0":
            print("\nBedankt voor het gebruiken van de Ethical Hacking Toolkit. Tot ziens!")
            break
        else:
            print("\nOngeldige keuze. Probeer opnieuw.")
            input("Druk op Enter om verder te gaan...")

if __name__ == "__main__":
    main()
