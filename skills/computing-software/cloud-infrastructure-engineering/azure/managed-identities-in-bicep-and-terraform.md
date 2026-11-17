---
id: computing-software.cloud-infrastructure-engineering.azure.managed-identities-in-bicep-and-terraform
name: managed-identities-in-bicep-and-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-identities, mi-bicep, identity-iac, user-assigned-identity, terraform, role-assignment]
level: practitioner
status: gated
description: "Declare system- and user-assigned managed identities in Bicep and Terraform, wire role assignments in the right order, and avoid first-start failures."
sources: ["https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities", "https://learn.microsoft.com/azure/templates/microsoft.managedidentity/userassignedidentities", "https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/user_assigned_identity"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed identities in Bicep and Terraform

**Goal:** the app has its identity and permissions before its first request, and redeploys are no-ops.

## Prefer user-assigned for IaC
A UAMI exists before the app, so you can grant roles first and the app starts healthy. System-assigned forces
"create app -> read principalId -> assign roles -> restart".

## Bicep
```bicep
resource uami 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-orders-prod'
  location: location
}
resource kvSecretsUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(kv.id, uami.id, '4633458b-17de-408a-b874-0445c86b69e6')
  scope: kv
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalId: uami.properties.principalId
    principalType: 'ServicePrincipal'
  }
}
resource app 'Microsoft.Web/sites@2023-12-01' = {
  name: appName
  location: location
  identity: { type: 'UserAssigned', userAssignedIdentities: { '${uami.id}': {} } }
  properties: {
    keyVaultReferenceIdentity: uami.id
    siteConfig: { appSettings: [ { name: 'AZURE_CLIENT_ID', value: uami.properties.clientId } ] }
  }
  dependsOn: [ kvSecretsUser ]
}
```
System-assigned: `identity: { type: 'SystemAssigned' }` and use `app.identity.principalId` in role assignments.

## Terraform
```hcl
resource "azurerm_user_assigned_identity" "orders" {
  name                = "id-orders-prod"
  location            = var.location
  resource_group_name = var.rg
}
resource "azurerm_linux_web_app" "app" {
  # ...
  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.orders.id]
  }
  key_vault_reference_identity_id = azurerm_user_assigned_identity.orders.id
  app_settings = { AZURE_CLIENT_ID = azurerm_user_assigned_identity.orders.client_id }
  depends_on   = [azurerm_role_assignment.kv_secrets_user]
}
```

## Gotchas
- With several UAMIs (or SAMI + UAMI), SDKs must be told which: set `AZURE_CLIENT_ID` / `ManagedIdentityCredential(clientId)`.
- Role assignments can take time to take effect, so first requests may fail with 403 (gated: unconfirmed, source is paywalled or blocked); build retries into startup or a post-deploy smoke test.
- Deleting and recreating a UAMI with the same name gives a **new principal ID**; old role assignments become
  "Identity not found" orphans. Treat UAMIs as long-lived, protect with a lock.
- Redeploying with a different identity `type` (for example `None`) changes or removes identities - watch module defaults.

## Verify
- [ ] what-if/plan is clean on second run; app smoke test reads its Key Vault secret on first boot.

## Checked
2026-10-28. The page set fetched for this skill covers only user-assigned identity management; role-assignment propagation delay, API versions in the Bicep samples (`roleAssignments@2022-04-01`, `sites@2023-12-01`) and Terraform arguments were not confirmed on a fetched page. Gated: those API versions and the propagation behaviour; use the current versions from the Bicep template reference.
Method: documentation only; no commands were run.
