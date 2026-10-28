import json
import unittest
from pathlib import Path

from automation.triage import Incident, assess_incident, parse_incident


ROOT = Path(__file__).resolve().parents[1]


class TriageTests(unittest.TestCase):
    def test_high_severity_privilege_change_is_urgent(self):
        incident = parse_incident(json.loads(
            (ROOT / "examples/role-assignment-alert.json").read_text(encoding="utf-8")
        ))
        decision = assess_incident(incident)
        self.assertEqual("P1", decision["priority"])
        self.assertTrue(decision["approval_required"])
        self.assertFalse(decision["automatic_changes_executed"])

    def test_approved_change_lowers_routing_priority(self):
        incident = Incident(
            incident_id="SOC-ABC", alert_type="nsg-rule-change",
            severity="High", environment="prod", approved_change=True
        )
        self.assertEqual("P2", assess_incident(incident)["priority"])

    def test_reject_unrecognized_alert_type(self):
        with self.assertRaises(ValueError):
            parse_incident({
                "incident_id": "SOC-ABCD", "alert_type": "execute-command",
                "severity": "High", "environment": "prod"
            })

    def test_reject_non_boolean_approval(self):
        with self.assertRaises(ValueError):
            parse_incident({
                "incident_id": "SOC-ABCD", "alert_type": "nsg-rule-change",
                "severity": "High", "environment": "prod",
                "approved_change": "false"
            })

    def test_no_automatic_actions_in_any_example(self):
        for path in (ROOT / "examples").glob("*alert.json"):
            with self.subTest(path=path.name):
                payload = json.loads(path.read_text(encoding="utf-8"))
                result = assess_incident(parse_incident(payload))
                self.assertEqual("advisory_only", result["mode"])
                self.assertFalse(result["automatic_changes_executed"])


if __name__ == "__main__":
    unittest.main()
