from argparse import Namespace
from pythonwhois.shared import WhoisException
import unittest
from unittest.mock import patch

from ninjauri import main


class TestMain(unittest.TestCase):

    ANY_RAW_URI = "https://en.wikipedia.org/wiki/URI"
    ANY_URI = {
        "raw": ANY_RAW_URI
    }

    def any_args(self) -> Namespace:
        args = Namespace()
        args.target = self.ANY_RAW_URI
        args.verbose = False
        args.json = True
        return args

    @patch('ninjauri.print_uri')
    @patch('ninjauri.parse_uri')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_happy_case(self, mock_parse_args, mock_parse_uri, mock_print_uri):
        mock_parse_args.return_value = self.any_args()
        mock_parse_uri.return_value = self.ANY_URI

        result = main()

        mock_parse_args.assert_called_once()
        mock_parse_uri.assert_called_once_with(self.ANY_RAW_URI)
        mock_print_uri.assert_called_once_with(self.ANY_URI, as_json=True)
        self.assertEqual(0, result)

    @patch('ninjauri.print_uri')
    @patch('ninjauri.parse_uri')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_when_uri_parsing_fails(self, mock_parse_args, mock_parse_uri, mock_print_uri):
        mock_parse_args.return_value = self.any_args()
        mock_parse_uri.side_effect = ValueError()

        result = main()

        mock_parse_args.assert_called_once()
        mock_parse_uri.assert_called_once_with(self.ANY_RAW_URI)
        mock_print_uri.assert_not_called()
        self.assertEqual(1, result)

    @patch('ninjauri.print_uri')
    @patch('ninjauri.parse_uri')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_when_whois_retrieval_fails(self, mock_parse_args, mock_parse_uri, mock_print_uri):
        mock_parse_args.return_value = self.any_args()
        mock_parse_uri.side_effect = WhoisException()

        result = main()

        mock_parse_args.assert_called_once()
        mock_parse_uri.assert_called_once_with(self.ANY_RAW_URI)
        mock_print_uri.assert_not_called()
        self.assertEqual(1, result)


if __name__ == '__main__':
    unittest.main()
