import unittest
from unittest.mock import patch

from ninjauri import get_whois


class TestGetWhois(unittest.TestCase):

    ANY_DOMAIN = "wikipedia.org"
    ANY_RAW_INFO = "any whois info"
    ANY_SERVER = "whois.wikipedia.org"
    ANY_ROOT_SERVER = "whois.org"

    @patch('ninjauri.get_root_server')
    @patch('ninjauri.get_whois_raw')
    def test_get_whois(self, mock_get_whois_raw, mock_get_root_server):
        mock_get_whois_raw.return_value = ([self.ANY_RAW_INFO], [self.ANY_SERVER])
        mock_get_root_server.return_value = self.ANY_SERVER

        result = get_whois(self.ANY_DOMAIN)

        self.assertEqual(self.ANY_RAW_INFO, result["raw"])
        self.assertEqual([self.ANY_SERVER], result["servers"])
        mock_get_whois_raw.assert_called_once_with(self.ANY_DOMAIN, with_server_list=True)
        mock_get_root_server.assert_called_once_with(self.ANY_DOMAIN)

    @patch('ninjauri.get_root_server')
    @patch('ninjauri.get_whois_raw')
    def test_get_whois_with_additional_root_server(self, mock_get_whois_raw, mock_get_root_server):
        mock_get_whois_raw.return_value = ([self.ANY_RAW_INFO], [self.ANY_SERVER])
        mock_get_root_server.return_value = self.ANY_ROOT_SERVER

        result = get_whois(self.ANY_DOMAIN)

        self.assertEqual(self.ANY_RAW_INFO, result["raw"])
        self.assertEqual([self.ANY_ROOT_SERVER, self.ANY_SERVER], result["servers"])
        mock_get_whois_raw.assert_called_once_with(self.ANY_DOMAIN, with_server_list=True)
        mock_get_root_server.assert_called_once_with(self.ANY_DOMAIN)


if __name__ == '__main__':
    unittest.main()
