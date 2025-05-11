import unittest
import os
import sys

# Zorg dat de parent directory in sys.path staat zodat modules gevonden worden
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ddos_attack')))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def discover_and_run_all():
    """Ontdekt en draait alle unittesten in deze map."""
    loader = unittest.TestLoader()
    suite = loader.discover(SCRIPT_DIR, pattern="unittest_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result

def run_specific(test_name):
    """Draait een specifieke unittest-module uit deze map."""
    if not test_name.endswith('.py'):
        test_name += '.py'
    test_path = os.path.join(SCRIPT_DIR, test_name)
    if not os.path.exists(test_path):
        print(f"❌ Testbestand '{test_name}' niet gevonden in map '{os.path.basename(SCRIPT_DIR)}'.")
        return
    # Importeer als module
    module_name = test_name[:-3]  # zonder .py
    suite = unittest.defaultTestLoader.loadTestsFromName(module_name)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

def main():
    print("Kies een optie:")
    print("1) Alle unittesten uitvoeren")
    print("2) Een specifieke unittest uitvoeren")
    keuze = input("Keuze (1/2): ").strip()
    if keuze == "1":
        discover_and_run_all()
    elif keuze == "2":
        print("Beschikbare unittest-bestanden:")
        for fname in sorted(os.listdir(SCRIPT_DIR)):
            if fname.startswith("unittest_") and fname.endswith(".py"):
                print(f" - {fname}")
        test_name = input("Voer de naam van het unittest-bestand in (bijv. unittest_arp_scanner.py): ").strip()
        run_specific(test_name)
    else:
        print("❌ Ongeldige keuze.")

if __name__ == "__main__":
    main()
