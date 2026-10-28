locals {
  suffix = format("%s-%s", var.name_prefix, var.environment)
  tags = merge(var.tags, {
    environment = var.environment
    workload    = "security-operations"
  })
  rules = jsondecode(file(format("%s/../../detections/catalog.json", path.module)))
}
resource "azurerm_resource_group" "soc" {
  name     = format("rg-%s-soc", local.suffix)
  location = var.location
  tags     = local.tags
}
resource "azurerm_log_analytics_workspace" "soc" {
  name                       = format("law-%s-soc", local.suffix)
  location                   = azurerm_resource_group.soc.location
  resource_group_name        = azurerm_resource_group.soc.name
  sku                        = "PerGB2018"
  retention_in_days          = var.workspace_retention_days
  daily_quota_gb             = var.daily_quota_gb
  internet_ingestion_enabled = true
  internet_query_enabled     = true
  tags                       = local.tags
}
