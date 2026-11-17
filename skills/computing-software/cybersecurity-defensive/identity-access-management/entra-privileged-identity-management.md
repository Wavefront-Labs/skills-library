---
id: computing-software.cybersecurity-defensive.identity-access-management.entra-privileged-identity-management
name: entra-privileged-identity-management
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [entra-id, entra-pim, pim, just-in-time-access, role-activation, privileged-roles, access-reviews]
level: practitioner
status: docs-checked
description: "Configure Microsoft Entra Privileged Identity Management: eligible vs active roles, activation settings with MFA and approval, PIM for groups, alerts and reviews."
sources: ["https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-configure", "https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-how-to-change-default-settings", "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/best-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Privileged Identity Management (PIM)

**Goal:** nobody holds powerful Entra or Azure roles permanently; admins activate a role
for a few hours with MFA, justification and (for the most sensitive) approval, and every
activation is logged.

## Plan assignments
- Inventory current permanent assignments: Entra roles (Global Administrator, Privileged
  Role Administrator, Security Administrator, Exchange/SharePoint Administrator...), Azure RBAC
  (Owner, User Access Administrator, Contributor at subscription/management group), and
  privileged groups.
- Convert to **eligible** assignments; keep **active (permanent)** only for break-glass
  accounts (excluded from CA with monitoring) and service principals that cannot use PIM.
- Prefer least-privilege roles (e.g. User Administrator rather than Global Administrator).
- Keep the number of Global Administrators small.

## Role settings (per role)
- Activation maximum duration: the setting accepts 1 to 24 hours; use the shortest practical value for high-privilege roles.
- On activation require: **multifactor authentication** or an authentication context mapped to a Conditional
  Access policy requiring phishing-resistant MFA; justification; ticket number.
- **Require approval** for Global Administrator, Privileged Role Administrator and
  subscription Owner/User Access Administrator; approvers are a small group, not the requester.
- Eligible assignment expiry so access lapses unless renewed.
- Notifications to the security team on activation of the top roles.

## PIM for groups
Make a security group "PIM-enabled" to manage membership/ownership just in time; use it for
role-assignable groups or for app access that does not support roles directly.

## Monitoring and reviews
- PIM security alerts (review the alert types in the PIM documentation).
- Access reviews of eligible and active assignments quarterly.
- Stream the Entra audit logs (PIM activations and role assignments)
  to the SIEM; alert on activations at odd hours or by unusual users, and on direct
  assignments bypassing PIM.

## Gotchas
- Requires Entra ID P2 or Entra ID Governance licences for users who benefit.
- Admins activating "just in case" for the full day; shorter durations and review of
  justification quality fix habits.

## Verify
Entra roles blade shows no permanent assignments except break-glass and documented service
principals; a test activation demands MFA/approval and appears in audit logs and SIEM.

## Checked

2026-10-28. Confirmed against the PIM configure and role settings pages: activation duration accepts 1 to 24 hours, multifactor authentication or authentication context on activation, approval option, P2 or Entra ID Governance licence requirement, break-glass accounts excluded from policies. Removed: Global Administrator count, '2' break-glass count, 6-12 month expiry, AuditLogs category string, PIM alert list, token-caching gotcha, 'Azure MFA' wording.

Method: documentation only; no commands were run.
