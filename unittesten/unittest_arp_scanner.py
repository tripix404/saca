import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, MagicMock, mock_open, AsyncMock
import sys
import asyncio
import os
from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'arp_scanner')))


import arp_scanner

class TestARPScanner(unittest.TestCase):
    """Basis tests voor het arp_scanner.py script"""
    
    def setUp(self):
        """Setup gemeenschappelijke test fixtures"""
        self.mock_iface = MagicMock()
        self.mock_iface.name = 'eth0'
        self.mock_iface.ip = '192.168.1.100'

    @patch('arp_scanner.Path') 
    @patch('json.dump')
    def test_save_results(self, mock_json_dump, mock_path):
        """Test dat save_results correct bestandsoperaties uitvoert"""
        mock_dir = MagicMock()
        mock_path.return_value = mock_dir
        mock_dir.iterdir.return_value = []  # Simuleer lege directory
        
        test_data = {'test_key': 'test_value'}
        
        with patch('builtins.open', mock_open()) as m:
            arp_scanner.save_results(test_data, 'test_filename')
        
        mock_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_json_dump.assert_called_once()

    @patch('arp_scanner.get_working_ifaces')
    @patch('arp_scanner.srp')
    @patch('builtins.input', side_effect=['0'])
    @patch('builtins.print')
    def test_arp_scan_successful(self, mock_print, mock_input, mock_srp, mock_get_ifaces):
        """Test ARP scan met een succesvolle respons"""
        mock_get_ifaces.return_value = [self.mock_iface]
        
        mock_received = MagicMock()
        mock_received.psrc = '192.168.1.1'
        mock_received.hwsrc = '00:11:22:33:44:55'
        mock_srp.return_value = ([(MagicMock(), mock_received)], [])
        
        result = arp_scanner.arp_scan('192.168.1.0/24')
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['IP'], '192.168.1.1')
        mock_srp.assert_called_once()

    @patch('arp_scanner.get_working_ifaces')
    @patch('builtins.input', side_effect=['99'])
    @patch('builtins.print')
    def test_arp_scan_back_to_menu(self, mock_print, mock_input, mock_get_ifaces):
        """Test terugkeren naar hoofdmenu vanuit ARP scan"""
        mock_get_ifaces.return_value = [self.mock_iface]
        result = arp_scanner.arp_scan('192.168.1.0/24')
        self.assertIsNone(result)

    @patch('arp_scanner.get_working_ifaces')
    @patch('builtins.print')
    def test_arp_scan_no_interfaces(self, mock_print, mock_get_ifaces):
        """Test ARP scan zonder geldige interfaces"""
        mock_get_ifaces.return_value = []
        result = arp_scanner.arp_scan('192.168.1.0/24')
        self.assertEqual(result, [])

class TestAsyncFunctions(IsolatedAsyncioTestCase):
    """Tests voor asynchrone functies"""
    
    async def test_check_port_open(self):
        """Test het controleren van een open poort"""
        with patch('asyncio.open_connection') as mock_conn:
            mock_writer = AsyncMock()
            mock_writer.wait_closed = AsyncMock()
            mock_conn.return_value = (AsyncMock(), mock_writer)
            
            result = await arp_scanner.check_port('192.168.1.1', 80)
            self.assertEqual(result[0], 80)

    async def test_check_port_closed(self):
        """Test het controleren van een gesloten poort"""
        with patch('asyncio.open_connection', side_effect=asyncio.TimeoutError):
            result = await arp_scanner.check_port('192.168.1.1', 81)
            self.assertIsNone(result)

class TestSSHBruteforce(unittest.TestCase):
    """Tests voor SSH bruteforce functie - TIJDELIJK OVERGESLAGEN"""
    
    @unittest.skip("Tijdelijk overgeslagen - wordt later opgelost")
    @patch('paramiko.SSHClient')
    @patch('time.sleep')
    def test_ssh_bruteforce_success(self, mock_sleep, mock_ssh):
        pass

class TestMainFunction(IsolatedAsyncioTestCase):
    """Tests voor hoofdprogramma"""
    
    @patch('arp_scanner.arp_scan')
    @patch('arp_scanner.async_port_scan')
    @patch('arp_scanner.save_results')
    @patch('builtins.input', return_value='192.168.1.0/24') 
    async def test_main_flow(self, mock_input, mock_save, mock_scan, mock_arp):
        """Test volledige workflow"""
        mock_arp.return_value = [{'IP': '192.168.1.1'}]
        mock_scan.return_value = {22: 'ssh'}
        
        await arp_scanner.main()
        mock_save.assert_called_once()

    @patch('arp_scanner.arp_scan', return_value=None)
    @patch('builtins.input', return_value='192.168.1.0/24')
    async def test_main_back_to_menu(self, mock_input, mock_arp):
        """Test main bij terugkeer naar menu"""
        await arp_scanner.main()
        mock_arp.assert_called_once()

if __name__ == '__main__':
    unittest.main()
