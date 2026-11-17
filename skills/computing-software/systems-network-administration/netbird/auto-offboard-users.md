---
id: computing-software.systems-network-administration.netbird.auto-offboard-users
name: auto-offboard-users
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, offboarding, idp-sync-revocation, group-access-revocation]
level: practitioner
status: docs-checked
description: "Offboard users and revoke group-based access in NetBird by changing them in the identity provider and letting IdP sync propagate within the sync cycle."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/team/auto-offboard-users.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With IdP sync, access ends when you change the identity provider.

Remove a user:
1. Delete the user in the IdP (the page's example is Microsoft Entra ID).
2. Refresh the IdP to confirm they are no longer active.
3. Wait for the next sync cycle, which "usually takes 300 seconds", or click the integration button on NetBird's Integrations screen to sync sooner.
4. Confirm the user is gone on the NetBird Users dashboard.

Revoke group access: if a policy lets group `Staging` reach group `Servers` and the project ends, remove `Staging` from the IdP. After sync, memberships update and the access tied to that group is revoked automatically.

Useful for departures, ended freelance or seasonal engagements, and finished projects.

## Checked

2026-11-04. Confirmed against the NetBird auto-offboard-users docs page: IdP delete, Refresh, 300-second sync cycle, manual sync from the Integrations screen, Users dashboard check, Staging/Servers group example. Removed a closing claim about setup-key machines that the page does not make.
Method: documentation only; no commands were run.
