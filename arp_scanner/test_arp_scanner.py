import unitttest
form unittest import patch, MagicMock, mock_open
import asyncio



class TestEthicalHackingToolkit(unittest.TestCase):

    @patch('builtins.input', side_effect=['0'])
    @patch('scapy.all.get_working_ifaces')
    @patch('scapy.all.srp')
    def test_arp_scanner(self, mock_srp, mock_get_working_ifaces, mock_input):
        # Mock de interface en de ARP-scan resultaten
        mock_iface = MagicMock()
        mock_iface.name = 'eth0'
        mock_iface.ip = '192.168.1.2'
        mock_get_ifaces.return_value = [mock_iface]

        # mock arp response
        mock_srp.return_value = ([
            (magicMock(), MagicMock(psrc='192.168.1.10', hwsrc='00:11:22:33:44:55'))
        ], None)

        from toolkit import arp_scan
        devices = arp_scan('192.168.1.0/24')
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]['IP'], '192.168.1.10')
        self.assertEqual(devices[0]['MAC'], '00:11:22:33:44:55')

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_results(self, mock_json_dump, mock_file):
        from toolkit import save_results
        data = {'test': 'data'}
        save_results(data, 'testfile')
        mock_file.assert_called_once()
        mock_json_dump.assert_called_once()  # pylint: disable=no-member')    
        arg, kwargs = mock_json_dump.call_args
        self.assertIn('timestamp', args[0])
        self.assertEqual(args[0]['data'], data)

    @patch('paramiko.SSHClient.connect')
    @patch('paramiko.SSHClient.close')
    @patch('builtins.open', new_callable=mock_open, read_data='password1\npassword2\n')
    def test_ssh_bruteforce_success(self, mock_file, mock_close, mock_connect):
        from toolkit import ssh_bruteforce
        # simuleer een successvol connect op 2de wachtwoord
        def side_effect(host, port, username, password, timeout, banner_timeout):
            if password == 'password2':
                return None
            else:
                raise Exception('failed')
        mock_connect.side_effect = side_effect
        result = ssh_bruteforce('127.0.0.1')
        self.assertEqual(result)

    @patch('paramiko.SSHClient.connect', side_effect=Exception('failed'))
    @patch('builtins.open', new_callable=mock_open, read_data='password1\npassword2\n')
    def test_ssh_bruteforce_failure(self, mock_file, mock_connect):
        from toolkit import ssh_bruteforce
        result = ssh_bruteforce('127.0.0.1')
        self.assertFalse(result)
    
    def test_async_port_scan(self):
        from toolkit import async_port_scan
        # draai de async functie met een bekende gesloten poort
        async def run_test():
            result = wait async_port_scan('127.0.0.1', port=[65535])
            self.assertIsInstance(result, dict)
        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()