---
id: computing-software.networking-hardware-and-wireless.tailscale.user-approval
name: user-approval
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [user-approval, user-management, needs-approval]
level: practitioner
status: docs-checked
description: "Gate new users until an admin approves them."
sources: ["https://tailscale.com/kb/1239"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# User approval

Goal: stop new users from reaching other devices until approved.

- Tailnets created May 22, 2025 or later have it enabled by default; earlier tailnets had it disabled.
- Enable: Owner, Admin or Network admin, User management page, turn on User Approval.
- A new user's status is needs approval. Their device can reach the coordination server but not other tailnet devices, and its Machines entry shows a User needs approval badge (filterable).
- Approve: Owner, Admin or IT admin, Users page. The user sits at the top with a Needs approval badge; you can also filter with `status:needsapproval`.
- Before approving you can change the role, for example Member to IT admin, then choose Approve from the menu.
- An unapproved user can instead be removed.

**Checklist**

1. Confirm it is on for older tailnets.
2. Review role before approving.
3. Use the status filter for queues.

## Checked

2026-11-03. Read User approval (kb/1239) and confirmed the 22 May 2025 default, roles, badges and the `status:needsapproval` filter. Nothing else was removed.

Method: documentation only; no commands were run.
