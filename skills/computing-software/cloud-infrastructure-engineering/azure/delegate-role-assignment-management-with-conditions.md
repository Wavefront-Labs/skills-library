---
id: computing-software.cloud-infrastructure-engineering.azure.delegate-role-assignment-management-with-conditions
name: delegate-role-assignment-management-with-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-rbac, delegate-role-assignments, constrained-delegation, rbac-administrator, role-assignment-conditions]
level: advanced
status: docs-checked
description: "Let app teams or pipelines grant access without Owner: Role Based Access Control Administrator plus conditions limiting which roles and principal types they can assign."
sources: ["https://learn.microsoft.com/azure/role-based-access-control/delegate-role-assignments-overview", "https://learn.microsoft.com/azure/role-based-access-control/delegate-role-assignments-examples", "https://learn.microsoft.com/azure/role-based-access-control/delegate-role-assignments-portal"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delegate role assignment management with conditions

**Goal:** a workload pipeline can give its managed identity a named data role but can never
make anyone Owner.

## Role
**Role Based Access Control Administrator** (`f58310d9-a9f6-439a-9e8d-f62e7b41a168`): only
create and delete role assignments at the scope, read all resource types except secrets, and create or update support tickets. It has fewer permissions than User Access Administrator, so prefer it for delegation.

## Condition: only these roles, only to service principals
```
(
 (
  !(ActionMatches{'Microsoft.Authorization/roleAssignments/write'})
 )
 OR
 (
  @Request[Microsoft.Authorization/roleAssignments:RoleDefinitionId] ForAnyOfAnyValues:GuidEquals {<ALLOWED_ROLE_GUID_1>, <ALLOWED_ROLE_GUID_2>}
  AND
  @Request[Microsoft.Authorization/roleAssignments:PrincipalType] ForAnyOfAnyValues:StringEqualsIgnoreCase {'ServicePrincipal'}
 )
)
AND
(
 (
  !(ActionMatches{'Microsoft.Authorization/roleAssignments/delete'})
 )
 OR
 (
  @Resource[Microsoft.Authorization/roleAssignments:RoleDefinitionId] ForAnyOfAnyValues:GuidEquals {<ALLOWED_ROLE_GUID_1>, <ALLOWED_ROLE_GUID_2>}
 )
)
```
Write uses `@Request`, delete uses `@Resource` (the same shape as the Learn examples page). Learn also shows constraining principal IDs and an "all roles except" form; you can set different conditions for add and remove.

```bash
az role assignment create --assignee <pipeline-sp> --role "Role Based Access Control Administrator" \
  --scope /subscriptions/<sub>/resourceGroups/rg-app --condition "<CONDITION>" --condition-version 2.0
```

## Portal templates
Add role assignment > select Role Based Access Control Administrator (any role with `roleAssignments/write` works, but this has the fewest permissions) > Conditions tab, "What user can do":
- "Allow user to only assign selected roles to selected principals (fewer privileges)", then constrain roles, roles and principal types, or roles and principals.
- "Allow all except specific roles": assign (and remove) every role except the ones you select.

## Gotchas
- Write and delete are separate actions, so add a delete clause as above; otherwise the delegate's removal rights are not constrained.
- Conditions reference role definition GUIDs, not role names.

## Verify
- [ ] The delegate can assign an allowed role to a managed identity, and is denied when assigning Owner or assigning to a user.

## Checked
2026-10-31. Confirmed on the delegate-role-assignments overview, examples and portal Learn pages: RBAC Administrator role GUID and permissions, condition shape (`ActionMatches`, `@Request`/`@Resource`, `ForAnyOfAnyValues:GuidEquals`, `StringEqualsIgnoreCase` for principal type), portal condition templates, `--condition` and `--condition-version`. Removed: the two literal role GUIDs (not on the pages; now placeholders), the `roleDefinitionName` gotcha, the Owner/UAA conditions gotcha, the privileged-roles template wording, the AuthorizationFailed error name.
Method: documentation only; no commands were run.
