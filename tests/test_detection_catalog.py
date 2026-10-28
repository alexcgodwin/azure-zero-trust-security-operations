import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DetectionCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads(
            (ROOT / "detections/catalog.json").read_text(encoding="utf-8")
        )

    def test_catalog_and_queries_exist(self):
        self.assertGreaterEqual(len(self.catalog), 3)
        for name, entry in self.catalog.items():
            with self.subTest(name=name):
                query = ROOT / "detections/queries" / entry["query_file"]
                self.assertTrue(query.is_file())
                contents = query.read_text(encoding="utf-8")
                self.assertIn("TimeGenerated", contents)
                self.assertIn("ago(1h)", contents)
                self.assertIn("project ", contents)

    def test_default_disabled_and_tactics_documented(self):
        for name, entry in self.catalog.items():
            with self.subTest(name=name):
                self.assertFalse(entry["enabled_by_default"])
                self.assertIn(entry["severity"], ["High", "Medium", "Low", "Informational"])
                self.assertTrue(entry["tactics"])
                self.assertEqual("PT1H", entry["frequency"])
                self.assertEqual("PT1H", entry["period"])

    def test_no_unused_query_files(self):
        referenced = {v["query_file"] for v in self.catalog.values()}
        actual = {p.name for p in (ROOT / "detections/queries").glob("*.kql")}
        self.assertEqual(referenced, actual)


if __name__ == "__main__":
    unittest.main()
