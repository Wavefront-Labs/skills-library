---
id: computing-software.cloud-infrastructure-engineering.azure.rbac-troubleshooting-limits-propagation-and-orphans
name: rbac-troubleshooting-limits-propagation-and-orphans
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-rbac, troubleshooting, role-assignment-limits, propagation, orphaned-assignments, unknown-principal, principal-type, authorization-failed, custom-roles]
level: practitioner
status: docs-checked
description: "Diagnose Azure RBAC failures: PrincipalNotFound, RoleAssignmentUpdateNotPermitted, propagation delay, orphaned assignments, limits and custom-role scope rules."
sources: ["https://learn.microsoft.com/en-us/azure/role-based-access-control/troubleshooting", "https://learn.microsoft.com/en-us/azure/role-based-access-control/troubleshoot-limits"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure RBAC troubleshooting — decode the error, then fix the actual cause

**Goal:** turn "I have Contributor but it says forbidden" into a short diagnosis.

## 1. Read the error
| Error or symptom | Meaning | Fix |
|---|---|---|
| `AuthorizationFailed` ("does not have authorization to perform action X over scope Y") | Principal lacks the action at that scope, or the scope is wrong | Check the exact action against the role's permissions at or above that scope; for guests, confirm a least-privileged role is assigned at the scope |
| `PrincipalNotFound` when assigning to a new user or service principal | Replication delay for a just-created principal | Set `principalType` on the role assignment (REST or ARM/Bicep) so the lookup is skipped, or retry later |
| `RoleAssignmentUpdateNotPermitted` (tenant ID, application ID, principal ID and scope cannot be updated) | A template redeploys an assignment with the same name but different principal or scope | Make the name idempotent and unique, for example `guid(resourceGroup().id, principalId, roleDefinitionId)` |
| Cannot delete the last Owner | Last Owner (or User Access Administrator) at subscription scope | A Global Administrator can remove it after elevating access; PIM-eligible owners can activate first (see the page) |

## 2. "I was just granted access and it still fails"
Role assignment changes can take up to 10 minutes to take effect, including changes at
management group scope and child management group assignments. In PowerShell, role-assignment
listings are cached, so a removed assignment can keep showing for 5-10 minutes.

## 3. Orphans and limits
An assignment whose user, group, service principal or managed identity was deleted shows as
*Identity not found*; `az role assignment list` returns an empty `principalName`, and
PowerShell shows an empty DisplayName or ObjectType Unknown. Remove these:
```bash
az role assignment list --all --query "[?principalName==''].{id:id,principalId:principalId,scope:scope}" -o table
az role assignment delete --ids <ASSIGNMENT_ID>
```
Limits (see the limits page): 5000 role assignments per subscription (not counting management
group scope; fixed) and 500 per management group.
If the same principal has several assignments, PowerShell removal by object ID and role name
may fail until you also give the `-Scope`.

## 4. Custom roles
- Only one management group may be in `AssignableScopes`.
- A custom role with `DataActions` cannot use a management group as assignable scope; use subscriptions.
- A custom role cannot be deleted until its role assignments are removed.

## Gotchas
- Moving a resource does not move role assignments made directly on it; recreate them (orphans are eventually removed automatically).
- Transferring a subscription to another directory deletes its role assignments (see the transfer page).
- Guest users get `AuthorizationFailed` until a role is assigned at the scope.

## Verify
- [ ] The failing action appears in a role the principal holds at or above the scope.
- [ ] After the wait (up to 10 minutes) the operation succeeds.
- [ ] No role assignments with empty `principalName` remain.

## Checked
2026-10-28. Confirmed on the Learn pages "Troubleshoot Azure RBAC" and "Troubleshoot Azure RBAC limits": error names and fixes, principalType, guid naming, last Owner, move behaviour, 10-minute propagation, PowerShell cache, orphan symptoms, custom-role scope rules, limits. Corrected: 4000 per subscription is 5000; resource moves keep direct assignments is wrong (they are not moved). Removed (not on those pages): `LinkedAuthorizationFailed`, token-caching and IMDS claims, data-plane (Storage, Key Vault, SQL, AKS) tables, RBAC Administrator ABAC advice, 5000-custom-roles figure, `#EXT#` and classic-admin flags.
Method: documentation only; no commands were run.
