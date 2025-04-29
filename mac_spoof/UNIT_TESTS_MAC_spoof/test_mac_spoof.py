import unittest
from unittest.mock import patch, MagicMock
import platform
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importeer de functies uit je MAC spoofing script
# Pas de import aan naar je eigen bestandsnaam
from mac_spoof import (
    is_windows,
    generate_mac,
    get_current_mac_linux,
    get_current_mac_windows,
    change_mac_linux,
    change_mac_windows,
    verify_mac_change,
    get_available_interfaces,
    run_command
)

class TestMacSpoof(unittest.TestCase):
    """Test class voor het MAC spoofing script"""

    def test_is_windows(self):
        """Test of de is_windows functie het juiste besturingssysteem detecteert"""
        # Echte platform-detectie gebruiken om te testen
        expected = platform.system().lower() == "windows"
        self.assertEqual(is_windows(), expected)

    def test_generate_mac(self):
        """Test of generate_mac een geldig MAC-adres genereert"""
        mac = generate_mac()
        # Controleer het formaat met een regex
        self.assertRegex(mac, r'^([0-9a-f]{2}:){5}[0-9a-f]{2}$')
        # Controleer of het eerste octet een even getal is (universeel/lokaal bit)
        first_byte = int(mac.split(':')[0], 16)
        self.assertEqual(first_byte & 0x01, 0, "Het eerste octet moet een even getal zijn")

    @patch('mac_spoof.run_command')
    def test_get_current_mac_linux(self, mock_run_command):
        """Test of get_current_mac_linux het MAC-adres correct ophaalt"""
        # Mock de output van het 'ip link show' commando
        mock_output = "2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT\n    link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff"
        mock_run_command.return_value = mock_output
        
        # Test de functie
        mac = get_current_mac_linux('eth0')
        
        # Controle of run_command is aangeroepen met de juiste parameters
        mock_run_command.assert_called_once_with(
            ["ip", "link", "show", "eth0"], 
            "Kan informatie van interface eth0 niet ophalen"
        )
        
        # Controleer of het MAC-adres correct is geëxtraheerd
        self.assertEqual(mac, "00:11:22:33:44:55")

    @patch('mac_spoof.run_command')
    def test_get_current_mac_windows(self, mock_run_command):
        """Test of get_current_mac_windows het MAC-adres correct ophaalt"""
        # Mock de output van het wmic commando
        mock_output = "Name                   MACAddress         \nWi-Fi                  00-11-22-33-44-55  \n"
        mock_run_command.return_value = mock_output
        
        # Test de functie
        mac = get_current_mac_windows('Wi-Fi')
        
        # Controle of run_command is aangeroepen met de juiste parameters
        mock_run_command.assert_called_once_with(
            ["wmic", "nic", "where", "NetEnabled=true", "get", "Name,MACAddress"],
            "Kan MAC-adressen niet ophalen"
        )
        
        # Controleer of het MAC-adres correct is geëxtraheerd en geconverteerd
        self.assertEqual(mac, "00:11:22:33:44:55")

    @patch('mac_spoof.run_command')
    def test_change_mac_linux(self, mock_run_command):
        """Test of change_mac_linux de juiste commando's uitvoert"""
        # Configureer de mock om succesvolle uitvoering na te bootsen
        mock_run_command.return_value = ""
        
        # Roep de functie aan
        result = change_mac_linux('eth0', '00:11:22:33:44:55')
        
        # Controleer of de functie waar retourneert (succes)
        self.assertTrue(result)
        
        # Controleer of de commando's in de juiste volgorde zijn uitgevoerd
        calls = [
            unittest.mock.call(["sudo", "ip", "link", "set", "dev", "eth0", "down"], 
                              "Kan interface eth0 niet uitschakelen"),
            unittest.mock.call(["sudo", "ip", "link", "set", "dev", "eth0", "address", "00:11:22:33:44:55"],
                              "Kan MAC-adres niet wijzigen"),
            unittest.mock.call(["sudo", "ip", "link", "set", "dev", "eth0", "up"],
                              "Kan interface eth0 niet inschakelen")
        ]
        mock_run_command.assert_has_calls(calls, any_order=False)

# python -m unittest test_mac_spoof.py

if __name__ == '__main__':
    unittest.main()
