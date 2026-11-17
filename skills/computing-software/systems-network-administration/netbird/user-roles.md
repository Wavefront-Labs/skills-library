---
id: computing-software.systems-network-administration.netbird.user-roles
name: user-roles
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, user-roles, rbac, network-admin, auditor]
level: intro
status: docs-checked
description: "NetBird user roles: Owner, Admin, Network Admin, Billing Admin, Auditor, User and Agent Network roles, what each can do, token rules and how to assign them."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/team/user-roles.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Core roles:
- Owner: full access, can delete the account; only one.
- Admin: full access except deleting the account or changing the Owner.
- Network Admin: manages Control Center, Access Control, Network Routing, DNS; read-only on Peers, Setup Keys, Team, Activity, Settings; can view but not create setup keys; cannot invite users or create service users.
- Billing Admin: only Settings > Plans & Billing and Invoices.
- Auditor: reads every configuration, changes nothing.
- User: sees only peers they own and may connect to.

Agent Network only: Agent Network Admin (full control of that area, plus read-only access to users, groups, peers and account information) and Usage Viewer (read-only usage and account-wide access logs). Warning: with prompt collection enabled, a Usage Viewer can read other users' prompts.

API: roles apply equally to the management API. Every role except User, Agent Network Admin and Usage Viewer can create a personal access token with that role's permissions.

IdP sync: roles live in NetBird; synced groups control membership only, not role.

Assign: Team > Users > select user > pick role > Save. Only an Owner can assign Owner; this transfers ownership and the old Owner becomes Admin.

## Checked

2026-11-04. Confirmed against the NetBird user roles page: role list and permissions, Network Admin limits, Billing Admin scope, Agent Network roles and Usage Viewer warning, API token rule, IdP sync note, assign steps, Owner transfer. Widened the Agent Network Admin description to match the page.
Method: documentation only; no commands were run.
