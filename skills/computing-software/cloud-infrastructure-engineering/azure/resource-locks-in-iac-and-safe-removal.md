---
id: computing-software.cloud-infrastructure-engineering.azure.resource-locks-in-iac-and-safe-removal
name: resource-locks-in-iac-and-safe-removal
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, resource-locks, lock-bicep, remove-lock, lock-permissions, cannotdelete]
level: practitioner
status: docs-checked
description: "Declare CanNotDelete/ReadOnly locks in Bicep, control who can remove them, and run a break-glass lock removal with an audit trail."
sources: ["https://learn.microsoft.com/azure/azure-resource-manager/management/lock-resources", "https://learn.microsoft.com/azure/templates/microsoft.authorization/locks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource locks in IaC and safe removal

**Goal:** critical resources (hub VNet, Key Vault, log workspace, DNS zones) survive a fat-fingered delete, and
removing the protection is a deliberate, logged act.

## Bicep
```bicep
resource kv 'Microsoft.KeyVault/vaults@<API_VERSION>' existing = { name: kvName }
resource kvLock 'Microsoft.Authorization/locks@2020-05-01' = {
  name: 'lock-nodelete'
  scope: kv
  properties: { level: 'CanNotDelete', notes: 'Holds CMK keys for prod storage. Change via CAB only.' }
}
```
Resource-group scope: deploy the lock in an RG-scoped module without `scope`.

A lock on a parent scope is inherited by every resource under it, including ones added later; the most restrictive lock in the chain wins. Extension resources (for example diagnostic settings) inherit the lock of their parent resource. In the portal the lock types are called Delete and Read-only; in the CLI CanNotDelete and ReadOnly.

## Who can remove a lock
Creating or deleting a lock needs access to `Microsoft.Authorization/*` or `Microsoft.Authorization/locks/*`. Owner and User Access Administrator have it, as do some specialised built-in roles; you can also write a custom role. Grant it to pipeline identities only where justified.

## Break-glass removal
```bash
az lock list --resource-group rg-hub -o table
az lock delete --name lock-nodelete --resource-group rg-hub            # or --ids <lock-id>
# ...perform the change...
az lock create --name lock-nodelete --resource-group rg-hub --lock-type CanNotDelete --notes "restored after CHG-1234"
```
Activate a role that can delete locks through PIM with justification first, and alert on lock deletions in the activity log.

## Gotchas
- Locks block the POST method to the Resource Manager API, so a ReadOnly lock breaks operations that look like reads: starting or restarting a VM, starting Automation runbooks, Application Gateway backend health. Prefer CanNotDelete.
- Locks apply to the management plane only; data-plane operations (for example data in a SQL database) are unaffected.
- Deployment stacks' deny settings (`DenySettingsMode`: None, DenyDelete, DenyWriteAndDelete) are an alternative for IaC-managed estates.

## Verify
- [ ] `az lock list` shows locks on all tier-0 resources; a test delete is refused.

## Checked
2026-10-31. Confirmed on the lock-resources, Microsoft.Authorization/locks template and deployment-stacks Learn pages: lock type names, `Microsoft.Authorization/locks@2020-05-01`, inheritance, permission requirement and roles, POST-method side effects, management-plane scope, `DenySettingsMode` values, `az lock list/create/delete`. Removed: the Terraform section and its source (page unreadable), complete-mode and child-resource gotchas, `ScopeLocked`, Contributor-lacks-delete claim, Key Vault API version (now a placeholder).
Method: documentation only; no commands were run.
