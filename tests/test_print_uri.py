import unittest
from unittest.mock import call, patch

from ninjauri import print_uri


class TestPrintUri(unittest.TestCase):
    """
    Test print_uri method.
    """

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
    @patch('ninjauri.format_uri_info')
    def test_print_uri(self, mock_format_uri_info, mock_json):
        mock_format_uri_info.return_value = ""

        print_uri(self.ANY_URI, as_json=False)

        # NOTE: no call for "raw", "any-key-without-value" and "any-key-with-empty" keys!
        self.assertEqual(6, mock_format_uri_info.call_count)
        mock_format_uri_info.assert_has_calls(
            calls=[
                call("any-key", "any-value", 0),
                call("any-dict-key", None, 0),
                call("any-dict-internal-key", "any-dict-internal-value", 1),
                call("any-list-key", None, 0),
                call(None, "any-list-internal-value", 1),
                call(None, "any-other-list-internal-value", 1)
            ]
        )
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
