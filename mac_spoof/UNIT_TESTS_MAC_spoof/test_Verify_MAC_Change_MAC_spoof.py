import unittest
from unittest.mock import patch
from unittest.mock import patch, MagicMock
import platform
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
@patch('mac_spoof.get_current_mac_linux')
def test_verify_mac_change_linux(self, mock_get_mac):
    """Test of verify_mac_change correct werkt op Linux"""
    # Configureer de mock om een MAC-adres te retourneren
    mock_get_mac.return_value = "00:11:22:33:44:55"
    
    # Test met gelijke MAC-adressen (succesvolle wijziging)
    self.assertTrue(verify_mac_change("eth0", "00:11:22:33:44:55", False))
    
    # Test met verschillende MAC-adressen (mislukte wijziging)
    self.assertFalse(verify_mac_change("eth0", "AA:BB:CC:DD:EE:FF", False))
if __name__ == '__main__':
    unittest.main()
