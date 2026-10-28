# Zero Trust security and threat model

## Security objectives

- Every deployment identity is explicitly scoped and auditable.
- Security data must remain inside an approved region and within defined retention.
- Detection logic and response recommendations are reviewed and version-controlled.
- No automated privilege escalation, user lockout or network containment is executed by repository automation.
- Subscription-wide changes are explicit opt-ins.

| Threat | Control | Residual risk |
| --- | --- | --- |
| Compromised PR | GitHub CI has read-only permissions and no Azure login | Maintainer merge bypass |
| Stolen deploy credentials | GitHub OIDC, no static client secrets | Unsafe environment protections or overly broad Azure RBAC |
| Malicious rule deployment | Peer-reviewed Terraform/KQL and protected production environment | Bad query can still create high alert volume/cost |
| Data exfiltration | Restricted workspace RBAC; no shared SIEM exports | Log Analytics public ingestion/query endpoints unless further secured |
| False positives | Disabled-by-default scheduled analytics and tuning guidance | Alert fatigue after activation |
| Unexpected Defender billing | Off by default with documented subscription-wide scope | Owner enables without budget |
| Destructive incident playbook | Read-only triage and human approval | Manual operators can still make mistakes |
| State leakage | Ignore state and backend values; Azure AD state auth recommended | Privileged backend operator compromise |

## Identity and privilege model

Use Entra groups for analysts and separate operators. Suggested duties:

- SOC analyst: view incidents, investigate and annotate.
- SOC detection engineer: propose reviewed detection changes.
- Platform operator: manage workspace and approved diagnostic settings.
- Cloud security owner: approve Defender tier changes and subscription policy.
- Incident commander: approve containment decisions.
- Privileged identity admin: maintain Entra PIM eligibility and approvals outside this Terraform codebase.

Avoid assigning subscription Owner/Contributor to CI. For production deploys, use a dedicated environment-scoped federated identity and a custom role where practical. No Azure RBAC assignment is created by the identity Terraform stack.

## Azure policy and Defender

The included custom Azure Policy uses an **Audit** effect, not Deny. It is explicitly assigned to the SOC resource group only. The optional Defender resources have subscription-level billing impact. Check existing pricing resources before attempting management via Terraform; import/adopt rather than fighting external drift.

## Data protection

AzureActivity and SigninLogs can include identities, IP addresses and sensitive administrative activity. Treat them as restricted operational records. Never commit actual incident JSON to this repository. Set retention based on your organization's privacy schedule and assess cross-border replication and export rules.

## Threat response

All automatic actions are intentionally disabled. Before introducing Azure Functions/Logic Apps runbooks:
1. Authenticate caller using Microsoft Entra, not a public webhook key alone.
2. Scope credentials to the exact target resource or account class.
3. Require approval for block, isolation, disable, deletion or network changes.
4. Implement idempotency, signed request validation and replay protection.
5. Document rollback and verify audit trail in test tenant.
