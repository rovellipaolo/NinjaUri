import unittest
from unittest.mock import patch

from ninjauri import get_whois


class TestGetWhois(unittest.TestCase):

    ANY_DOMAIN = "wikipedia.org"
    ANY_RAW_INFO = ["any whois info"]
    ANY_SERVERS = ["whois.org"]

    @patch('ninjauri.get_whois_raw')
    def test_get_whois(self, mock_get_whois_raw):
        mock_get_whois_raw.return_value = (self.ANY_RAW_INFO, self.ANY_SERVERS)

        whois, servers = get_whois(self.ANY_DOMAIN)

        self.assertEqual(self.ANY_RAW_INFO[0], whois)
        self.assertEqual(self.ANY_SERVERS, servers)
        mock_get_whois_raw.assert_called_once_with(self.ANY_DOMAIN, with_server_list=True)


if __name__ == '__main__':
    unittest.main()
