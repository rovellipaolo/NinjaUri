import unittest

from ninjauri import parse_uri_parts


class TestParseUriParts(unittest.TestCase):

    def test_parse_uri(self):
        uri = {"raw": "en.wikipedia.org"}

        parse_uri_parts(uri)

        self.assertEqual("en.wikipedia.org", uri["hostname"])

    def test_parse_uri_scheme(self):
        uri = {"raw": "https://en.wikipedia.org"}

        parse_uri_parts(uri)

        self.assertEqual("en.wikipedia.org", uri["hostname"])
        self.assertEqual("https", uri["protocol"])

    def test_parse_uri_path(self):
        uri = {"raw": "https://en.wikipedia.org/wiki/URI"}

        parse_uri_parts(uri)

        self.assertEqual("/wiki/URI", uri["path"])

    def test_parse_uri_query(self):
        uri = {"raw": "https://en.wikipedia.org?param1=aaa&param2=bbb"}

        parse_uri_parts(uri)

        self.assertEqual("param1=aaa&param2=bbb", uri["query"])

    def test_parse_uri_port(self):
        uri = {"raw": "http://localhost:8080"}

        parse_uri_parts(uri)

        self.assertEqual("8080", uri["port"])


if __name__ == '__main__':
    unittest.main()
