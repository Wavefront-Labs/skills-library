---
id: computing-software.cloud-infrastructure-engineering.azure.resource-move-across-groups-and-subscriptions
name: resource-move-across-groups-and-subscriptions
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, resource-move, move-resources, move-validation, resource-groups, subscription-move, azure-resource-mover]
level: practitioner
status: docs-checked
description: "Move Azure resources between resource groups and subscriptions: validate first, move dependent resources together, handle locks, RBAC and service-specific limits."
sources: ["https://learn.microsoft.com/azure/azure-resource-manager/management/move-resource-group-and-subscription", "https://learn.microsoft.com/azure/azure-resource-manager/management/move-support-resources", "https://learn.microsoft.com/azure/azure-resource-manager/management/move-limitations/virtual-machines-move-limitations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Move resources across resource groups and subscriptions

**Goal:** a move that validates cleanly, carries every dependent resource, and leaves RBAC,
policy and monitoring in a known state.

## Facts to know before starting
- Moves change the **resource ID**; anything referencing the ID (diagnostic settings,
  alerts, Key Vault access, scripts, Terraform state) breaks.
- Both source and target RGs are **locked for writes** during the move (up to 4 hours).
- Re-check RBAC and policy after the move; the target's policies and role assignments apply to the moved resources.
- Cross-subscription moves require same Entra tenant; across tenants needs redeploy (or subscription transfer).
- Region does not change. For region moves use Azure Resource Mover or redeploy.

## 1. Check support and dependencies
Consult the *move support* table per resource type (columns: resource group, subscription, region) and the service-specific guidance it links (virtual machines, App Service, networking). Read the MoveCannotProceedWithResourcesNotInSucceededState section of the move article if a dependent resource blocks the move; some types (for example `addsservices`) are not movable at all.

## 2. Validate (no change made)
```bash
az resource invoke-action --action validateMoveResources \
  --ids /subscriptions/<src>/resourceGroups/rg-src \
  --request-body '{"resources":["<id1>","<id2>"],"targetResourceGroup":"/subscriptions/<dst>/resourceGroups/rg-dst"}'
```
Returns 202 + a Location URL; poll it (honour retry-after) — 204 means valid; a failure returns an error message.
PowerShell: `Invoke-AzResourceAction -Action validateMoveResources ...`. Portal runs the same validation.

## 3. Prepare
- Register the resource providers in the target subscription (`az provider register -n Microsoft.Compute`).
- Remove read-only locks on the source and destination resource groups or subscriptions (they block the move).
- Need `Microsoft.Resources/subscriptions/resourceGroups/moveResources/action` on source RG and write on target.
- Quotas in the target subscription must accommodate the resources.

## 4. Move
```bash
az resource move --destination-group rg-dst --destination-subscription-id <dst> --ids <id1> <id2>
```

## 5. After
- Recreate RBAC assignments, re-point diagnostic settings/alerts, update IaC (`terraform state mv` or import), re-apply locks.
- Re-enable backup (new protection under the target vault if subscription changed).

## Gotchas
- Validation passing does not guarantee success for long-running service-specific steps; schedule a window.
- Key Vaults used to encrypt disks can't be moved (see the move support page).

## Verify
- [ ] `az resource show --ids <new-id>` returns; old ID 404s.
- [ ] Role assignments and diagnostic settings re-created (`az monitor diagnostic-settings list --resource <new-id>`).
- [ ] IaC plan shows no changes against the new location.

## Checked
2026-10-28. Confirmed against Microsoft Learn move-resource-group-and-subscription and move-support-resources: validateMoveResources via `az resource invoke-action` returns 202 then 204 on success, four-hour lock on both resource groups, read-only locks block moves, same Entra tenant required, moveResources/action permission on the source group, Azure Resource Mover for region changes, `addsservices` not movable, disk-encryption Key Vaults not movable. Removed: the per-service VM/VNet/App Service rules, RBAC deletion claim, 409 detail, and managed identity and Key Vault tenant claims (not found in the pages).
Method: documentation only; no commands were run.
