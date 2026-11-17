---
id: computing-software.cloud-infrastructure-engineering.azure.custom-role-update-versioning-and-safe-deletion
name: custom-role-update-versioning-and-safe-deletion
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, custom-roles, custom-role-update, role-definition-update, rbac-lifecycle, role-definition]
level: practitioner
status: docs-checked
description: "Change an in-use Azure custom role safely: diff and review, update by id, audit who is affected, and delete only after removing assignments."
sources: ["https://learn.microsoft.com/azure/role-based-access-control/custom-roles-cli", "https://learn.microsoft.com/azure/role-based-access-control/custom-roles-powershell", "https://learn.microsoft.com/azure/role-based-access-control/troubleshooting"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Update, version and delete custom roles safely

**Goal:** custom role changes are reviewed like code, applied atomically to every assignment,
and old roles disappear without leaving "Identity not found"/orphaned assignments.

## Key facts
- A role definition update applies **immediately to every assignment** of that role at every
  scope. Keep Git as your version history.
- The role is identified by its GUID (`name`), not `roleName`. Renaming is an update; the role ID does not change.
- Role changes can take up to 10 minutes to take effect.

## Update procedure
```bash
# 1. export current state
az role definition list --name "VM Operator" -o json | jq '.[0]' > current.json
# 2. edit the repo copy, then diff against live
diff <(jq -S '.permissions' current.json) <(jq -S '.permissions' vm-operator.json)
# 3. blast radius: who holds it
az role assignment list --all --role "VM Operator" --query "[].{who:principalName,scope:scope}" -o table
# 4. update (JSON must include the Id/name of the existing role)
az role definition update --role-definition @vm-operator.json
```
PowerShell:
```powershell
$r = Get-AzRoleDefinition "VM Operator"
$r.Actions.Add("Microsoft.Compute/virtualMachines/runCommand/action")
Set-AzRoleDefinition -Role $r
```
Bicep/Terraform: keep `name: guid(...)` deterministic so the deployment updates in place.

## Breaking vs non-breaking changes
| Change | Risk | Handling |
|---|---|---|
| Add Actions | Privilege grows for all holders | Security review; note in PR |
| Remove Actions | Breaks automation silently | Search Activity Log for that operation by holders over 30 days first |
| Add AssignableScope | Low | Needs write on the new scope |
| Remove AssignableScope | Assignments at that scope lose their role | List and remove those assignments first |
Activity-log check before removing an operation:
```kusto
AzureActivity | where TimeGenerated > ago(30d)
| where OperationNameValue =~ "Microsoft.Compute/virtualMachines/runCommand/action"
| summarize count() by Caller
```

## Delete
```bash
az role assignment list --all --role "Old Role" --query "[].id" -o tsv | xargs -r -n1 az role assignment delete --ids
az role definition delete --name "Old Role"
```
Deletion fails with *RoleDefinitionHasAssignments* while any assignment exists — including
ones at scopes you can't see; run the list as someone with read at the MG root.

## Gotchas
- `roleName` must be unique in the tenant, so two roles cannot share it; to "version" create `Role v2`, migrate assignments, then delete v1.
- Portal edits drift from Git; deny portal role writes to humans with a custom role lacking `roleDefinitions/write`.
- Removing a DataAction from a role used by a managed identity can break the app; monitor 403s after the change (propagation can take up to 10 minutes).

## Verify
- [ ] `az role definition list --name "<role>"` matches the repo JSON after update.
- [ ] No 403 spike in App Insights / Activity Log for holders within 1 hour of the change.
- [ ] Deleted roles return nothing from `az role definition list --name`.

## Checked
2026-10-28. Confirmed against Microsoft Learn custom-roles, custom-roles-cli, custom-roles-powershell, RBAC troubleshooting, the az role definition reference and the AzureActivity table page: `az role definition update --role-definition`, PowerShell `Get-AzRoleDefinition` and `.Actions.Add`, up to 10 minutes propagation, `RoleDefinitionHasAssignments` error on delete, roleName unique per tenant, role ID unchanged on rename, `OperationNameValue`. Fixed: the diff command compared mismatched JSON paths. Removed: the no-versioning absolute, and the unconfirmed token-refresh and remove-scope behaviour claims.
Method: documentation only; no commands were run.
