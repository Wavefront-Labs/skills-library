---
id: computing-software.systems-network-administration.netbird.user-approval
name: user-approval
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, user-approval, domain-matching, pending-users]
level: intro
status: docs-checked
description: "Require admin approval for users who join a NetBird account by domain matching: the setting, approving or rejecting, and what the waiting user sees."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/team/approve-users.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
User approval blocks users who join through domain matching until an administrator accepts them. New NetBird Cloud accounts have it enabled by default.

Toggle: Settings > Authentication > User Approval Required.
- On: domain-matched users stay blocked until approved.
- Off: they are added automatically.

Decide: Users page > Approve or Reject on the user's row. Any admin may do it, not only the owner.

The waiting user sees "Waiting for Approval", possibly with a partly hidden email of the account owner. After approval they click Refresh to join.

## Checked

2026-11-04. Confirmed against the NetBird approve users page: default on for new Cloud accounts, Settings Authentication toggle and both states, Approve and Reject on the Users page, Waiting for Approval screen, any admin may approve, Refresh. Removed the peer approval and sign-in domains pointers, which the page does not state.
Method: documentation only; no commands were run.
