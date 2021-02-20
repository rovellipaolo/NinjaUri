import unittest
from unittest.mock import patch

from ninjauri import print_uri


class TestPrintUri(unittest.TestCase):

    ANY_RAW_URI = "https://en.wikipedia.org/wiki/URI"
    ANY_URI = {
        "raw": "raw-value",
        "any-key": "any-value",
        "any-key-without-value": None,
        "any-key-with-empty": "",
        "any-dict-key": {
            "any-dict-internal-key": "any-dict-internal-value"
        },
        "any-list-key": [
            "any-list-internal-value",
            "any-other-list-internal-value"
        ]
    }
    ANY_JSON = "any-json"

    @patch('ninjauri.json')
    def test_print_uri(self, mock_json):

        print_uri(self.ANY_URI, as_json=False)

        mock_json.dumps.assert_not_called()

    @patch('ninjauri.json')
    def test_print_uri_as_json(self, mock_json):
        mock_json.dumps.return_value = self.ANY_JSON

        print_uri(self.ANY_URI, as_json=True)

        mock_json.dumps.assert_called_once_with(
            self.ANY_URI,
            sort_keys=True,
            ensure_ascii=False,
            default=str,
            indent=4
        )


if __name__ == '__main__':
    unittest.main()
