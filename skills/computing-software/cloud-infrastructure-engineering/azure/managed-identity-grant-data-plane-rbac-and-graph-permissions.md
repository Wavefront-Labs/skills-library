---
id: computing-software.cloud-infrastructure-engineering.azure.managed-identity-grant-data-plane-rbac-and-graph-permissions
name: managed-identity-grant-data-plane-rbac-and-graph-permissions
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-identity, mi-grant, mi-rbac, graph-permissions-mi, app-role-assignment, sql-contained-user]
level: practitioner
status: docs-checked
description: "Grant a managed identity what it needs: data-plane RBAC roles, Microsoft Graph application permissions via appRoleAssignments, and database users for Azure SQL."
sources: ["https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/manage-user-assigned-managed-identities-azure-portal", "https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/assign-app-role-managed-identity-azure-cli", "https://learn.microsoft.com/en-us/azure/azure-sql/database/authentication-azure-ad-user-assigned-managed-identity"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grant a managed identity data-plane RBAC and Graph permissions

**Goal:** the identity has the minimum data access at the narrowest scope, using the mechanism
each target actually honours.

## Which mechanism for which target
| Target | Mechanism |
|---|---|
| Storage, Key Vault (RBAC mode), Service Bus, Event Hubs, App Config | Azure RBAC data role on the resource/container |
| Cosmos DB (NoSQL) | Cosmos native SQL role assignment (`az cosmosdb sql role assignment create`) |
| Azure SQL / MI | Contained database user `FROM EXTERNAL PROVIDER` |
| Microsoft Graph | App role assignment (application permission) |
| Your own API | App role assignment to your app registration's role |

## Azure RBAC
```bash
pid=$(az identity show -n id-orders-prd -g rg-orders --query principalId -o tsv)
az role assignment create --assignee-object-id $pid --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Reader" \
  --scope "/subscriptions/<sub>/resourceGroups/rg-data/providers/Microsoft.Storage/storageAccounts/stdata/blobServices/default/containers/orders"
```
Scope to the narrowest resource that supports it.

## Microsoft Graph application permission
Assign the Graph app role to the identity's service principal directly (Microsoft's script uses the Graph PowerShell SDK):
```powershell
Connect-MgGraph -Scopes "AppRoleAssignment.ReadWrite.All","Application.Read.All"
$mi    = Get-MgServicePrincipal -Filter "displayName eq 'id-orders-prd'"
$graph = Get-MgServicePrincipal -Filter "appId eq '00000003-0000-0000-c000-000000000000'"
$role  = $graph.AppRoles | ? { $_.Value -eq "User.Read.All" -and $_.AllowedMemberTypes -contains "Application" }
New-MgServicePrincipalAppRoleAssignment -ServicePrincipalId $mi.Id -PrincipalId $mi.Id -ResourceId $graph.Id -AppRoleId $role.Id
```
Microsoft's script requires signing in as a Privileged Role Administrator or higher. Graph application
permissions are tenant-wide, so grant the narrowest permission that works.

## Azure SQL
```sql
-- run as the Entra admin of the server, in the user database
CREATE USER [id-orders-prd] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [id-orders-prd];
ALTER ROLE db_datawriter ADD MEMBER [id-orders-prd];
```
The server identity needs either the Directory Readers role or lower-level Microsoft Graph permissions to resolve Entra names; only a Privileged Role Administrator or higher can grant them.

## Gotchas
- Pass `--assignee-object-id` with `--assignee-principal-type` when scripting role assignments for a brand-new identity.
- Managed identity tokens are cached by the infrastructure, so role changes can take significant time to show up.
- `CREATE USER ... FROM EXTERNAL PROVIDER` accepts `WITH OBJECT_ID = '<oid>'`; use it when display names are ambiguous.

## Verify
- [ ] `az role assignment list --assignee $pid --all -o table` lists only intended scopes.
- [ ] `Get-MgServicePrincipalAppRoleAssignment -ServicePrincipalId $mi.Id` shows the Graph role.
- [ ] App call succeeds; same call with a different identity fails 403.

## Checked
2026-10-28. Confirmed on Microsoft Learn (assign app role to a managed identity, Azure SQL Entra managed identity pages): Graph SDK scopes `AppRoleAssignment.ReadWrite.All` and `Application.Read.All`, Microsoft Graph appId `00000003-0000-0000-c000-000000000000`, `appRoleAssignments` POST, Privileged Role Administrator requirement, Directory Readers or lower-level Graph permissions for the SQL server identity, `CREATE USER ... FROM EXTERNAL PROVIDER` with `OBJECT_ID`, token caching delay. `az role assignment` and `az cosmosdb sql role assignment` commands passed check_commands. Removed: PostgreSQL function, Sites.Selected/Mail.Send advice, Key Vault RBAC-mode and 24-hour cache claims.
Method: documentation only; no commands were run.
