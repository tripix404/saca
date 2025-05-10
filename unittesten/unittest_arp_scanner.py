import unittest
from unittest.mock import patch, MagicMock
import logging

from arp_scanner.arp_scanner import arp_scan

class TestARPScanner(unittest.TestCase):
    def setUp(self):
        self.mock_eth = MagicMock()
        self.mock_eth.name = "eth0"
        self.mock_eth.ip = "192.168.1.2"
        
        self.mock_wifi = MagicMock()
        self.mock_wifi.name = "wlan0"
        self.mock_wifi.ip = "192.168.1.3"
        
        self.mock_packet = MagicMock()
        self.mock_packet.psrc = "192.168.1.1"
        self.mock_packet.hwsrc = "00:11:22:33:44:55"

    @patch('scapy.all.get_working_ifaces')
    @patch('builtins.input', return_value='0')
    @patch('scapy.all.srp')
    def test_arp_scan_success(self, mock_srp, mock_input, mock_ifaces):
        """Test een succesvolle ARP-scan op Ethernet"""
        mock_srp.return_value = ([(MagicMock(), self.mock_packet)], [])
        mock_ifaces.return_value = [self.mock_eth, self.mock_wifi]
        
        result = arp_scan("192.168.1.0/24")
        
        self.assertEqual(len(result), 1)
        self.assertIn(result[0]['Interface'], ['eth0', 'wlan0'])

    @patch('scapy.all.get_working_ifaces')
    @patch('builtins.input', return_value='1')
    @patch('scapy.all.srp')
    def test_wifi_scan(self, mock_srp, mock_input, mock_ifaces):
        """Test scan via WiFi interface"""
        mock_srp.return_value = ([(MagicMock(), self.mock_packet)], [])
        mock_ifaces.return_value = [self.mock_eth, self.mock_wifi]
        
        result = arp_scan("192.168.1.0/24")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['Interface'], "wlan0")

    @patch('scapy.all.get_working_ifaces')
    def test_interface_filtering(self, mock_ifaces):
        """Test of alleen Ethernet/WiFi interfaces worden getoond"""
        mock_ifaces.return_value = [
            MagicMock(name="Bluetooth Network", ip="192.168.1.4"),
            MagicMock(name="lo", ip="127.0.0.1"),
            self.mock_eth,
            self.mock_wifi
        ]
        
        result = arp_scan()
        self.assertIsNone(result)  # Omdat gebruiker terugkeert naar hoofdmenu

    @patch('scapy.all.get_working_ifaces')
    @patch('builtins.input', return_value='0')
    @patch('scapy.all.srp', side_effect=Exception("Test error"))
    def test_error_handling(self, mock_srp, mock_input, mock_ifaces):
        """Test foutafhandeling tijdens scan"""
        mock_ifaces.return_value = [self.mock_eth]
        
        with self.assertLogs(level='CRITICAL') as cm:
            result = arp_scan("192.168.1.0/24")
            self.assertTrue(any("ARP-scan fout: Test error" in msg for msg in cm.output))
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
