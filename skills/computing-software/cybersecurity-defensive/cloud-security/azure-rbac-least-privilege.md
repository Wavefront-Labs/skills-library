---
id: computing-software.cybersecurity-defensive.cloud-security.azure-rbac-least-privilege
name: azure-rbac-least-privilege
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [iam-least-privilege, azure-rbac, custom-roles, role-assignments, management-groups, pim-eligible, azure-policy]
level: advanced
status: docs-checked
description: "Apply least privilege in Azure RBAC: narrow scopes, limit privileged roles and owners, avoid wildcard custom roles, assign to groups, use PIM and conditions."
sources: ["https://learn.microsoft.com/en-us/azure/role-based-access-control/best-practices", "https://learn.microsoft.com/en-us/azure/role-based-access-control/custom-roles", "https://learn.microsoft.com/en-us/azure/role-based-access-control/delegate-role-assignments-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure RBAC least privilege

**Goal:** each identity has the narrowest built-in or custom role at the lowest scope it needs, granted through groups, with privileged roles just-in-time.

## Principles
- Scope hierarchy: management group > subscription > resource group > resource. Avoid broader roles at broader scopes even when convenient.
- Keep at most 3 subscription owners; Defender for Cloud can monitor this recommendation.
- Limit privileged administrator role assignments: remove unnecessary ones, prefer a job function role, and if one is needed use a narrow scope such as resource group or resource.
- **Owner** and **User Access Administrator** can create and delete role assignments. A safer way to delegate is the **Role Based Access Control Administrator** role (fewer permissions than User Access Administrator) with **conditions** limiting which roles can be assigned, to which principals.
- Assign roles to Entra groups, not users. This also reduces the number of role assignments, which is limited per subscription.
- In scripts and automation use the unique role ID, not the role name; names can change (for example when a preview role is released).
- Use Microsoft Entra Privileged Identity Management (PIM) for just-in-time, time-bound privileged access instead of permanent assignments.

## Custom roles
A role definition has `Actions`, `NotActions`, `DataActions`, `NotDataActions` and `AssignableScopes` (required; at most 2,000 entries). Start from a built-in role and modify it, and include only the permissions needed.
- Do not use the `*` wildcard in `Actions` or `DataActions`: future actions added under a wildcard may grant access you did not intend. List them explicitly.
- A custom role that contains `DataActions` cannot be assigned at management group scope.
- Set `AssignableScopes` to the narrowest subscription or resource group that needs the role.

## Verify
- [ ] No more than 3 subscription owners; no permanent Owner outside an approved break-glass list.
- [ ] Privileged roles are PIM-eligible with time limits.
- [ ] Custom roles contain no wildcard actions and have narrow `AssignableScopes`.
- [ ] Delegated role assignment uses Role Based Access Control Administrator with conditions.

## Checked
Checked 2026-11-09 against the three Microsoft Learn pages in `sources` (best practices, custom roles, delegating role assignments with conditions). Removed unconfirmed claims: the specific built-in role examples, the custom-role JSON sample, the Resource Graph audit query, the NotActions-is-not-a-deny and deny-assignment remarks, Contributor and storage keys, access reviews, classic administrators and Activity Log alert advice.
Method: documentation only; no commands were run.
