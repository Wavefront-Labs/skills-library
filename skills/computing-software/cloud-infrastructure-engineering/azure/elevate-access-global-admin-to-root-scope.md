---
id: computing-software.cloud-infrastructure-engineering.azure.elevate-access-global-admin-to-root-scope
name: elevate-access-global-admin-to-root-scope
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-rbac, elevate-access, user-access-administrator, root-scope, tenant-root, global-administrator, access-management-for-azure-resources, break-glass, lost-owner-recovery, tenant-root-group, elevateaccess-action, audit]
level: practitioner
status: docs-checked
description: "Elevate a Global Admin to User Access Administrator at root (/) for tenant-root setup or lost-Owner recovery, then remove the elevation and audit it."
sources: ["https://learn.microsoft.com/en-us/azure/role-based-access-control/elevate-access-global-admin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elevate access — the tenant's break-glass into every subscription, used for minutes not months

**Goal:** when the platform team needs root (`/`) access — first management-group setup,
recovering a subscription whose only Owner left, assigning root-level roles — a Global
Administrator elevates, does the one task, removes elevation, and the SOC sees it.

## 1. What it does
The toggle is only available to users with the Entra Global Administrator role. Setting
**Access management for Azure resources** to Yes assigns you **User Access Administrator**
at scope `/` (root): permission to view all resources and assign roles in every subscription
and management group of the tenant. You then assign yourself or others what is needed.

## 2. Do it
```bash
# 1. elevate (Entra admin center: Entra ID > Manage > Properties > Access management for Azure resources = Yes)
az rest --method post --url "/providers/Microsoft.Authorization/elevateAccess?api-version=2016-07-01"
# 2. see the assignment
az role assignment list --role "User Access Administrator" --scope "/"
# 3. do the one task (role assignment at the scope you need)
# 4. remove elevation
az role assignment delete --assignee <user-principal-name> --role "User Access Administrator" --scope "/"
```
PowerShell equivalents: `Get-AzRoleAssignment` to list and `Remove-AzRoleAssignment ... -Scope "/"` to remove.
REST: POST `elevateAccess` (api-version 2016-07-01), then delete the role assignment it created.
Set the portal toggle back to No as well; it is a per-user setting, so use the same user that elevated.

## 3. Rules of engagement
- Use a PIM-activated Global Administrator with a ticket; avoid standing GA.
- With PIM, deactivating the role does not set the toggle to No: set it to No before you deactivate.
- Assign root-level roles to **groups** (platform admins) so you do not have to elevate again.
- Root-scope assignments appear in subscription IAM as inherited; tell app teams.

## 4. Audit
Elevation and removal write log entries to both the Entra directory audit logs and the Azure
activity logs. In Entra ID > Monitoring > Audit logs, filter Service = **Azure RBAC (Elevated Access)**
(this view was in preview when checked). Entries read "User has elevated their access to User
Access Administrator for their Azure Resources" and "The role assignment of User Access
Administrator has been removed from the user". Directory audit logs are easier to filter and
export; stream them with Entra diagnostic settings to Sentinel or another detection system.

## Gotchas
- Portal banners (Entra Properties, and elsewhere in the portal) warn when users still have elevated access; remove those assignments (you must be elevated yourself to do so).
- Removing the assignment on the Access control (IAM) page is blocked: set the toggle to No or use PowerShell, CLI or REST.
- Elevation does not grant Entra permissions.

## Verify
- [ ] `az role assignment list --role "User Access Administrator" --scope "/"` shows no leftover user after the task.
- [ ] Property *Access management for Azure resources* reads No.
- [ ] The Azure RBAC (Elevated Access) audit log shows both the elevation and the removal.

## Checked
2026-10-28. Confirmed against the Learn page "Elevate access to manage all Azure subscriptions and management groups": Global Administrator only, User Access Administrator at root, toggle and PIM caveat, az rest / az role assignment list / delete, PowerShell and REST steps, banner, audit log service filter and entry text. Removed (not on that page): unverified `--include-inherited`/JSON-query list forms, Activity-log REST filter and diagnostic-settings advice, `Microsoft.Subscription/policies` and Lighthouse/Defender root-task claims, "Set company information" audit events, Defender flagging and service-principal Reader advice, the "assignment stays if GA role removed" claim.
Method: documentation only; no commands were run.
