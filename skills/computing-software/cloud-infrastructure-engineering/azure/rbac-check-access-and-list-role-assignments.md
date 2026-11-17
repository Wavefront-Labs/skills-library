---
id: computing-software.cloud-infrastructure-engineering.azure.rbac-check-access-and-list-role-assignments
name: rbac-check-access-and-list-role-assignments
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-rbac, check-access, role-assignments, access-review, resource-graph, audit, orphaned-assignments, effective-permissions, iam]
level: practitioner
status: docs-checked
description: "Answer 'who has access to what' in Azure: Check access in IAM, az role assignment list by scope or assignee, and Resource Graph role-assignment queries."
sources: ["https://learn.microsoft.com/en-us/azure/role-based-access-control/check-access", "https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-list-cli", "https://learn.microsoft.com/en-us/azure/role-based-access-control/troubleshoot-limits", "https://learn.microsoft.com/en-us/azure/governance/resource-graph/reference/supported-tables-resources"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Who can do what — checking and listing Azure RBAC access

**Goal:** answer an auditor or incident responder in minutes: every principal with access to a
scope (including inherited), and what one principal holds on one resource.

## 1. One principal, one resource: Check access
Open the resource (management group, subscription, resource group or resource) > **Access
control (IAM)** > **Check access** tab. *View my access* lists your assignments at this scope
and inherited to it; assignments at child scopes are not listed. With Entra ID P2 or ID
Governance, PIM is integrated and eligible and time-bound assignments are listed too, with
*Activate role*. Check access for another user is Step 3 on the same tab.

## 2. List assignments with the CLI
```bash
az role assignment list --assignee <upn-or-objectId>                  # current subscription only
az role assignment list --all --assignee <upn-or-objectId>            # current subscription and below
az role assignment list --scope "/subscriptions/<SUBSCRIPTION_ID>"
az role assignment list --scope /providers/Microsoft.Management/managementGroups/<MG_ID>
```
By default only the current subscription is listed; `--all` adds everything below it and
`--include-inherited` adds assignments at parent scopes. Add
`--query '[].{principalName:principalName, roleDefinitionName:roleDefinitionName, scope:scope}'`
for a compact table. A group assignment shows as one row; its members are not expanded.

## 3. Fleet-wide with Resource Graph
Role assignments and definitions are in the `authorizationresources` table
(`microsoft.authorization/roleassignments`, `microsoft.authorization/roledefinitions`).
Join on the role definition id to filter for Owner or User Access Administrator, then resolve
principal ids in Entra; ids that no longer resolve are orphaned, so remove those assignments.

## 4. Limits to keep in mind
Azure supports up to 5000 role assignments per subscription (fixed; management group scope is
not counted) and 500 per management group.

## Gotchas
- Data-plane access via Key Vault access policies or storage SAS is not in RBAC listings.
- Assignments at child scopes do not appear in Check access for the parent scope.

## Verify
- [ ] Check access on a prod resource for a sampled user matches the CLI listing (same roles, same source).
- [ ] A Resource Graph Owner query returns only groups and workload identities, and no unresolved principals.

## Checked
2026-10-28. Confirmed on the Learn pages "Check access for a user to a single Azure resource", "List Azure role assignments using Azure CLI", "Troubleshoot Azure RBAC limits" and the Resource Graph supported-tables reference: portal steps, PIM integration, `--all`, `--include-inherited`, `--scope`, query form, `authorizationresources` types, limits. Corrected: 4000 per subscription is 5000. Removed (not found in those pages): `--include-groups`, `--include-classic-administrators`, `list-deny`, the `checkAccess` REST claim, Graph transitiveMembers advice, the full KQL, `--management-groups`, access-review settings and licensing, Lighthouse `managedByTenants`.
Method: documentation only; no commands were run.
