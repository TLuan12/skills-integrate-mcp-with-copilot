import json
import tempfile
import unittest
from pathlib import Path

from src.data_pipeline import import_activity_rows, import_activity_file, normalize_activity_record


class ImportPipelineTests(unittest.TestCase):
    def test_normalize_activity_record_converts_fields(self):
        activity = normalize_activity_record(
            {
                "name": "Chess Club",
                "description": "Learn strategies",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": "12",
                "participants": "michael@mergington.edu, daniel@mergington.edu",
            }
        )

        self.assertEqual(activity["name"], "Chess Club")
        self.assertEqual(activity["max_participants"], 12)
        self.assertEqual(activity["participants"], [
            "michael@mergington.edu",
            "daniel@mergington.edu",
        ])

    def test_import_activity_rows_builds_activity_map(self):
        rows = [
            {
                "name": "Chess Club",
                "description": "Learn strategies",
                "schedule": "Fridays",
                "max_participants": "12",
                "participants": "michael@mergington.edu, daniel@mergington.edu",
            },
            {
                "name": "Programming Class",
                "description": "Learn programming",
                "schedule": "Tuesdays",
                "max_participants": "20",
                "participants": "emma@mergington.edu",
            },
        ]

        activities = import_activity_rows(rows)

        self.assertIn("Chess Club", activities)
        self.assertIn("Programming Class", activities)
        self.assertEqual(activities["Programming Class"]["max_participants"], 20)

    def test_import_activity_file_supports_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "activities.json"
            payload = {
                "Chess Club": {
                    "description": "Learn strategies",
                    "schedule": "Fridays",
                    "max_participants": 12,
                    "participants": ["michael@mergington.edu"],
                }
            }
            path.write_text(json.dumps(payload), encoding="utf-8")

            imported = import_activity_file(path)
            self.assertEqual(imported["Chess Club"]["participants"], ["michael@mergington.edu"])


if __name__ == "__main__":
    unittest.main()
