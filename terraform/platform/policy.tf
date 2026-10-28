# Audit-only Azure Policy scoped to the SOC resource group. No blocking effect.
resource "azurerm_policy_definition" "audit_storage_public_network" {
  count        = var.enable_governance_policy ? 1 : 0
  name         = format("audit-soc-storage-public-network-%s", var.environment)
  policy_type  = "Custom"
  mode         = "Indexed"
  display_name = "Audit publicly accessible storage accounts used by SOC"
  description  = "Reports storage accounts with public network access enabled."

  policy_rule = jsonencode({
    if = {
      allOf = [
        { field = "type", equals = "Microsoft.Storage/storageAccounts" },
        { field = "Microsoft.Storage/storageAccounts/publicNetworkAccess", equals = "Enabled" }
      ]
    }
    then = { effect = "audit" }
  })
}
resource "azurerm_resource_group_policy_assignment" "soc_storage_guardrail" {
  count                = var.enable_governance_policy ? 1 : 0
  name                 = "audit-soc-storage-public"
  resource_group_id    = azurerm_resource_group.soc.id
  policy_definition_id = azurerm_policy_definition.audit_storage_public_network[0].id
  display_name         = "SOC storage public network access audit"
  description          = "Audit only; remediation is a reviewed operation."
}
