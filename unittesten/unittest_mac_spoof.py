import unittest
import re
from unittest.mock import patch, MagicMock

import mac_spoof

class TestMacSpoof(unittest.TestCase):

    @patch('platform.system', return_value='Windows')
    def test_is_windows_true(self, mock_system):
        self.assertTrue(mac_spoof.is_windows())

    @patch('platform.system', return_value='Linux')
    def test_is_windows_false(self, mock_system):
        self.assertFalse(mac_spoof.is_windows())

    @patch('random.randint')
    def test_generate_valid_mac_format(self, mock_randint):
        # Forceer vaste bytes voor controle
        mock_randint.side_effect = [0x02, 0x11, 0x22, 0x33, 0x44, 0x55]
        mac = mac_spoof.generate_valid_mac()
        self.assertTrue(re.match(r"^([0-9A-F]{2}:){5}[0-9A-F]{2}$", mac))
        self.assertEqual(mac, "02:11:22:33:44:55")

    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "output\n"
        mock_run.return_value = mock_result
        output = mac_spoof.run_command(["echo", "test"])
        self.assertEqual(output, "output")

    @patch('subprocess.run', side_effect=mac_spoof.subprocess.CalledProcessError(1, 'cmd'))
    def test_run_command_fail(self, mock_run):
        output = mac_spoof.run_command(["fail"])
        self.assertEqual(output, "")

    @patch('os.geteuid', return_value=0)
    @patch('platform.system', return_value='Linux')
    def test_check_admin_linux(self, mock_system, mock_geteuid):
        self.assertTrue(mac_spoof.check_admin())

    @patch('os.geteuid', return_value=1000)
    @patch('platform.system', return_value='Linux')
    def test_check_admin_linux_false(self, mock_system, mock_geteuid):
        self.assertFalse(mac_spoof.check_admin())

    @patch('ctypes.windll.shell32.IsUserAnAdmin', return_value=True)
    @patch('platform.system', return_value='Windows')
    def test_check_admin_windows(self, mock_system, mock_admin):
        self.assertTrue(mac_spoof.check_admin())

    @patch('ctypes.windll.shell32.IsUserAnAdmin', side_effect=Exception)
    @patch('platform.system', return_value='Windows')
    def test_check_admin_windows_exception(self, mock_system, mock_admin):
        self.assertFalse(mac_spoof.check_admin())

    # Je kunt verder uitbreiden met meer tests voor registry-functies indien gewenst.

if __name__ == "__main__":
    unittest.main()
