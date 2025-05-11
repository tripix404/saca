import unittest
import sys
import os
from unittest.mock import patch, MagicMock, call
from io import StringIO

# Voeg het correcte pad toe aan sys.path indien nodig
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ddos_attack  # Verondersteld dat je script ddos_attack.py heet

class TestDDOSAttack(unittest.TestCase):

    # Bestaande tests blijven hetzelfde...

    @patch('ddos_attack.socket.socket')
    def test_flood_basic(self, mock_socket):
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        
        # Zorgt dat de loop slechts één keer wordt uitgevoerd
        with patch.object(ddos_attack.stop_event, 'is_set', side_effect=[False, True]):
            ddos_attack.CAMOUFLAGE_DNS = False
            ddos_attack.flood()
        
        self.assertTrue(mock_sock.sendto.called)
        self.assertEqual(mock_sock.method_calls[0][0], 'sendto')

    @patch('ddos_attack.socket.socket')
    def test_flood_camouflage(self, mock_socket):
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        
        # Zorgt dat de loop slechts één keer wordt uitgevoerd
        with patch.object(ddos_attack.stop_event, 'is_set', side_effect=[False, True]):
            ddos_attack.CAMOUFLAGE_DNS = True
            ddos_attack.flood()
        
        args, kwargs = mock_sock.sendto.call_args
        self.assertTrue(args[0].startswith(b'\x00\x00\x01\x00\x00\x01'))

    @patch('ddos_attack.threading.Thread')
    @patch('ddos_attack.bevestig_veilige_omgeving')
    @patch('ddos_attack.display_banner')
    @patch('ddos_attack.clear_screen')
    @patch('ddos_attack.time.sleep')  # Voorkom vertraging
    def test_main_flow(self, mock_sleep, mock_clear, mock_banner, mock_bevestig, mock_thread):
        # Zorg dat threads meteen als "niet actief" worden gezien
        mock_thread_instance = MagicMock()
        mock_thread_instance.is_alive.return_value = False
        mock_thread.return_value = mock_thread_instance
        
        # Voorkom dat stop_event wordt overschreven
        original_set = ddos_attack.stop_event.set
        
        try:
            with patch('sys.exit') as mock_exit:
                ddos_attack.main()
            
            mock_clear.assert_called()
            mock_banner.assert_called()
            mock_bevestig.assert_called()
            self.assertEqual(mock_thread.call_count, ddos_attack.NUM_STREAMS)
        finally:
            # Herstel stop_event functionaliteit
            ddos_attack.stop_event.set = original_set

    @patch('sys.exit')
    @patch('ddos_attack.time.sleep', side_effect=KeyboardInterrupt)
    @patch('ddos_attack.threading.Thread')  # Voorkom echte threads
    @patch('ddos_attack.bevestig_veilige_omgeving')
    def test_keyboard_interrupt(self, mock_bevestig, mock_thread, mock_sleep, mock_exit):
        # Zorg dat de threads niet echt worden gestart
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance
        
        ddos_attack.stop_event.clear()
        ddos_attack.main()
        self.assertTrue(ddos_attack.stop_event.is_set())

if __name__ == '__main__':
    unittest.main()
