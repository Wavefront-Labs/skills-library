---
id: computing-software.cloud-infrastructure-engineering.azure.role-assignments-in-bicep-and-terraform
name: role-assignments-in-bicep-and-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-rbac, role-assignment-bicep, principal-type, role-assignment-guid, terraform, roleassignmentexists]
level: practitioner
status: docs-checked
description: "Declare Azure role assignments in Bicep: deterministic names, principalType, resource scope, built-in role IDs and RoleAssignmentExists fixes."
sources: ["https://learn.microsoft.com/azure/role-based-access-control/role-assignments-template", "https://learn.microsoft.com/azure/azure-resource-manager/bicep/scenarios-rbac"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Role assignments in Bicep

**Goal:** idempotent RBAC in IaC that does not fail on redeploy or on brand-new identities. (Terraform `azurerm_role_assignment` details were not verifiable here: the Terraform registry cannot be read. Check its docs directly.)

## Bicep pattern
```bicep
param principalId string
param roleDefinitionResourceId string

resource sa 'Microsoft.Storage/storageAccounts@2025-06-01' existing = { name: storageName }

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: sa
  name: getRoleAssignmentName({
    scope: sa.id
    principalId: principalId
    roleDefinitionId: roleDefinitionResourceId
  })
  properties: {
    roleDefinitionId: roleDefinitionResourceId
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
```
- A role assignment is an extension resource; `scope:` points it at another resource. With no `scope`, Bicep uses the file's `targetScope`. Use the smallest scope that meets the need.
- The name must be a GUID, unique within the Entra tenant even when the scope is narrower. Make it deterministic. For new assignments Microsoft recommends `getRoleAssignmentName()`, which builds a GUID from scope, principal ID and fully qualified role definition ID (normalises casing, strips a trailing slash, uses only the role definition GUID). Pass the Entra object ID as principalId, not a resource ID.
- When the principal ID is not known at the start of the deployment (a managed identity created in the same file), Microsoft's example keeps `guid(resourceGroup().id, managedIdentity.id, roleDefinitionResourceId)` for the name, or create the assignment in a module and pass `managedIdentity.properties.principalId` as a parameter.
- Reference a built-in role through an existing resource and use its `.id`: `resource r 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = { scope: subscription() name: '<role GUID>' }`.
- `principalId` is the Entra object ID; `principalType` is user, group or service principal (managed identities are service principals). Always set `principalType`: otherwise you may get intermittent deployment errors, especially with service principals and managed identities.

## Built-in role IDs confirmed on Microsoft's pages
Owner `8e3af657-a8ff-443c-a75c-2fe8c4bcb635`, Contributor `b24988ac-6180-42a0-ab88-20f7382dd24c`, Reader `acdd72a7-3385-48ef-bd42-f606fba81ae7`. Look up others in the built-in roles reference.

## Errors
- **RoleAssignmentExists**: the same assignment already exists under a different name, or a template generated a new GUID each run. Switching from `guid()` or another naming convention to `getRoleAssignmentName()` can produce a different name for the same assignment: delete the old assignment before deploying its replacement.
- Deleting a principal from Entra does not delete its role assignments; they become invalid. Reusing an assignment name then fails: remove the old assignment or use a unique name.
- The deploying identity needs `Microsoft.Authorization/roleAssignments/write`, for example Role Based Access Control Administrator or User Access Administrator.
- Some services keep their own role resources (Azure Cosmos DB has `sqlRoleAssignments`).

## Verify
- [ ] Redeploying is a no-op; `az deployment ... what-if` shows no change for the assignment.

## Checked

Method: docs-checked 2026-11-09 against the Learn pages scenarios-rbac (read in full) and role-assignments-template (keyword checks). Removed the Terraform section and registry source (unreadable host), the Storage/Key Vault/AcrPull GUIDs, `PrincipalNotFound`, the `az role definition list` lookup and the group/user type gotchas that were not on the pages.
