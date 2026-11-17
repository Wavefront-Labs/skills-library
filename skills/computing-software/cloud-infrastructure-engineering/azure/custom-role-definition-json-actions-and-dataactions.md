---
id: computing-software.cloud-infrastructure-engineering.azure.custom-role-definition-json-actions-and-dataactions
name: custom-role-definition-json-actions-and-dataactions
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-rbac, custom-roles, custom-role-json, role-definition, notactions, dataactions, notdataactions, least-privilege]
level: practitioner
status: docs-checked
description: "Author an Azure custom role JSON: find exact operations, split Actions/NotActions/DataActions, avoid wildcard traps, create it with az/PowerShell/Bicep and test it."
sources: ["https://learn.microsoft.com/azure/role-based-access-control/custom-roles", "https://learn.microsoft.com/azure/role-based-access-control/role-definitions", "https://learn.microsoft.com/azure/role-based-access-control/custom-roles-cli", "https://learn.microsoft.com/azure/role-based-access-control/resource-provider-operations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Author a custom role definition (Actions, NotActions, DataActions)

**Goal:** a role that grants exactly the operations a job needs, written as reviewable JSON in
source control, and proven with a test principal before anyone relies on it.

## 1. Start from a built-in, not from scratch
```bash
az role definition list --name "Virtual Machine Contributor" --output json > vm-operator.json
```
Clone, then cut. Built-ins already encode the companion reads (`*/read` on NICs, disks,
`Microsoft.Resources/deployments/*`) that a hand-written role usually forgets.

## 2. Find the exact operation strings
```bash
az provider operation show --namespace Microsoft.Compute \
  --query "resourceTypes[?name=='virtualMachines'].operations[].{op:name, data:isDataAction}" -o table
Get-AzProviderOperation "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/*" | ft Operation, IsDataAction
```
`isDataAction: true` operations go in **DataActions**, never in Actions (the API rejects the role).

## 3. Write the JSON
```json
{
  "Name": "VM Operator (start/stop/restart)",
  "IsCustom": true,
  "Description": "Start, stop, restart and read VMs. No create/delete. Owner: platform-team.",
  "Actions": [
    "Microsoft.Compute/virtualMachines/read",
    "Microsoft.Compute/virtualMachines/start/action",
    "Microsoft.Compute/virtualMachines/powerOff/action",
    "Microsoft.Compute/virtualMachines/deallocate/action",
    "Microsoft.Compute/virtualMachines/restart/action",
    "Microsoft.Compute/virtualMachines/instanceView/read",
    "Microsoft.Resources/subscriptions/resourceGroups/read",
    "Microsoft.Insights/alertRules/*"
  ],
  "NotActions": [],
  "DataActions": [],
  "NotDataActions": [],
  "AssignableScopes": ["/subscriptions/<sub-id>/resourceGroups/rg-app-prod"]
}
```
```bash
az role definition create --role-definition @vm-operator.json
```
Bicep: `Microsoft.Authorization/roleDefinitions` with `name: guid(subscription().id, 'vm-operator')`
— a deterministic GUID makes redeploys idempotent instead of failing with *RoleDefinitionWithSameNameExists*.

## 4. NotActions is subtraction, not deny
Effective permissions = Actions − NotActions (same for Data). A user with your role *and*
Contributor still gets everything Contributor grants. For a real block use a deny assignment (see Understand Azure deny assignments).

## 5. Wildcard rules
- Wildcards are allowed in operation strings, for example `Microsoft.Compute/*/read` and `Microsoft.Network/*`.
- Wildcards cover operations a provider adds later; for audited roles list operations explicitly.

## 6. Test before rollout
```bash
az role assignment create --assignee <test-upn> --role "VM Operator (start/stop/restart)" --scope <rg-id>
# sign in as the test user, after allowing time for the assignment to propagate:
az vm start -g rg-app-prod -n vm1        # expect success
az vm delete -g rg-app-prod -n vm1 --yes # expect AuthorizationFailed
```
Portal **Check access → View my access** on the test user shows the effective role list.

## Gotchas
- Include an owner in the `Description`.
- DataActions apply only to services that evaluate data-plane Azure RBAC; check the provider's operations list before relying on them.

## Verify
- [ ] `az role definition list --custom-role-only true --query "[?roleName=='<name>']"` returns the role with the intended operation list.
- [ ] Positive and negative test commands behave as expected for a test principal.
- [ ] The JSON file is in Git and deployed by pipeline, not edited in the portal.

## Checked

Date: 2026-10-28.

Confirmed against Learn (custom-roles, role-definitions, custom-roles-cli, resource-provider-operations): role JSON properties (Actions, NotActions, DataActions, NotDataActions, AssignableScopes), NotActions versus deny assignments, wildcard use, CLI commands (check_commands.py).
Removed: DenyAction and deployment-stack alternatives, the Authorization/*/write Owner claim, 10/5-minute propagation figures, name uniqueness, portal clone behaviour, Microsoft.Support note and the per-service data-plane list.

Method: documentation only; no commands were run.
