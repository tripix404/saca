import unittest
import re
import sys
import os
from unittest.mock import patch, MagicMock

# Pad correctie voor imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mac_spoof')))
import mac_spoof

class TestMacSpoof(unittest.TestCase):

    # ─── Algemene tests ───────────────────────────────────────────────────────

    @patch('mac_spoof.platform.system')
    def test_is_windows(self, mock_system):
        mock_system.return_value = 'Windows'
        self.assertTrue(mac_spoof.is_windows())
        
        mock_system.return_value = 'Linux'
        self.assertFalse(mac_spoof.is_windows())

    @patch('mac_spoof.random.randint')
    def test_generate_valid_mac(self, mock_randint):
        mock_randint.side_effect = [0x02, 0x11, 0x22, 0x33, 0x44, 0x55]
        mac = mac_spoof.generate_valid_mac()
        self.assertEqual(mac, "02:11:22:33:44:55")
        self.assertTrue(re.match(r"^([0-9A-F]{2}:){5}[0-9A-F]{2}$", mac))

    # ─── Platform-specifieke tests ────────────────────────────────────────────

    @unittest.skipUnless(sys.platform.startswith("linux"), "Linux-specifieke test")
    class LinuxTests(unittest.TestCase):
        @patch('mac_spoof.os.geteuid')
        @patch('mac_spoof.platform.system', return_value='Linux')
        def test_check_admin_linux(self, mock_system, mock_geteuid):
            mock_geteuid.return_value = 0
            self.assertTrue(mac_spoof.check_admin())

            mock_geteuid.return_value = 1000
            self.assertFalse(mac_spoof.check_admin())

    @unittest.skipUnless(sys.platform.startswith("win"), "Windows-specifieke test")
    class WindowsTests(unittest.TestCase):
        @patch('mac_spoof.ctypes.windll.shell32.IsUserAnAdmin')
        @patch('mac_spoof.platform.system', return_value='Windows')
        def test_check_admin_windows(self, mock_system, mock_admin):
            mock_admin.return_value = True
            self.assertTrue(mac_spoof.check_admin())

            mock_admin.side_effect = Exception
            self.assertFalse(mac_spoof.check_admin())

    # ─── Cross-platform tests ─────────────────────────────────────────────────

    @patch('mac_spoof.subprocess.run')
    def test_run_command(self, mock_run):
        # Success test
        mock_result = MagicMock()
        mock_result.stdout = "output"
        mock_run.return_value = mock_result
        self.assertEqual(mac_spoof.run_command(["test"]), "output")

        # Failure test
        mock_run.side_effect = mac_spoof.subprocess.CalledProcessError(1, 'cmd')
        self.assertEqual(mac_spoof.run_command(["fail"]), "")

if __name__ == '__main__':
    unittest.main(failfast=True)
