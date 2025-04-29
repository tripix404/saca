import unittest
from unittest.mock import patch
from unittest.mock import patch, MagicMock
import platform
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
@patch('mac_spoof.run_command')
@patch('mac_spoof.is_windows')
def test_get_available_interfaces_linux(self, mock_is_windows, mock_run_command):
    """Test of get_available_interfaces correct werkt op Linux"""
    # Setup voor Linux
    mock_is_windows.return_value = False
    mock_output = "1: lo: <LOOPBACK,UP,LOWER_UP>\n    link/loopback 00:00:00:00:00:00\n2: eth0: <BROADCAST,UP>\n    link/ether 00:11:22:33:44:55"
    mock_run_command.return_value = mock_output
    
    # Functie aanroepen
    interfaces = get_available_interfaces()
    
    # Controleren of de juiste commando's zijn aangeroepen
    mock_run_command.assert_called_with(["ip", "link", "show"], "Kan netwerkinterfaces niet ophalen")
    
    # Controleren of de interfaces correct zijn geparsed
    self.assertIn(('eth0', 'eth0'), interfaces)
    self.assertNotIn(('lo', 'lo'), interfaces)  # loopback interface moet worden genegeerd
if __name__ == '__main__':
    unittest.main()
