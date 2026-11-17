---
id: computing-software.cloud-infrastructure-engineering.azure.discover-provider-operations-for-custom-roles
name: discover-provider-operations-for-custom-roles
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, custom-roles, provider-operations, permission-discovery, least-privilege]
level: practitioner
status: docs-checked
description: "Find the Azure RBAC actions and dataActions a custom role needs: provider operation listings, built-in roles as a start, wildcard caution and custom role limits."
sources: ["https://learn.microsoft.com/azure/role-based-access-control/resource-provider-operations", "https://learn.microsoft.com/cli/azure/provider/operation", "https://learn.microsoft.com/azure/role-based-access-control/custom-roles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Discover provider operations for custom roles

**Goal:** build a custom role from the actual operations a task needs, not by guessing.

## Find the permissions
The custom roles page suggests: look at existing built-in roles (you typically start with one and modify it), list the Azure services you need, map them to resource providers (for example `Microsoft.Compute` supplies virtual machine resources and `Microsoft.Billing` supplies subscription and billing resources), then search the available permissions. The portal custom role editor can search by keyword and download all permissions as a CSV.

Operations come from:
- The "Azure permissions" reference page, which lists permissions per resource provider. It says permissions are always evolving and points to `Get-AzProviderOperation` or `az provider operation list` for the latest.
- `az provider operation list` (all providers) and `az provider operation show --namespace Microsoft.Storage` (one provider).

## Role definition shape
Properties: `Name`/`roleName`, `Id`, `IsCustom`/`roleType`, `Description`, `Actions` (control plane), `NotActions`, `DataActions` (data plane), `NotDataActions`, `AssignableScopes`. Permission strings are case-insensitive; match the case shown in the provider operations. When scripting, use the role ID rather than the name, since renaming does not change the ID.

## Gotchas and limits
- Wildcards are supported, but Microsoft recommends listing Actions and DataActions explicitly, because a wildcard also picks up future operations. Only one wildcard is allowed per action string.
- A role with `DataActions` cannot be assigned at management group scope. It can have one management group in `AssignableScopes` and be assigned at subscriptions inside it.
- `AssignableScopes`: not the root scope `/`, no wildcards, at most one management group, maximum 2,000 entries.
- Limit of 5,000 custom roles per tenant (2,000 for Azure operated by 21Vianet).
- Name must be unique in the tenant (recommended maximum 256 characters, maximum 512); description recommended maximum 512, maximum 2,048.
- Creating, updating or deleting a role needs `Microsoft.Authorization/roleDefinitions/write` on all of its AssignableScopes; viewing needs `.../roleDefinitions/read`.
- Deleting a role with assignments fails with `RoleDefinitionHasAssignments`; remove assignments (including eligible PIM assignments) first.

## Verify
Test a principal holding the custom role against the end-to-end task and confirm nothing broader is possible.

## Checked
Confirmed against the "Azure custom roles" page (last updated 2025-10-23), the "Azure permissions" reference intro and `az provider operation` CLI reference, 2026-11-08. Removed: JMESPath queries and the `isDataAction` field, specific linked-action examples, the KQL activity-log query, `az role definition list` diffs and the portal-blade read advice, because the pages do not state them.
Method: docs-only read of cited pages, 2026-11-08
