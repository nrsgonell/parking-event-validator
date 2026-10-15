import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validator import validate


class ValidatorTests(unittest.TestCase):
    def test_pairs_entry_and_exit(self):
        events = [
            {"timestamp": "2026-10-01T08:00:00", "plate": "TEST1", "event": "ENTRY"},
            {"timestamp": "2026-10-01T09:00:00", "plate": "TEST1", "event": "EXIT"},
        ]
        result = validate(events)
        self.assertEqual(len(result["paired"]), 1)
        self.assertEqual(result["anomalies"], [])

    def test_orphan_exit(self):
        result = validate([{"timestamp": "2026-10-01T09:00:00", "plate": "TEST1", "event": "EXIT"}])
        self.assertEqual(result["anomalies"][0]["type"], "orphan_exit")

    def test_duplicate_entry(self):
        result = validate([
            {"timestamp": "2026-10-01T08:00:00", "plate": "TEST1", "event": "ENTRY"},
            {"timestamp": "2026-10-01T08:01:00", "plate": "TEST1", "event": "ENTRY"},
        ])
        self.assertIn("duplicate_entry", [a["type"] for a in result["anomalies"]])


if __name__ == "__main__":
    unittest.main()
