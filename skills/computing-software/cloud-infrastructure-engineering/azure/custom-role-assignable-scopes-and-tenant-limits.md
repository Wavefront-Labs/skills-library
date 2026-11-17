---
id: computing-software.cloud-infrastructure-engineering.azure.custom-role-assignable-scopes-and-tenant-limits
name: custom-role-assignable-scopes-and-tenant-limits
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, custom-roles, assignable-scopes, custom-role-limits, management-groups, role-definition]
level: practitioner
status: docs-checked
description: "Choose AssignableScopes for Azure custom roles (subscription vs management group), stay under the 5,000 custom roles per tenant limit and avoid scope-related failures."
sources: ["https://learn.microsoft.com/azure/role-based-access-control/custom-roles", "https://learn.microsoft.com/azure/role-based-access-control/troubleshoot-limits", "https://learn.microsoft.com/azure/azure-resource-manager/management/azure-subscription-service-limits#azure-rbac-limits"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom role assignable scopes and tenant limits

**Goal:** each custom role is defined once, at the highest scope that needs it, so it is
assignable everywhere it should be and nowhere else, and the tenant never hits the role limit.

## AssignableScopes rules
| Scope in `AssignableScopes` | Effect |
|---|---|
| `/subscriptions/<id>` | Assignable in that subscription and its RGs/resources |
| `/subscriptions/<id>/resourceGroups/<rg>` | Only in that RG |
| `/providers/Microsoft.Management/managementGroups/<mg>` | Assignable in every subscription under the MG |
| `/` (root) | Not allowed for custom roles (only built-ins) |

- **Only one management group** may appear in `AssignableScopes` of a role; you can still list
  several subscriptions.
- A custom role with **DataActions cannot be assigned at management group scope**. It may still list one management group in `AssignableScopes` and be assigned at the subscriptions under it.
- To create or update a role you need `Microsoft.Authorization/roleDefinitions/write` on
  **every** scope listed (Owner or User Access Administrator there).

## Recommended layout
- Platform roles (e.g. *Network Operator*, *Landing Zone Reader+*): define once at the
  intermediate root MG (`mg-contoso`) so every landing-zone subscription can use them.
- Workload-specific roles: define at the workload subscription.
- Keep the JSON in the platform repo; deploy with a `targetScope = 'managementGroup'` Bicep file.
```bicep
targetScope = 'managementGroup'
resource role 'Microsoft.Authorization/roleDefinitions@2022-04-01' = {
  name: guid(managementGroup().id, 'network-operator')
  properties: {
    roleName: 'Network Operator'
    description: 'Manage NSG rules and route tables. Owner: platform-network.'
    permissions: [ { actions: [ 'Microsoft.Network/networkSecurityGroups/*', 'Microsoft.Network/routeTables/*', 'Microsoft.Network/*/read' ], notActions: [] } ]
    assignableScopes: [ managementGroup().id ]
  }
}
```

## Limits that bite
| Limit | Value |
|---|---|
| Custom roles per tenant | 5,000 (2,000 for Microsoft Azure operated by 21Vianet) |
| Role assignments per subscription | 5,000 |
| Role assignments per management group | 500 |
Count custom roles:
```bash
az role definition list --custom-role-only true --query "length(@)"
```
Hitting the limit usually means a pipeline creates a role per app; consolidate by moving the
role up to an MG and parameterising scope at assignment time instead.

## Changing scopes later
- Adding a scope: update the definition (need write on new scope).
- Removing a scope: list assignments at that scope first (`az role assignment list --role <name> --all`) and remove them.

## Verify
- [ ] `az role definition list --name "<role>" --query "[].assignableScopes"` shows the intended scopes.
- [ ] The role appears in the Add role assignment picker in a subscription under the MG.
- [ ] Custom role count is tracked against the 5,000 limit in the platform dashboard.

## Checked
2026-10-28. Confirmed against Microsoft Learn custom-roles, RBAC troubleshooting and Azure subscription limits (RBAC section) pages: 5,000 custom roles per tenant (2,000 for 21Vianet), root `/` not allowed, one management group per role, DataActions cannot be assigned at management group scope, roleDefinitions/write needed on assignable scopes, 5,000 assignments per subscription and 500 per management group, `--custom-role-only`. Fixed: the subscription assignment limit (was 4,000) and the DataActions rule (a role may list a management group but cannot be assigned at it). Removed: the unconfirmed claim about moving subscriptions between management groups.
Method: documentation only; no commands were run.
