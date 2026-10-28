output "client_id" {
  value       = azurerm_user_assigned_identity.github.client_id
  description = "Use with azure/login OIDC, not a client secret."
}
output "principal_id" {
  value       = azurerm_user_assigned_identity.github.principal_id
  description = "Principal to grant reviewed, narrowly-scoped Azure RBAC roles."
}
output "federated_subject" {
  value = azurerm_federated_identity_credential.github_environment.subject
}
