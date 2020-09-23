import unittest
from unittest.mock import patch
from datetime import datetime

from ninjauri import parse_uri


class TestParseWhois(unittest.TestCase):

    ANY_RAW_URI = "https://en.wikipedia.org/wiki/URI"

    ANY_WHOIS_SERVER = "whois.pir.org"
    ANY_WHOIS_REGISTRAR_SERVER = "whois.markmonitor.com"
    ANY_WHOIS_REGISTRAR_EMAIL = "abusecomplaints@markmonitor.com"

    ANY_RAW_WHOIS = """Domain Name: WIKIPEDIA.ORG
        Registry Domain ID: D51687756-LROR
        Registrar WHOIS Server: %(registrar_server)s
        Registrar URL: http://www.markmonitor.com
        Updated Date: 2015-12-12T10:16:19Z
        Creation Date: 2001-01-13T00:12:14Z
        Registry Expiry Date: 2023-01-13T00:12:14Z
        Registrar Registration Expiration Date:
        Registrar: MarkMonitor Inc.
        Registrar IANA ID: 292
        Registrar Abuse Contact Email: %(registrar_email)s
        Registrar Abuse Contact Phone: +1.2083895740
        Reseller:
        Domain Status: clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited
        Domain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited
        Domain Status: clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited
        Registrant Organization: Wikimedia Foundation, Inc.
        Registrant State/Province: CA
        Registrant Country: US
        Name Server: NS0.WIKIMEDIA.ORG
        Name Server: NS1.WIKIMEDIA.ORG
        Name Server: NS2.WIKIMEDIA.ORG
        DNSSEC: unsigned
        URL of the ICANN Whois Inaccuracy Complaint Form https://www.icann.org/wicf/)
        >>> Last update of WHOIS database: 2020-05-28T14:27:51Z <<<
        
        For more information on Whois status codes, please visit https://icann.org/epp""" % {
        "registrar_server": ANY_WHOIS_REGISTRAR_SERVER,
        "registrar_email": ANY_WHOIS_REGISTRAR_EMAIL
    }

    @patch('ninjauri.get_root_server')
    @patch('ninjauri.get_whois_raw')
    def test_parse_uri(self, mock_get_whois_raw, mock_get_root_server):
        mock_get_whois_raw.return_value = ([self.ANY_RAW_WHOIS], [self.ANY_WHOIS_SERVER])
        mock_get_root_server.return_value = self.ANY_WHOIS_SERVER

        result = parse_uri(self.ANY_RAW_URI)

        # noinspection PyDictCreation
        expected_uri = {
            "admin_contacts": {},
            "available": False,
            "billing_contacts": {},
            "create_time": datetime(2001, 1, 13, 0, 12, 14),
            "domain": "wikipedia.org",
            "domain_id": "D51687756-LROR",
            "expire_time": datetime(2023, 1, 13, 0, 12, 14),
            "hostname": "en.wikipedia.org",
            "nameservers": [
                "ns0.wikimedia.org",
                "ns1.wikimedia.org",
                "ns2.wikimedia.org"
            ],
            "path": "/wiki/URI",
            "port": "",
            "protocol": "https",
            "query": "",
            "raw": self.ANY_RAW_URI,
            "registered": True,
            "registrant_contacts": {},
            "registrar": "MarkMonitor Inc.",
            "sld": "wikipedia",
            "status": [
                "clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited",
                "clientTransferProhibited https://icann.org/epp#clientTransferProhibited",
                "clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited"
            ],
            "subdomain": "en",
            "technical_contacts": {},
            "tld": "org",
            "update_time": datetime(2015, 12, 12, 10, 16, 19),
            "whois": {
                "emails": [
                    self.ANY_WHOIS_REGISTRAR_EMAIL
                ],
                "raw": self.ANY_RAW_WHOIS,
                "servers": [
                    self.ANY_WHOIS_REGISTRAR_SERVER,
                    self.ANY_WHOIS_SERVER
                ]
            }
        }
        self.assertDictEqual(expected_uri, result)


if __name__ == '__main__':
    unittest.main()
