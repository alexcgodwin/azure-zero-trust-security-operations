# SOC operations and on-call model

## Daily

- Confirm Log Analytics ingest activity, connector health and workspaces in the correct region.
- Investigate analytic rule failures, unusual alert volumes and ingestion spikes.
- Check Defender for Cloud recommendations against owned assets and exceptions.
- Validate GitHub CI health for changed rules and Terraform plans.

## Incident handling

1. Receive incident, record unique ID and source.
2. Correlate AzureActivity, SigninLogs and authorized change tickets.
3. Run the offline triage model only on a sanitized event (never real credentials).
4. Assign risk score and P1/P2/P3 route.
5. Obtain approval for any containment/change.
6. Execute response using approved runbook and least-privilege operator.
7. Record scope, evidence, approvals, recovery validation and timeline.

## Escalation

- P1: suspected critical production identity compromise or unauthorized privilege escalation; page security on-call immediately.
- P2: important but contained anomaly; investigate within the agreed SOC SLO.
- P3: lower confidence or approved change; queue review and suppression tuning.

The supplied risk score is a demonstrator—not a compliance rating or an authoritative incident severity engine. Human analysts may override it with documented rationale.

## Maintenance

- Monthly: query efficiency, latency, cost, exception expiry and threat intelligence.
- Quarterly: access review, Defender plan scope, detection catalog and dry-run tabletop.
- Annually: disaster recovery exercise and data retention review.

See runbooks/ for scenario-specific investigations.
