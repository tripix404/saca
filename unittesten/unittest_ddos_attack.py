import unittest
import sys
import os
from unittest.mock import patch, MagicMock, call
from io import StringIO

import ddos_attack  # Verondersteld dat je script ddos_attack.py heet

class TestDDOSAttack(unittest.TestCase):

    @patch('os.system')
    def test_clear_screen_windows(self, mock_system):
        with patch('os.name', 'nt'):
            ddos_attack.clear_screen()
            mock_system.assert_called_with('cls')

    @patch('os.system')
    def test_clear_screen_linux(self, mock_system):
        with patch('os.name', 'posix'):
            ddos_attack.clear_screen()
            mock_system.assert_called_with('clear')

    @patch('os.get_terminal_size')
    def test_display_banner(self, mock_terminal):
        mock_terminal.return_value = os.terminal_size((80, 24))
        with patch('sys.stdout', new=StringIO()) as fake_out:
            ddos_attack.display_banner()
            output = fake_out.getvalue()
            self.assertIn(">>===<<", output)
            self.assertIn("_____", output)

    @patch('sys.exit')
    @patch('builtins.input', side_effect=['nee'])
    def test_bevestiging_annulering(self, mock_input, mock_exit):
        ddos_attack.bevestig_veilige_omgeving()
        mock_exit.assert_called_with(0)

    @patch('sys.exit')
    @patch('builtins.input', side_effect=['ja', '99'])
    def test_bevestiging_menu_terug(self, mock_input, mock_exit):
        ddos_attack.bevestig_veilige_omgeving()
        mock_exit.assert_called_with(0)

    @patch('ddos_attack.socket.socket')
    def test_flood_basic(self, mock_socket):
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        
        ddos_attack.stop_event.clear()
        ddos_attack.CAMOUFLAGE_DNS = False
        ddos_attack.flood()
        
        self.assertTrue(mock_sock.sendto.called)
        self.assertEqual(mock_sock.method_calls[0][0], 'sendto')

    @patch('ddos_attack.socket.socket')
    def test_flood_camouflage(self, mock_socket):
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        
        ddos_attack.stop_event.clear()
        ddos_attack.CAMOUFLAGE_DNS = True
        ddos_attack.flood()
        
        args, kwargs = mock_sock.sendto.call_args
        self.assertTrue(args[0].startswith(b'\x00\x00\x01\x00\x00\x01'))

    @patch('ddos_attack.threading.Thread')
    @patch('ddos_attack.bevestig_veilige_omgeving')
    @patch('ddos_attack.display_banner')
    @patch('ddos_attack.clear_screen')
    def test_main_flow(self, mock_clear, mock_banner, mock_bevestig, mock_thread):
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance
        
        with patch('sys.exit') as mock_exit:
            ddos_attack.main()
        
        mock_clear.assert_called()
        mock_banner.assert_called()
        mock_bevestig.assert_called()
        self.assertEqual(mock_thread.call_count, ddos_attack.NUM_STREAMS)

    @patch('sys.exit')
    @patch('ddos_attack.time.sleep', side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt(self, mock_sleep, mock_exit):
        ddos_attack.stop_event.clear()
        ddos_attack.main()
        self.assertTrue(ddos_attack.stop_event.is_set())

if __name__ == '__main__':
    unittest.main()
