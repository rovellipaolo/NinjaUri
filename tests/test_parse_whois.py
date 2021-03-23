import unittest

from ninjauri import parse_whois


class TestParseWhois(unittest.TestCase):
    """
    Test parse_whois method.
    """

    ANY_DOMAIN = "wikipedia.org"
    ANY_WHOIS_SERVER = "whois.pir.org"

    def test_parse_whois_domain_id(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "Domain Name: WIKIPEDIA.ORG\r\n"
                       "Registry Domain ID: D51687756-LROR\r\n",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual("D51687756-LROR", uri["domain_id"])

    def test_parse_whois_domain_id_when_missing(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual("", uri["domain_id"])

    def test_parse_whois_status(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "Domain Status: clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited\r\n"
                       "Domain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited\r\n"
                       "Domain Status: clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited\r\n",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual(
            [
                "clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited",
                "clientTransferProhibited https://icann.org/epp#clientTransferProhibited",
                "clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited"
            ],
            uri["status"]
        )

    def test_parse_whois_status_when_missing(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual([], uri["status"])

    def test_parse_whois_registrar(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "Registrar WHOIS Server: whois.markmonitor.com\r\n"
                       "Registrar URL: http://www.markmonitor.com\r\n"
                       "Registrar Registration Expiration Date:\r\n"
                       "Registrar: MarkMonitor Inc.\r\n"
                       "Registrar IANA ID: 292\r\n",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual("MarkMonitor Inc.", uri["registrar"])

    def test_parse_whois_registrar_when_missing(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual("", uri["registrar"])

    def test_parse_whois_dates(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "Updated Date: 2015-12-12T10:16:19Z\r\n"
                       "Creation Date: 2001-01-13T00:12:14Z\r\n"
                       "Registry Expiry Date: 2023-01-13T00:12:14Z\r\n"
                       "Registrar Registration Expiration Date:\r\n",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual("2001-01-13 00:12:14", str(uri["create_time"]))
        self.assertEqual("2015-12-12 10:16:19", str(uri["update_time"]))
        self.assertEqual("2023-01-13 00:12:14", str(uri["expire_time"]))

    def test_parse_whois_dates_when_missing(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertTrue("create_time" not in uri)
        self.assertTrue("update_time" not in uri)
        self.assertTrue("expire_time" not in uri)

    def test_parse_whois_nameservers(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "Name Server: NS0.WIKIMEDIA.ORG\r\n"
                       "Name Server: NS1.WIKIMEDIA.ORG\r\n"
                       "Name Server: NS2.WIKIMEDIA.ORG\r\n",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual(
            [
                "ns0.wikimedia.org",
                "ns1.wikimedia.org",
                "ns2.wikimedia.org"
            ],
            uri["nameservers"]
        )

    def test_parse_whois_nameservers_when_missing(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual([], uri["nameservers"])

    def test_parse_whois_server(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "Registrar WHOIS Server: whois.markmonitor.com\r\n"
                       "Registrar URL: http://www.markmonitor.com\r\n"
                       "Registrar Registration Expiration Date:\r\n"
                       "Registrar: MarkMonitor Inc.\r\n"
                       "Registrar IANA ID: 292\r\n",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual(["whois.markmonitor.com", self.ANY_WHOIS_SERVER], uri["whois"]["servers"])

    def test_parse_whois_server_when_missing(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual([self.ANY_WHOIS_SERVER], uri["whois"]["servers"])

    def test_parse_whois_contacts(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "Registrar WHOIS Server: whois.markmonitor.com\r\n"
                       "Registrar URL: http://www.markmonitor.com\r\n"
                       "Registrar Registration Expiration Date:\r\n"
                       "Registrar: MarkMonitor Inc.\r\n"
                       "Registrar IANA ID: 292\r\n",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual({}, uri["admin_contacts"])
        self.assertEqual({}, uri["billing_contacts"])
        self.assertEqual({}, uri["registrant_contacts"])
        self.assertEqual({}, uri["technical_contacts"])

    def test_parse_whois_contacts_when_missing(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual({}, uri["admin_contacts"])
        self.assertEqual({}, uri["billing_contacts"])
        self.assertEqual({}, uri["registrant_contacts"])
        self.assertEqual({}, uri["technical_contacts"])

    def test_parse_whois_emails(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "Registrar: MarkMonitor Inc.\r\n"
                       "Registrar IANA ID: 292\r\n"
                       "Registrar Abuse Contact Email: abusecomplaints@markmonitor.com\r\n"
                       "Registrar Abuse Contact Phone: +1.2083895740\r\n",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual(["abusecomplaints@markmonitor.com"], uri["whois"]["emails"])

    def test_parse_whois_emails_when_missing(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertEqual([], uri["whois"]["emails"])

    def test_parse_whois_available_registered_flags_when_no_match_for_domain(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "No match for \"MYDOMAIN.NET\".",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertTrue(uri["available"])
        self.assertFalse(uri["registered"])

    def test_parse_whois_available_registered_flags_when_status_is_missing(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertTrue(uri["available"])
        self.assertFalse(uri["registered"])

    def test_parse_whois_available_registered_flags_when_status_is_not_empty(self):
        uri = {
            "domain": self.ANY_DOMAIN,
            "whois": {
                "raw": "Status: ok",
                "servers": [self.ANY_WHOIS_SERVER]
            }
        }

        parse_whois(uri)

        self.assertFalse(uri["available"])
        self.assertTrue(uri["registered"])


if __name__ == '__main__':
    unittest.main()
