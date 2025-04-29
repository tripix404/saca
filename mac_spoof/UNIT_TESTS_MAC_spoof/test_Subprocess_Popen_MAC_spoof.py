import unittest
from unittest.mock import patch
from unittest.mock import patch, MagicMock
import platform
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
class TestSubprocessMocking(unittest.TestCase):
    
    @patch('subprocess.Popen')
    def test_subprocess_call(self, mock_popen):
        """Test voor het correct mocken van subprocess.Popen calls"""
        # Mock opzetten
        process_mock = MagicMock()
        process_mock.communicate.return_value = (b'test output', b'test error')
        process_mock.returncode = 0
        mock_popen.return_value = process_mock
        
        # Functie aanroepen die subprocess.Popen gebruikt
        # Bijvoorbeeld: result = run_some_command("test")
        
        # Assertions
        # mock_popen.assert_called_once_with(["some", "command"], stdout=subprocess.PIPE)
        # process_mock.communicate.assert_called_once_with()
        # self.assertEqual(result, "test output")
if __name__ == '__main__':
    unittest.main()
