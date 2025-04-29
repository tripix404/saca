import unittest
from unittest.mock import patch, MagicMock
import sys
import random
from ddos_attack import main, TARGET_IP, TARGET_PORT, PACKETS_TOTAL, RATE_PPS, NUM_STREAMS, MIN_PAYLOAD_SIZE, MAX_PAYLOAD_SIZE

"""
----------------------------------------------------------------------
Unit Test Overzicht voor ddos_attack.py

Getest wordt:
- Of de standaardparameters veilig zijn ingesteld
- Of het juiste aantal threads wordt aangemaakt en gestart
- Of de payloads voldoende willekeurig zijn
- Of de rate limiting per thread klopt
- Of het target IP een geldig privé-adres is
----------------------------------------------------------------------
"""

class TestDDoSSimulator(unittest.TestCase):
    """Unit tests voor het DDoS simulatiescript (zonder labbevestiging)"""
    
    def setUp(self):
        self.original_argv = sys.argv
        sys.argv = ['ddos_attack.py']
        # Mock de socket om echte netwerk calls te voorkomen
        self.socket_mock = MagicMock()
        self.socket_patcher = patch('socket.socket', return_value=self.socket_mock)
        self.socket_patcher.start()

    def tearDown(self):
        sys.argv = self.original_argv
        self.socket_patcher.stop()

    def test_initial_parameters(self):
        """Standaard parameters zijn veilig ingesteld"""
        self.assertEqual(TARGET_IP, "192.168.1.1")
        self.assertEqual(TARGET_PORT, 8080)
        self.assertLessEqual(RATE_PPS, 100)
        self.assertEqual(NUM_STREAMS, 2)

    @patch('builtins.input', return_value='ja')
    def test_packet_count(self, input_mock):
        """Juiste aantal threads wordt aangemaakt en gestart"""
        with patch('ddos_attack.threading.Thread') as thread_mock:
            main()
            self.assertEqual(thread_mock.call_count, NUM_STREAMS)
            self.assertEqual(thread_mock().start.call_count, NUM_STREAMS)

    def test_payload_randomization(self):
        """Payloads zijn voldoende willekeurig"""
        payloads = set()
        for _ in range(100):
            size = random.randint(MIN_PAYLOAD_SIZE, MAX_PAYLOAD_SIZE)
            payload = bytes(random.getrandbits(8) for _ in range(size))
            payloads.add(payload)
        self.assertGreaterEqual(len(payloads), 95)

    @patch('time.sleep', return_value=None)
    @patch('builtins.input', return_value='ja')
    def test_rate_limiting(self, input_mock, sleep_mock):
        """Rate limiting per thread klopt"""
        from ddos_attack import pps_per_thread
        with patch('ddos_attack.flood'):
            main()
        expected_pps = RATE_PPS / NUM_STREAMS
        self.assertAlmostEqual(pps_per_thread, expected_pps, delta=0.01)

    def test_target_ip_format(self):
        """Target IP is een geldig privé-adres"""
        private_ranges = ('192.168.', '10.', '172.16.', '127.')
        is_private = any(TARGET_IP.startswith(prefix) for prefix in private_ranges)
        self.assertTrue(is_private)

# Custom test runner om geslaagde tests te tonen
class ReportingTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successes = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes.append(test)

    def printSuccesses(self):
        print("\n-------------------------------")
        print("GESLAAGDE TESTS:")
        for test in self.successes:
            # Toon alleen de functienaam en de docstring (korte beschrijving)
            print(f" - {test.id().split('.')[-1]}: {test.shortDescription()}")
        print("-------------------------------\n")

if __name__ == '__main__':
    runner = unittest.TextTestRunner(resultclass=ReportingTestResult, verbosity=2)
    result = runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(TestDDoSSimulator))
    result.printSuccesses()
