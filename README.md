# Azure Zero Trust Security Operations Platform

**Detection engineering, cloud security governance, and safe incident response using Microsoft Sentinel, Defender for Cloud, Azure Policy, Terraform, KQL, and GitHub Actions.**

[![CI](https://github.com/alexcgodwin/azure-zero-trust-security-operations/actions/workflows/ci.yml/badge.svg)](https://github.com/alexcgodwin/azure-zero-trust-security-operations/actions/workflows/ci.yml)
![Azure](https://img.shields.io/badge/Microsoft-Azure-0078D4)
![Terraform](https://img.shields.io/badge/Terraform-4.x_Provider-844FBA)
![Security](https://img.shields.io/badge/SOC-Review_First-2D7D46)

## Executive summary

A security operations program needs more than a SIEM deployment. It needs clear trust boundaries, collected signals, actionable detection rules, ownership, measured risk, reviewable automation, and a tested escalation path. This repository supplies a **cost-aware, production-oriented reference implementation** for Azure security operations.

This project **does not** claim to operate an active SOC. Terraform is validated without a live tenant. No Sentinel, Defender, Entra PIM, Azure Functions, or paid security plans have been activated by this repository. Live deployment and connector validation require an authorized Azure subscription and change approval.

## Architecture

```text
                  Microsoft Entra ID
             (identity + human approvals)
                         |
GitHub PR --> CI: Terraform/KQL/Tests --> Protected environment
                         |                (optional OIDC identity)
                         v
              Azure subscription
                         |
      +------------------+------------------+
      |                  |                  |
Azure Activity      Entra SigninLogs   Defender for Cloud
(optional diag)    (connector manual)  (opt-in plans)
      |                  |                  |
      +------------------+------------------+
                         v
                  Log Analytics
                         |
                Microsoft Sentinel
                (opt-in onboarding)
                         |
              KQL scheduled analytics
              (off until sources ready)
                         |
                Incident investigation
                         |
                Read-only Python triage
                         |
              SOC analyst / change owner
                         |
             Manual, approved remediation
```

Azure Policy audit assignments evaluate designated resources; policy findings are not an automatic remediation engine. Azure Workload Identity Federation is isolated in a separate Terraform stack and grants **no Azure roles by default**.

## What is included

| Engineering area | Practical implementation | Boundary |
| --- | --- | --- |
| Security foundation | Resource group and Log Analytics workspace | Workspace ingestion may incur costs |
| Microsoft Sentinel | Optional workspace onboarding | Disabled by default |
| Detection-as-code | Three KQL analytics, metadata catalog and quality tests | Disabled until data sources exist |
| Azure activity telemetry | Optional subscription-level diagnostic routing | Requires approved privileged scope |
| Microsoft Entra telemetry | Failure-sign-in analytic | Connector and appropriate licensing required |
| Defender for Cloud | Opt-in subscription pricing for VMs, Storage, Key Vault | Changes subscription-wide paid plans |
| Governance | SOC-specific audit-only custom Azure Policy | No deny/remediation without review |
| Identity | GitHub OIDC federated identity example | RBAC grants intentionally separate |
| Response automation | Offline deterministic Python severity triage with tests | No automatic containment or deletion |
| CI/CD | Terraform fmt/init/validate + unit tests + repository checks | Read-only; no apply, no secrets |
| Operations | Incident playbooks, deployment/rollback, threat model, ADR | Deployment evidence not claimed |

## Repository layout

```text
terraform/
  platform/       Main SOC foundation, Sentinel and optional policies
  identity/       Optional GitHub OIDC federated identity, no RBAC grant
detections/
  catalog.json    Detection metadata: owners, severities and ATT&CK tactics
  queries/        KQL analytic queries
automation/
  triage.py       Safe, offline, read-only incident recommendations
examples/         Synthetic, non-sensitive test events
tests/            Standard-library automated tests
docs/
  ARCHITECTURE.md
  DEPLOYMENT.md
  SECURITY.md
  DETECTION_ENGINEERING.md
  OPERATIONS.md
  COST.md
  adr/            Architectural decisions
  runbooks/       Identity and networking investigations
.github/workflows/ci.yml
```

## Run the project locally (no cloud account required)

Requirements: Terraform >=1.6, Python >=3.10.

```bash
python -m unittest discover -s tests -v
python -m automation.triage examples/role-assignment-alert.json
terraform fmt -check -recursive terraform
cd terraform/platform && terraform init -backend=false && terraform validate
cd ../identity && terraform init -backend=false && terraform validate
```

This validates Terraform syntax/schema and triage logic. It does **not** validate actual Sentinel detections against live data, RBAC in a tenant, or control effectiveness in production.

## Deployment sequence

1. Read [Deployment](docs/DEPLOYMENT.md), [Security](docs/SECURITY.md), and [Cost](docs/COST.md).
2. Prepare Azure permissions, subscription ID and approved log destinations.
3. Configure a protected Azure Storage remote-state backend before a team-managed deployment.
4. Deploy base Log Analytics foundation after reviewing a Terraform plan.
5. Opt into diagnostics and confirm actual event ingestion in the workspace.
6. Opt into Sentinel; set up and test each data connector before enabling analytics.
7. Enable Defender plans and subscription policies **only** after separate billing and security approvals.
8. Apply the optional OIDC identity stack and explicitly review narrow RBAC grants and GitHub environment protections.
9. Test signals end-to-end and capture incident evidence.

Do not run unattended production applies. No real secrets, subscription IDs or client IDs are committed.

## Threat model and zero-trust stance

Identity assertions, network location and source-code origin are not implicit trust. The design minimizes broad privileges and dangerous automation. Analysts must validate signals; containment requires a human approver and a separate workflow. See [Security](docs/SECURITY.md).

## Technology

Terraform, Microsoft Azure, Azure Monitor, Log Analytics, Microsoft Sentinel, Defender for Cloud, Azure Policy, Microsoft Entra ID, KQL, Python 3, GitHub Actions, Workload Identity Federation, MITRE ATT&CK.

## Important limitations

- **PIM:** Entra Privileged Identity Management is a tenant-level licensed service. This repository documents the control architecture; it does not configure PIM.
- **Logic Apps / Azure Functions:** An automated containment service is deliberately NOT deployed; the included triage engine is offline and approval-first. A hardened integration would need signed source events, least-privilege credentials, private ingress, and approval workflow.
- **No SOC screenshots or deployment claims:** This is an IaC and detection reference implementation pending tenant-specific validation.
- **Cost:** Sentinel ingestion, retention and Defender plans can be chargeable; switches default to off.

## References

- [Microsoft Sentinel overview](https://learn.microsoft.com/azure/sentinel/overview)
- [Microsoft Defender for Cloud](https://learn.microsoft.com/azure/defender-for-cloud/defender-for-cloud-introduction)
- [Azure Policy](https://learn.microsoft.com/azure/governance/policy/overview)
- [Azure Monitor logs](https://learn.microsoft.com/azure/azure-monitor/logs/log-analytics-overview)
- [GitHub OIDC with Azure](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure)

**License:** MIT. © 2026 Alex Godwin.
