"""Read-only SOC alert triage. No Azure or Microsoft Graph mutations.

Usage:
    python -m automation.triage examples/role-assignment-alert.json

Output is an ADVISORY recommendation, never an automated account block,
policy change, isolation, deletion, or incident closure.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

KNOWN_TYPES = frozenset({
    "privileged-role-assignment",
    "nsg-rule-change",
    "repeated-signin-failures",
})
SEVERITY_ORDER = {"Informational": 0, "Low": 1, "Medium": 2, "High": 3}


@dataclass(frozen=True)
class Incident:
    incident_id: str
    alert_type: str
    severity: str
    environment: str
    approved_change: bool = False
    production_scope: bool = False
    indicators: tuple[str, ...] = ()


def parse_incident(payload: Mapping[str, Any]) -> Incident:
    """Validate a minimal event contract without accepting privileged action fields."""
    if not isinstance(payload, dict):
        raise ValueError("Expected a JSON object")
    required = ("incident_id", "alert_type", "severity", "environment")
    for key in required:
        if not isinstance(payload.get(key), str) or not payload[key].strip():
            raise ValueError(f"{key} must be a nonempty string")
    if payload["alert_type"] not in KNOWN_TYPES:
        raise ValueError("Unsupported alert_type")
    if payload["severity"] not in SEVERITY_ORDER:
        raise ValueError("Unsupported severity")
    if payload["environment"] not in ("dev", "test", "prod"):
        raise ValueError("Unsupported environment")
    if not re.fullmatch(r"[a-zA-Z0-9._:-]{3,100}", payload["incident_id"]):
        raise ValueError("Invalid incident_id")
    for flag in ("approved_change", "production_scope"):
        if type(payload.get(flag, False)) is not bool:
            raise ValueError(f"{flag} must be boolean")
    indicators = payload.get("indicators", [])
    if not isinstance(indicators, list) or len(indicators) > 20:
        raise ValueError("indicators must be a list with at most 20 entries")
    if not all(isinstance(v, str) and len(v) <= 256 for v in indicators):
        raise ValueError("indicators must contain short strings")
    return Incident(
        incident_id=payload["incident_id"],
        alert_type=payload["alert_type"],
        severity=payload["severity"],
        environment=payload["environment"],
        approved_change=payload.get("approved_change", False),
        production_scope=payload.get("production_scope", False),
        indicators=tuple(indicators),
    )


def assess_incident(incident: Incident) -> dict[str, Any]:
    """Rank routing urgency. Never execute remediation."""
    score = 10 + SEVERITY_ORDER[incident.severity] * 20
    if incident.production_scope or incident.environment == "prod":
        score += 20
    if incident.alert_type == "privileged-role-assignment":
        score += 15
    if incident.alert_type == "repeated-signin-failures":
        score += 10
    if incident.approved_change:
        score -= 35
    score = max(0, min(100, score))
    priority = "P1" if score >= 80 else "P2" if score >= 55 else "P3"
    steps = {
        "privileged-role-assignment": [
            "Verify scope and principal against change approval.",
            "Review AzureActivity correlation ID and caller identity.",
            "Escalate any unexplained elevation to identity owners.",
        ],
        "nsg-rule-change": [
            "Review the NSG effective rules and network exposure.",
            "Correlate operation with approved change and deployment history.",
            "Escalate unexpected broad ingress to the network on-call.",
        ],
        "repeated-signin-failures": [
            "Validate successful sign-ins, device context and MFA events.",
            "Compare source IPs with approved business travel and VPNs.",
            "Escalate suspected account compromise to identity response.",
        ],
    }[incident.alert_type]
    return {
        "incident_id": incident.incident_id,
        "priority": priority,
        "risk_score": score,
        "approval_required": True,
        "mode": "advisory_only",
        "recommended_actions": steps,
        "automatic_changes_executed": False,
    }


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("Usage: python -m automation.triage <incident.json>", file=sys.stderr)
        return 2
    try:
        path = Path(args[0])
        if path.stat().st_size > 65_536:
            raise ValueError("Incident exceeds 64 KiB")
        payload = json.loads(path.read_text(encoding="utf-8"))
        result = assess_incident(parse_incident(payload))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Invalid incident: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
