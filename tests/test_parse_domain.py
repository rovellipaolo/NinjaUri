import unittest

from ninjauri import parse_domain


class TestParseDomain(unittest.TestCase):

    def test_parse_domain(self):
        uri = {"hostname": "wikipedia.org"}

        parse_domain(uri)

        self.assertEqual("org", uri["tld"])
        self.assertEqual("wikipedia", uri["sld"])
        self.assertEqual("wikipedia.org", uri["domain"])
        self.assertEqual("", uri["subdomain"])

    def test_parse_subdomain(self):
        uri = {"hostname": "en.wikipedia.org"}

        parse_domain(uri)

        self.assertEqual("en", uri["subdomain"])


if __name__ == '__main__':
    unittest.main()
