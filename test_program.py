import unittest
from unittest import TestCase
from main import create_tables
from main import load_json
from main import validation_check


class TestDataCase(TestCase):
    def test_crate_tables(self):
        self.assertIsNone(create_tables(), "Error: no tables were created")

    def test_load_json(self):
        self.name_schema = "goods.schema.json"
        self.result = load_json(self.name_schema)
        self.assertIsInstance(self.result, dict, "Error: result is not dict")

    def test_validation(self):
        self.uncorrect_json_file = load_json("uncorrect_json_file.json")
        self.name_schema = load_json("goods.schema.json")
        self.correct_json_file = load_json("json_file.json")
        self.result = validation_check(self.uncorrect_json_file, self.name_schema)
        self.assertFalse(self.result, "Error: validation passed, but shouldn't")
        self.result = validation_check(self.correct_json_file, self.name_schema)
        self.assertTrue(self.result, "Error: validation didn't pass, but should")


if __name__ == "__main__":
    unittest.main()
