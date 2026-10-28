# Subscription Activity Logs are independent of Sentinel data connectors.
# This setting changes subscription-wide diagnostics. Keep opt-in.
resource "azurerm_monitor_diagnostic_setting" "subscription_activity" {
  count                      = var.enable_subscription_diagnostics ? 1 : 0
  name                       = format("diag-%s-sub-activity", local.suffix)
  target_resource_id         = format("/subscriptions/%s", var.subscription_id)
  log_analytics_workspace_id = azurerm_log_analytics_workspace.soc.id

  dynamic "enabled_log" {
    for_each = toset(["Administrative", "Security", "Policy", "ServiceHealth"])
    content {
      category = enabled_log.value
    }
  }
}
