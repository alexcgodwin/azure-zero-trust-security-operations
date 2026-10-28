variable "subscription_id" {
  type = string
}
variable "location" {
  type    = string
  default = "canadacentral"
}
variable "resource_group_name" {
  description = "Existing resource group from platform stack."
  type        = string
}
variable "github_owner" {
  description = "Exact case-sensitive GitHub owner login."
  type        = string
  default     = "alexcgodwin"
}
variable "github_repository" {
  description = "Exact GitHub repository name."
  type        = string
  default     = "azure-zero-trust-security-operations"
}
variable "github_environment" {
  description = "Protected GitHub environment: requires approvals and deployment restrictions."
  type        = string
  default     = "production"
}
