---
id: computing-software.cloud-infrastructure-engineering.azure.pim-eligible-and-time-bound-assignments
name: pim-eligible-and-time-bound-assignments
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, pim, eligible-assignment, eligible-assignments, time-bound-assignment, pim-assign, active-assignment, role-eligibility-schedule, role-assignment-schedule, az-role-assignment, pim-azure-resources, pim-discovery, assignment-expiry, extend-renew]
level: practitioner
status: docs-checked
description: "Create PIM eligible and time-bound active assignments for Entra roles and Azure RBAC via portal and Graph; set expiry, extend or renew, convert permanent assignments."
sources:
  - https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-how-to-add-role-to-user
  - https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-resource-roles-assign-roles
  - https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-resource-roles-discover-resources
  - https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-how-to-renew-extend
  - https://learn.microsoft.com/en-us/graph/api/rbacapplication-post-roleeligibilityschedulerequests
  - https://learn.microsoft.com/en-us/azure/role-based-access-control/pim-integration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PIM assignments — eligible by default, active only with an end date

**Goal:** no human holds a permanent privileged role. Admins are *eligible* and activate when
needed; the rare active assignment has an expiry; service principals keep plain RBAC.

## 1. Types
- **Eligible**: user/group may activate (subject to role settings). Maximum duration comes from the
  role settings.
- **Active (time-bound)**: role applies now until end date — for a contractor's 2-week project,
  a migration window. Still logged in PIM.
- **Permanent active**: what you are trying to eliminate.
You can assign users or groups, so a group suits a duty several people share.

## 2. Entra roles
```bash
# eligible for 365 days, via Graph
az rest -m POST -u https://graph.microsoft.com/v1.0/roleManagement/directory/roleEligibilityScheduleRequests \
  -b '{"action":"adminAssign","justification":"Tier-1 helpdesk","roleDefinitionId":"<ROLE-TEMPLATE-ID>",
       "directoryScopeId":"/","principalId":"<GROUP-ID>",
       "scheduleInfo":{"startDateTime":"2026-10-16T00:00:00Z","expiration":{"type":"afterDuration","duration":"P365D"}}}'
# active time-bound (2 weeks)
az rest -m POST -u https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignmentScheduleRequests \
  -b '{"action":"adminAssign","justification":"Migration window","roleDefinitionId":"<ROLE-TEMPLATE-ID>",
       "directoryScopeId":"/","principalId":"<USER-ID>",
       "scheduleInfo":{"startDateTime":"2026-10-16T00:00:00Z","expiration":{"type":"afterDateTime","endDateTime":"2026-10-30T00:00:00Z"}}}'
```
Portal: ID Governance → Privileged Identity Management → Microsoft Entra roles → **Add assignments**
→ select a role and members → Assignment type Eligible or Active → start and end date and time → **Assign**.
A time-bound Global Administrator assignment is not removed at expiry if it is the last one.

## 3. Azure resource roles
The updated PIM experience manages Azure resources with no onboarding; the legacy experience needs
discovery first: PIM → Azure resources → **Discover resources** → select management groups or
subscriptions → **Manage resource**. Managing a management group also covers its child resources, and
once managed it cannot be unmanaged.
`az role assignment create` has no eligible or time-bound option: it makes a permanent
assignment. Create the eligible or time-bound assignment in the portal (PIM → Azure resources →
the scope → Assignments → Add assignments) or through the Azure RBAC role eligibility schedule
request REST API; see the PIM integration page in Sources.

## 4. Convert permanent to eligible
1. Inventory: `az role assignment list --all --query "[?principalType=='User'] | [?roleDefinitionName=='Owner' || roleDefinitionName=='Contributor'].{p:principalName,s:scope}" -o table`.
2. Create the eligible assignment for the same principal/scope **first**, confirm they can activate.
3. Remove the permanent one: `az role assignment delete --assignee <id> --role Owner --scope <scope>`.
4. Role settings → *Allow permanent active assignment* = No, so it cannot come back.
Service principals/managed identities: keep normal RBAC (they can't activate); scope them tightly instead.

## 5. Expiry, extend, renew
- Assignees get email 14/1 days before expiry; they request **Extend** (before) or **Renew**
  (after) from PIM → My roles; an administrator of the role approves the request.
- Admin extension: `roleEligibilityScheduleRequests` with `"action":"adminExtend"` (or `adminRenew`).
- Expired assignments move to the Expired roles tab (30 days of history); run access reviews on eligible roles to catch drift.

## Gotchas
- Deactivate an activated role explicitly with the `selfDeactivate` action.

## Checked
2026-10-28. Confirmed against Microsoft Learn: expiry emails 14 days and one day before expiry, Extend and Renew, Expired roles tab with 30 days of history (PIM extend or renew pages); Graph actions adminAssign, adminExtend, adminRenew, selfDeactivate and `afterDateTime`/`afterDuration` expiration (roleEligibilityScheduleRequests create page); `az role assignment` flags (CLI reference). Removed: `--assignment-type`, `--end-date-time`, `--justification` flags that do not exist on `az role assignment create`, ARM, Terraform and Bicep specifics, default-duration, group-type and audit-name claims that could not be confirmed.
Method: documentation only; no commands were run.

## Verify
- [ ] PIM → Entra roles → Assignments shows 0 **permanent active** assignments for privileged roles other than break-glass.
- [ ] Test user sees the role under *My roles → Eligible* and can activate; audit history shows the activation.
- [ ] `az role assignment list --all` for Owner/Contributor contains only groups and service principals.
