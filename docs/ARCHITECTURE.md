# Architecture and data flows

## Scope

This is a subscription-scoped Azure SOC **reference** built to make capabilities and
blast radius obvious. It separates the core workspace from the highly privileged
subscription diagnostics/Defender changes and the OIDC deployment identity.

### Trust boundaries

1. **GitHub repository:** untrusted PRs can request changes but CI is read-only and never runs Terraform apply.
2. **GitHub environments:** a protected production environment is needed before using the optional OIDC identity. Protect branches and require reviewers.
3. **Azure control plane:** an operator identity is needed to create resources. Terraform never grants itself Owner or Contributor.
4. **Telemetry ingestion:** Azure Activity Logs and Entra SigninLogs are different signals and require separate ingestion configuration.
5. **Detection evaluation:** Microsoft Sentinel analytics execute against tables only after data exists; no data means no credible detection.
6. **Incident handling:** findings and triage recommendations do not equal authorized response; a human approves containment.
7. **Subscription scope:** Defender plans and Azure activity diagnostics can affect the entire subscription, even though the workspace lives in one resource group.

## Logical view

    GitHub branch/PR
       |  read-only tests and schema checks
       v
    GitHub Actions CI
       |
       +--> Terraform validated offline
       +--> KQL catalog checks
       +--> Python triage + no-mutation tests

    [Operator-approved Terraform plan]
       |
       +--> SOC resource group
       |      +--> Log Analytics
       |              +--> Sentinel (opt-in)
       |                     +--> scheduled KQL detections (opt-in)
       +--> Audit-only Azure Policy (opt-in, RG scoped)
       +--> Activity Log subscription diagnostics (opt-in)
       +--> Defender pricing subscription settings (opt-in)

    AzureActivity + SigninLogs connectors --> workspace
         |
         v
    Sentinel analytics --> incidents --> analyst + read-only triage
                                     --> manual approval --> separate response

## Environment strategy

Use separate subscriptions for dev/test/prod when available. Naming alone is
not an authorization boundary. Do not connect sensitive production sign-in
logs to a personal learning tenant. Avoid mixing restricted datasets and PII.

## Terraform state

- Separate backend keys for platform and identity.
- Enable Azure Storage versioning, soft-delete, RBAC and private endpoints.
- Use Azure AD authentication for state; rotate access via group governance.
- Never place state artifacts in Git or GitHub Actions job artifacts.
- Review state access as privileged: it may contain cloud identifiers and secrets.

## Optional components

Entra PIM policies and identity governance are **design controls**, not
implemented tenant changes here. Adding Logic App playbooks requires a separate
review of triggers, connectors, approvers, privileges and rollback.
