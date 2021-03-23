import unittest
from parameterized import parameterized

from ninjauri import format_uri_info


# pylint: disable=too-many-arguments
class TestFormatUriInfo(unittest.TestCase):
    """
    Test format_uri_info method.
    """

    @parameterized.expand([
        [None, None, 0, "- None"],
        [None, None, 1, "\t- None"],
        [None, None, 2, "\t\t- None"],
        [None, "value", 0, "- value"],
        [None, "value", 1, "\t- value"],
        [None, "value", 2, "\t\t- value"],
        ["key", None, 0, "key:"],
        ["key", None, 1, "\tkey:"],
        ["key", None, 2, "\t\tkey:"],
        ["key", "value", 0, "key:         value"],
        ["key", "value", 1, "\tkey:        value"],
        ["key", "value", 2, "\t\tkey:       value"],
    ])
    def test_format_uri_info(self, key, value, depth, expected):
        result = format_uri_info(key=key, value=value, depth=depth)

        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
