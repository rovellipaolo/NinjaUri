import unittest

from ninjauri import get_domain


class TestParseDomain(unittest.TestCase):

    def test_get_domain(self):
        result = get_domain("wikipedia.org")

        self.assertEqual("org", result["tld"])
        self.assertEqual("wikipedia", result["sld"])
        self.assertEqual("wikipedia.org", result["domain"])
        self.assertEqual("", result["subdomain"])

    def test_get_subdomain(self):
        result = get_domain("en.wikipedia.org")

        self.assertEqual("en", result["subdomain"])


if __name__ == '__main__':
    unittest.main()
