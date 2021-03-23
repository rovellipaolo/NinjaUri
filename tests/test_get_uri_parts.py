import unittest

from ninjauri import get_uri_parts


class TestGetUriParts(unittest.TestCase):
    """
    Test get_uri_parts method.
    """

    def test_get_uri_hostname(self):
        result = get_uri_parts("en.wikipedia.org")

        self.assertEqual("en.wikipedia.org", result["hostname"])

    def test_get_uri_scheme(self):
        result = get_uri_parts("https://en.wikipedia.org")

        self.assertEqual("en.wikipedia.org", result["hostname"])
        self.assertEqual("https", result["protocol"])

    def test_get_uri_parts_uri_path(self):
        result = get_uri_parts("https://en.wikipedia.org/wiki/URI")

        self.assertEqual("/wiki/URI", result["path"])

    def test_get_uri_parts_uri_query(self):
        result = get_uri_parts("https://en.wikipedia.org?param1=aaa&param2=bbb")

        self.assertEqual("param1=aaa&param2=bbb", result["query"])

    def test_get_uri_parts_uri_port(self):
        result = get_uri_parts("http://localhost:8080")

        self.assertEqual("8080", result["port"])


if __name__ == '__main__':
    unittest.main()
