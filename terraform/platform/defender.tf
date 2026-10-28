# CAUTION: these change paid Defender for Cloud plans at the subscription scope.
# Do not enable without billing, ownership and entitlement approval.
resource "azurerm_security_center_subscription_pricing" "defender" {
  for_each = var.enable_defender_plans ? toset(["VirtualMachines", "StorageAccounts", "KeyVaults"]) : toset([])

  tier          = "Standard"
  resource_type = each.key
}
