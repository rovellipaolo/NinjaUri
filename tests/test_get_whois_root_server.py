import unittest
from unittest.mock import patch

from ninjauri import get_whois_root_server


class TestGetWhoisRootServer(unittest.TestCase):

    ANY_DOMAIN = "wikipedia.org"
    ANY_SERVER = "whois.org"

    @patch('ninjauri.get_root_server')
    def test_get_whois(self, mock_get_root_server):
        mock_get_root_server.return_value = self.ANY_SERVER

        result = get_whois_root_server(self.ANY_DOMAIN)

        self.assertEqual(self.ANY_SERVER, result)
        mock_get_root_server.assert_called_once_with(self.ANY_DOMAIN)


if __name__ == '__main__':
    unittest.main()
