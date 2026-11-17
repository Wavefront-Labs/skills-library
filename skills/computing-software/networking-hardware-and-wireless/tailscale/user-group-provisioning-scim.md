---
id: computing-software.networking-hardware-and-wireless.tailscale.user-group-provisioning-scim
name: user-group-provisioning-scim
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [scim, user-provisioning, group-sync]
level: advanced
status: docs-checked
description: "Know how suspension, deletion and group sync behave per identity provider."
sources: ["https://tailscale.com/kb/1290"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# User and group provisioning

Goal: sync users and groups from your identity provider.

**Existing users.** When you enable SCIM, users from your IdP already using Tailscale stay in Tailscale; you can review them while enabling.

**SSO and SCIM**

- If one app handles both SSO and SCIM (not a custom Microsoft Entra ID app), users can sign up only if the app allows them.
- If you use different apps for SSO and SCIM, use user approval to restrict who may join.
- Owner, Admin or IT admin can still invite users from other domains and providers.

**Suspension sync**

- Okta: deactivating a user suspends them in Tailscale; merely suspending in Okta does nothing.
- Microsoft Entra ID: a soft delete suspends them in Tailscale.
- Google Workspace: suspending a user suspends them in Tailscale.

**Deletion sync**

- Okta: deletions cannot sync.
- Microsoft Entra ID: soft delete suspends, then 30 days later a hard delete removes them from Tailscale.
- Google Workspace: deleting suspends in Tailscale; recreating a user later is treated as a new user.
- You can also delete users manually, including pre-provisioning users, suspended users and other-domain users.

**Groups.** Group membership syncs from SCIM-integrated IdPs, and you can reuse human-readable group names in policy.

**Checklist**

1. Pick the sync model.
2. Enable user approval if apps differ.
3. Know the Okta deletion gap.

## Checked

2026-11-09. Confirmed against the Tailscale User and group provisioning page: existing users, SSO and SCIM considerations, inviting users, suspension and deletion behaviour per provider, and group sync. Nothing removed.

Method: docs-checked 2026-11-09 against tailscale.com/kb/1290 (User and group provisioning), read in full.
