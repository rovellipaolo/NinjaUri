from argparse import Namespace
import unittest
from unittest.mock import patch

from ninjauri import main, WhoisException


class TestMain(unittest.TestCase):

    ANY_RAW_URI = "https://en.wikipedia.org/wiki/URI"
    ANY_URI = {
        "raw": ANY_RAW_URI
    }

    def any_args(self) -> Namespace:
        any_args = Namespace()
        any_args.target = self.ANY_RAW_URI
        any_args.verbose = False
        return any_args

    @patch('ninjauri.print_uri_info')
    @patch('ninjauri.parse_uri')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_happy_case(self, mock_parse_args, mock_parse_uri, mock_print_uri_info):
        mock_parse_args.return_value = self.any_args()
        mock_parse_uri.return_value = self.ANY_URI

        main()

        mock_parse_args.assert_called_once()
        mock_parse_uri.assert_called_once_with(self.ANY_RAW_URI)
        mock_print_uri_info.assert_called_once_with(self.ANY_URI)

    @patch('sys.exit')
    @patch('ninjauri.print_uri_info')
    @patch('ninjauri.parse_uri')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_when_uri_parsing_fails(self, mock_parse_args, mock_parse_uri, mock_print_uri_info, mock_sys_exit):
        mock_parse_args.return_value = self.any_args()
        mock_parse_uri.side_effect = ValueError()

        main()

        mock_parse_args.assert_called_once()
        mock_parse_uri.assert_called_once_with(self.ANY_RAW_URI)
        mock_print_uri_info.assert_not_called()
        mock_sys_exit.assert_called_once_with(1)

    @patch('sys.exit')
    @patch('ninjauri.print_uri_info')
    @patch('ninjauri.parse_uri')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_when_whois_retrieval_fails(self, mock_parse_args, mock_parse_uri, mock_print_uri_info, mock_sys_exit):
        mock_parse_args.return_value = self.any_args()
        mock_parse_uri.side_effect = WhoisException()

        main()

        mock_parse_args.assert_called_once()
        mock_parse_uri.assert_called_once_with(self.ANY_RAW_URI)
        mock_print_uri_info.assert_not_called()
        mock_sys_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
