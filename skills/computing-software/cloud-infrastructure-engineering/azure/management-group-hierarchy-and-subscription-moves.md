---
id: computing-software.cloud-infrastructure-engineering.azure.management-group-hierarchy-and-subscription-moves
name: management-group-hierarchy-and-subscription-moves
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, management-groups, hierarchy, subscription-move, default-management-group, require-authorization, tenant-root-group, landing-zones, policy-inheritance, rbac-inheritance, hierarchy-settings]
level: practitioner
status: docs-checked
description: "Build a shallow Azure management group hierarchy, set the default group and authorization protection, and move subscriptions with the right permissions."
sources: ["https://learn.microsoft.com/en-us/azure/governance/management-groups/overview", "https://learn.microsoft.com/en-us/azure/governance/management-groups/manage", "https://learn.microsoft.com/en-us/azure/governance/management-groups/how-to/protect-resource-hierarchy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Management group hierarchy — build it once, move things deliberately

**Goal:** a shallow hierarchy (for example root, platform, landing zones, sandbox, decommissioned)
that policy and RBAC inherit through, with new subscriptions landing in a safe default and
moves done without breaking deployments.

## 1. First-time setup and limits
- The root management group shows as **Tenant root group**; its ID is the Entra tenant ID. It
  cannot be moved or deleted.
- No one has default access to the root. Only Global Administrators can elevate themselves
  (see the elevate-access skill), then assign roles to a platform group.
- Limits: 10,000 management groups per directory; a tree supports up to six levels of depth;
  a subscription has one parent.
- Use the management group **ID**, not the display name, in commands.

## 2. Hierarchy settings (before onboarding subscriptions)
Changing them needs `Microsoft.Management/managementgroups/settings/write` and `/read` on the
root (both are in the built-in role **Hierarchy Settings Administrator**).
- **Default management group** for new subscriptions: portal Management groups > Settings >
  *Change default management group*, or PUT
  `https://management.azure.com/providers/Microsoft.Management/managementGroups/{rootMgID}/settings/default?api-version=2020-05-01`
  with `defaultManagementGroup` set to the group's full resource ID. Setting it back to the root's ID restores the default.
- **Require authorization** for group creation: same endpoint, body property
  `requireAuthorizationForGroupCreation` (true or false); with true, creating a group needs write permission on the parent.

## 3. Create and arrange (CLI)
```bash
az account management-group list
az account management-group show --name 'Contoso' -e -r                  # group and whole tree below it
az account management-group subscription add --name 'Contoso' --subscription '<SUBSCRIPTION_ID>'
az account management-group subscription remove --name 'Contoso' --subscription '<SUBSCRIPTION_ID>'
az account management-group update --name 'Contoso' --parent ContosoIT   # move a group
az account management-group update --name 'Contoso' --display-name 'Contoso Group'
```
Subscriptions can also be moved with an ARM template deployed at tenant scope.

## 4. Moving a subscription or group: what is required
To move a child you need, on the child itself, write permission (`Microsoft.Management/managementgroups/write`,
and `managementgroups/subscriptions/write` for a subscription) plus `Microsoft.Authorization/roleAssignments/delete`
where the page lists it, and `managementgroups/write` on the target and on the existing parent. Built-in
examples: Owner, Contributor, Management Group Contributor (check the role table on the overview page). If either
side is the root, the permission requirements do not apply. If your Owner on the subscription is inherited from its
current group, you can only move it to a group where you also hold Owner.
- A moved subscription inherits the new parent's access and policy.
- Subscription role assignments that depend on a custom role whose assignable scope is the old group break the move: remove the assignment first.
- Resource Manager caches the hierarchy for up to 30 minutes, so the portal may not show a move immediately.

## 5. Delete
A management group can be deleted only when it has no child groups or subscriptions and you
have write permission on it: `az account management-group delete --name 'Contoso'`.

## Gotchas
- Subscriptions you cannot read do not appear in the tree.
- Only one management group may appear in the assignable scopes of a new custom role.

## Verify
- [ ] `az account management-group show --name <ROOT-ID> -e -r` matches the intended design.
- [ ] Settings show the intended default management group and authorization protection.

## Checked
2026-10-28. Confirmed on the Learn pages "Management groups overview", "Manage your Azure subscriptions at scale with management groups" and "How to protect your resource hierarchy": limits, root properties, settings endpoint (api-version 2020-05-01), `requireAuthorizationForGroupCreation`, Hierarchy Settings Administrator, CLI forms, move permissions, 30-minute cache, delete requirements. Corrected: property name (was `requireAuthorization`), move command (was `move --new-parent`), api versions. Removed (not on those pages): Bicep/API-version specifics, policy-state and DINE advice, reservation scoping, Lighthouse and 30-minute RBAC propagation claims, quarantine-MG naming conventions.
Method: documentation only; no commands were run.
