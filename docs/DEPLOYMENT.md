# Controlled deployment and rollback

## Minimum requirements

- Azure subscription with an authorized billing owner and SOC owner.
- Terraform >= 1.6, Azure CLI, permissions to create an RG and Log Analytics workspace.
- For Sentinel: Microsoft.SecurityInsights availability, workspace onboarding permission, cost approval.
- For Activity Log routing: subscription-level monitoring permissions and access to category-specific logs.
- For Entra SigninLogs: supported connector, tenant permissions/licensing and confirmed ingestion.
- For OIDC identity: a protected GitHub environment and explicit Azure RBAC review.
- Team use: pre-provisioned encrypted/private Azure Storage backend, access-controlled via Entra ID.

## Local checks before any Azure access

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/check_repo.py
python -m automation.triage examples/role-assignment-alert.json
terraform fmt -check -recursive terraform
terraform -chdir=terraform/platform init -backend=false -input=false
terraform -chdir=terraform/platform validate
terraform -chdir=terraform/identity init -backend=false -input=false
terraform -chdir=terraform/identity validate
```

## Baseline rollout

1. Ask the cloud and security owners to approve workspace location, retention, costs, IAM access and service data classification.
2. Copy `terraform/platform/terraform.tfvars.example` to the untracked `terraform.tfvars` and set your actual subscription ID.
3. Use `az login` and select the approved subscription. For automation prefer OIDC, not a saved client secret.
4. Configure an existing, hardened AzureRM backend. The checked-in `backend.tf.example` is **not active**.
5. Apply separately with review: `terraform plan -out=tfplan`, `terraform show tfplan`, then `terraform apply tfplan`. Protect plan files because they may contain data.
6. Verify the workspace ID, RBAC, and initial ingestion cost. **Do not** enable Sentinel, detections, or Defender plans just to prove Terraform works.
7. To enable Azure Activity diagnostics, approve the impact on the subscription and then set `enable_subscription_diagnostics = true`. Validate AzureActivity ingestion and ensure no duplicate diagnostic route.
8. To enable Sentinel, set `enable_sentinel = true`. Onboard the correct connectors through the permitted Azure workflow. Confirm real table schemas and data arrivals.
9. Only then consider `enable_detection_rules = true`. Each detection is also disabled at the rule level until tuned and explicitly enabled, even with the feature switch on.
10. For Defender pricing changes, assess plan/ingestion costs, data handling and existing tenant policy. Set `enable_defender_plans = true` only if specifically authorized.
11. For Azure Policy, `enable_governance_policy = true` creates an **Audit** effect only. Review compliance results before suggesting a Deny policy.

## Optional identity stack

Do not deploy the identity stack to an untrusted resource group.

```bash
cp terraform/identity/terraform.tfvars.example terraform/identity/terraform.tfvars
terraform -chdir=terraform/identity init -backend=false
terraform -chdir=terraform/identity plan
```

After creating the user-assigned identity and federated credential:
- Enable GitHub Actions environment protection and restriction to the trusted branch.
- Grant only the resource-level roles that a specific deployment job needs.
- Confirm the OIDC token subject, issuer and audience match exactly.
- Keep deployment workflows separated from read-only PR validation.

## Tests before calling a deployment complete

- AzureActivity: generate an approved test role assignment and verify the expected fields exist and propagate.
- NSG: perform an approved change in a test resource group; validate operation name and timestamp.
- SigninLogs: check an approved synthetic/test account, licensing and data connector.
- Verify incident grouping, false positives and customer data boundaries.
- Confirm analyst assignment, review records and manual response approval.
- Verify cost alerts and retention settings.

## Rollback and cleanup

- Disable analytics first; keep evidence.
- Roll back Terraform using reviewed commit and plan.
- Removing a Defender pricing resource can revert/change paid subscription settings; coordinate with subscription security owner.
- Removing diagnostics stops future routing, not existing retained records.
- Never destroy the shared state backend or Log Analytics evidence under incident hold.
- Terraform destroy is NOT a substitute for records retention, legal hold or financial approval.

## Known limitations

No tenant-specific plan or apply is performed in CI. Provider schema validation is useful, but cannot prove Azure API permissions, available features, actual detection performance, or costs.
