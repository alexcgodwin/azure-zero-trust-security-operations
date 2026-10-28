variable "subscription_id" {
  type        = string
  description = "Target Azure subscription ID. Passed explicitly; never embed credentials."
}
variable "location" {
  type        = string
  description = "Approved Azure region for the SOC workspace."
  default     = "canadacentral"
}
variable "name_prefix" {
  type        = string
  description = "Lowercase short identifier; must be unique per environment."
  default     = "ztsec"
  validation {
    condition     = can(regex("^[a-z][a-z0-9]{2,11}$", var.name_prefix))
    error_message = "Use 3-12 lowercase alphanumeric characters starting with a letter."
  }
}
variable "environment" {
  type    = string
  default = "dev"
  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "environment must be dev, test or prod."
  }
}
variable "workspace_retention_days" {
  type        = number
  default     = 30
  description = "Log Analytics retention; higher values may incur additional costs."
  validation {
    condition     = var.workspace_retention_days >= 30 && var.workspace_retention_days <= 730
    error_message = "Retention must be between 30 and 730 days."
  }
}
variable "daily_quota_gb" {
  type        = number
  default     = 1
  description = "Workspace daily ingestion cap in GB. Not a hard cost budget."
}
variable "enable_sentinel" {
  type        = bool
  default     = false
  description = "Opt in to Microsoft Sentinel onboarding (potentially billable)."
}
variable "enable_detection_rules" {
  type        = bool
  default     = false
  description = "Enable scheduled analytics only AFTER relevant data connectors are configured."
}
variable "enable_subscription_diagnostics" {
  type        = bool
  default     = false
  description = "Subscription-scope activity log routing; requires elevated permissions."
}
variable "enable_defender_plans" {
  type        = bool
  default     = false
  description = "Subscription-wide Defender plans can generate material charges."
}
variable "enable_governance_policy" {
  type        = bool
  default     = false
  description = "Add an Audit-only storage public access custom policy for the SOC resource group."
}
variable "tags" {
  type = map(string)
  default = {
    managed_by  = "terraform"
    cost_center = "platform-security"
    data_class  = "security"
  }
}
