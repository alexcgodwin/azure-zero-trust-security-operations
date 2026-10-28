output "soc_resource_group" {
  value       = azurerm_resource_group.soc.name
  description = "Resource group containing SOC resources."
}
output "log_analytics_workspace_id" {
  value       = azurerm_log_analytics_workspace.soc.id
  description = "Workspace resource ID. Use to configure approved connectors."
}
output "log_analytics_workspace_name" {
  value = azurerm_log_analytics_workspace.soc.name
}
output "sentinel_enabled" {
  value = var.enable_sentinel
}
output "deployed_analytics_rule_names" {
  value = keys(azurerm_sentinel_alert_rule_scheduled.detections)
}
