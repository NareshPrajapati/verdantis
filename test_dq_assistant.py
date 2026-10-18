import copy
import unittest
from dq_assistant import analyze_records


class DataQualityTests(unittest.TestCase):
    def issue_types(self, records):
        return {x["issue_type"] for x in analyze_records(records)}

    def test_missing_part_number_and_weak_description(self):
        records = [
            {
                "item_id": "1",
                "item_description": "bearing",
                "manufacturer": "SKF",
                "manufacturer_part_number": "",
                "category": "Mechanical",
                "unit_of_measure": "EA",
                "source_system": "ERP-A",
            }
        ]
        issues = self.issue_types(records)
        self.assertIn("missing_part_number", issues)
        self.assertIn("weak_description_candidate", issues)

    def test_category_uom_and_business_key_duplicate(self):
        records = [
            {
                "item_id": "1",
                "item_description": "SKF Bearing 6205 ZZ",
                "manufacturer": "SKF",
                "manufacturer_part_number": "6205-ZZ",
                "category": "Electrical",
                "unit_of_measure": "EA",
                "source_system": "A",
            },
            {
                "item_id": "2",
                "item_description": "SKF Bearing 6205 ZZ",
                "manufacturer": "SKF",
                "manufacturer_part_number": "6205 ZZ",
                "category": "Mechanical",
                "unit_of_measure": "EACH",
                "source_system": "B",
            },
        ]
        issues = self.issue_types(records)
        self.assertIn("category_mismatch_candidate", issues)
        self.assertIn("unsupported_unit_of_measure", issues)
        self.assertIn("potential_duplicate", issues)

    def test_input_is_not_mutated(self):
        records = [{"item_id": "1", "item_description": " bearing ", "manufacturer": None}]
        original = copy.deepcopy(records)
        analyze_records(records)
        self.assertEqual(original, records)

    def test_non_object_row(self):
        result = analyze_records(["bad row"])
        self.assertEqual("malformed_row", result[0]["issue_type"])
        self.assertEqual("high", result[0]["severity"])


if __name__ == "__main__":
    unittest.main()
