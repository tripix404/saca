import unittest
from unittest.mock import patch
import platform
from unittest.mock import MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
class TestPlatformSpecific(unittest.TestCase):
    
    @unittest.skipUnless(platform.system().lower() == "linux", "Alleen uitvoeren op Linux")
    def test_linux_only_features(self):
        """Tests die alleen op Linux worden uitgevoerd"""
        with patch('subprocess.run') as mock_run:
            mock_process = MagicMock()
            mock_process.stdout = "eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>"
            mock_run.return_value = mock_process
            
            # Test Linux-specifieke functies hier
            self.assertTrue(True)  # Voorbeeld assert
    
    @unittest.skipUnless(platform.system().lower() == "windows", "Alleen uitvoeren op Windows")
    def test_windows_only_features(self):
        """Tests die alleen op Windows worden uitgevoerd"""
        with patch('subprocess.run') as mock_run:
            mock_process = MagicMock()
            mock_process.stdout = "Wi-Fi"
            mock_run.return_value = mock_process
            
            # Test Windows-specifieke functies hier
            self.assertTrue(True)  # Voorbeeld assert
if __name__ == '__main__':
    unittest.main()
