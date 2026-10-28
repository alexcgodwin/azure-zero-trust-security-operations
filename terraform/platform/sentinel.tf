# Sentinel is deliberately OFF by default. Connectors, permissions and cost
# approvals must be established before enabling analytics rules.
resource "azurerm_sentinel_log_analytics_workspace_onboarding" "soc" {
  count        = var.enable_sentinel ? 1 : 0
  workspace_id = azurerm_log_analytics_workspace.soc.id
}

resource "azurerm_sentinel_alert_rule_scheduled" "detections" {
  for_each = var.enable_sentinel && var.enable_detection_rules ? local.rules : {}

  name                       = each.key
  log_analytics_workspace_id = azurerm_log_analytics_workspace.soc.id
  display_name               = each.value.display_name
  description                = each.value.description
  severity                   = each.value.severity
  query                      = file(format("%s/../../detections/queries/%s", path.module, each.value.query_file))
  query_frequency            = each.value.frequency
  query_period               = each.value.period
  trigger_operator           = "GreaterThan"
  trigger_threshold          = 0
  tactics                    = each.value.tactics
  enabled                    = each.value.enabled_by_default

  incident {
    create_incident_enabled = true
    grouping {
      enabled                 = true
      lookback_duration       = "PT1H"
      entity_matching_method  = "AllEntities"
      reopen_closed_incidents = false
    }
  }

  depends_on = [azurerm_sentinel_log_analytics_workspace_onboarding.soc]
}
