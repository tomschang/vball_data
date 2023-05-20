# for testing all code

import unittest

import src.main as main
import jsonschema


class TestJSONMethods(unittest.TestCase):
    def test_validator(self):
        test_error = jsonschema.ValidationError

        # doesn't contain necessary fields
        with self.assertRaises(test_error):
            main.validate_json()
        # ...
        with self.assertRaises(test_error):
            main.validate_json()

        # two examples that should validate
        self.assertIsNone(main.validate_json())
        self.assertIsNone(main.validate_json())
