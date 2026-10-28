# Detection engineering playbook

## Rule lifecycle

Hypothesis → data source contract → query → test dataset → false-positive review
→ peer review → deploy disabled → confirm ingestion → run simulation
→ enable at low volume → tune → monitor rule health.

The included Terraform intentionally has TWO gates: global enablement
(`enable_sentinel` + `enable_detection_rules`) and per-rule
`enabled_by_default: false`. Turning on only the feature switches does
not switch each rule into active alerting.

## Detection catalog

| Rule | Table | Intent | Baseline tuning |
| --- | --- | --- | --- |
| privileged-role-assignment | AzureActivity | RBAC role assignment writes | Known automation/service principal allowlist |
| nsg-rule-change | AzureActivity | NSG rule create/update/delete | Scheduled infrastructure changes |
| repeated-signin-failures | SigninLogs | Distributed failed sign-ins | Conditional Access/service account activity |

## Verification

Run `python -m unittest discover -s tests -v`. Tests verify that
queries exist, include time windows and produce projected columns; they are
NOT a KQL engine. For full verification, ingest approved sample data to a
test workspace and execute each query in Log Analytics before switching it
on. Validate field names and provider limits against the connected table.

## Operational metrics

Track: rule executions, data delay, true/false-positive ratio, unowned
incidents, detection-to-triage time, severity changes and exception expiry.
Re-review quarterly and after major identity/network topology changes.

## ATT&CK mapping

The catalog includes technique **tactics**. Review true technique mappings
per rule at onboarding; do not claim MITRE detection coverage without
measured validation. Failed sign-in bursts are investigative signals rather
than proof of compromise.
