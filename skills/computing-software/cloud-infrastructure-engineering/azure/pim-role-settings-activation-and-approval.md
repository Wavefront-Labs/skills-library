---
id: computing-software.cloud-infrastructure-engineering.azure.pim-role-settings-activation-and-approval
name: pim-role-settings-activation-and-approval
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, pim, privileged-identity-management, pim-role-settings, activation-duration, pim-approval, role-management-policy, authentication-context, justification, ticket-information, activation-mfa, notifications, pim-notifications, graph-api]
level: advanced
status: docs-checked
description: "Configure PIM role settings per Entra and Azure role: activation duration, MFA or authentication context, approval, justification/ticket, eligible duration, notifications."
sources: ["https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-how-to-change-default-settings", "https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-resource-roles-configure-role-settings", "https://learn.microsoft.com/graph/api/unifiedrolemanagementpolicyrule-update"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PIM role settings — make activation cost the right amount of friction

**Goal:** every privileged Entra and Azure role has a role-management policy that matches its
blast radius: short activation, strong auth, approval where humans must be in the loop,
and no permanent assignments that bypass it.

## 1. The settings and sane defaults
| Setting | Global Admin / Owner | Contributor-class | Reader-class |
|---|---|---|---|
| Activation max duration (PIM allows 1–24 h) | 2–4 h | 8 h | 8–24 h |
| On activation require | **Authentication context** (CA policy: phishing-resistant MFA + compliant device) | MFA | MFA |
| Require justification | yes | yes | no |
| Require ticket info | yes (change ticket) | optional | no |
| Require approval | yes, 2+ approvers group | no | no |
| Allow permanent eligible | no (expire 1 y) | 1 y | 1 y |
| Allow permanent active | **no** | no | no |
| Notifications | admins + approvers on activation | default | default |
Approvers: prefer a group over individuals so one person isn't a single point of failure.

## 2. Portal path
Entra ID → Identity Governance → PIM → *Microsoft Entra roles* (or *Azure resources* → pick
subscription) → Settings → role → **Edit** → Activation / Assignment / Notification tabs.
Azure resource roles get settings **per scope** (management group, subscription, RG) — set at
management group and let inheritance apply.

## 3. As code with Graph (Entra roles)
```bash
# find the policy for a role: assignments link policies to roleDefinitionId + scope
az rest -m GET -u "https://graph.microsoft.com/v1.0/policies/roleManagementPolicyAssignments?\$filter=scopeId eq '/' and scopeType eq 'DirectoryRole' and roleDefinitionId eq '62e90394-69f5-4237-9190-012177145e10'"
# -> policyId "DirectoryRole_<tenant>_<guid>"; list rules
az rest -m GET -u "https://graph.microsoft.com/v1.0/policies/roleManagementPolicies/<POLICY-ID>/rules"
# set max activation duration (rule id Expiration_EndUser_Assignment)
az rest -m PATCH -u "https://graph.microsoft.com/v1.0/policies/roleManagementPolicies/<POLICY-ID>/rules/Expiration_EndUser_Assignment" \
  -b '{"@odata.type":"#microsoft.graph.unifiedRoleManagementPolicyExpirationRule","isExpirationRequired":true,"maximumDuration":"PT4H"}'
# MFA, justification, ticketing and approval live in other rules of the same policy:
# read their ids and shapes from the GET .../rules output, then PATCH each the same way
# (types: unifiedRoleManagementPolicyEnablementRule, unifiedRoleManagementPolicyApprovalRule)
```
Azure resource roles use the same `roleManagementPolicies` API with `scopeId` =
`/subscriptions/<id>` and `scopeType: Subscription` (Terraform: `azurerm_role_management_policy`).
List the policy's rules to find the rule ids for eligibility, assignment and notification settings.

## 4. Authentication context instead of plain MFA
Create a CA **authentication context** → CA policy targeting that
context (e.g. an authentication strength and a compliant device) → in the
role setting pick "Microsoft Entra Conditional Access authentication context". Create and enable the CA policy first, and don't scope one policy to both the context and a directory role. Activation then requires authentication methods different from the one used at sign-in.

## Gotchas
- Settings apply to **future** activations; already-active assignments keep their expiry.
- If the approval group is empty or all approvers are out, requests stall — keep a break-glass path that bypasses PIM.
- Azure RBAC settings at subscription scope don't flow up; set them at the management group
  for consistency, and re-check after moving subscriptions.
- Role settings are not versioned — export the rules JSON to a repo before every change.

## Verify
- [ ] `GET .../rules` for Global Administrator shows the intended `maximumDuration`, approval required, permanent active disallowed.
- [ ] A test activation prompts for the authentication-context policy (sign-in log shows the CA policy applied) and waits for approval.
- [ ] Notification emails reach the admin alias on activation; approver group has ≥ 2 members.

## Checked

2026-10-28. Confirmed against Microsoft Learn pages: activation maximum duration 1 to 24 hours, authentication context behaviour, Graph rule update for Expiration_EndUser_Assignment.

Removed because not confirmed: the other rule ids, enablement and approval request bodies, approver count and self-approval rules, and the request-expired alert name.

Method: documentation only; no commands were run.
