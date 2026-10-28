# Federated identity avoids long-lived AZURE_CLIENT_SECRET in Actions.
# Trust is scoped to a single repository + protected GitHub environment.
# The role assignment is intentionally NOT automatic. Grant only the
# permissions needed, on the smallest appropriate scope, after review.
resource "azurerm_user_assigned_identity" "github" {
  name                = format("id-%s-%s-security-deploy", var.github_repository, var.github_environment)
  location            = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_federated_identity_credential" "github_environment" {
  name                = format("fic-%s", var.github_environment)
  resource_group_name = var.resource_group_name
  parent_id           = azurerm_user_assigned_identity.github.id
  issuer              = "https://token.actions.githubusercontent.com"
  subject             = format("repo:%s/%s:environment:%s", var.github_owner, var.github_repository, var.github_environment)
  audience            = ["api://AzureADTokenExchange"]
}
