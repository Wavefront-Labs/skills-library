---
id: computing-software.cloud-infrastructure-engineering.rancher.auth-user-info-refresh-and-saml-caveats
name: auth-user-info-refresh-and-saml-caveats
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [auth-user-info-max-age-seconds, auth-user-info-resync-cron, saml, groups, user-refresh, global-settings]
level: advanced
status: docs-checked
description: "Control how often Rancher refreshes external users and groups with auth-user-info-max-age-seconds and auth-user-info-resync-cron, and avoid the SAML member-assignment pitfalls."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/authentication-config/manage-users-and-groups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When you enable an external provider, it supplies Rancher with the groups each user belongs to at login. Rancher keeps this user information (whether the user may access Rancher and their group list) so the CLI, API and kubectl can reflect access accurately. It is refreshed on every UI login, and also periodically.

Two **Global Settings** control the periodic refresh (open **Global Settings**, then **Edit Setting** on the row):

- `auth-user-info-max-age-seconds`: if a user makes an API call, directly or through the Rancher CLI or kubectl, and their last refresh is older than this, a refresh is triggered. Default `3600`.
- `auth-user-info-resync-cron`: a recurring schedule that refreshes all users regardless of activity. Default `0 0 * * *`, once a day at midnight.

SAML does not support user lookup, so SAML-based providers do **not** get periodic refresh: user information only updates when the user logs into the UI. A manual refresh option also exists on the page.

SAML caveats when assigning permissions:

- users and groups are not validated when you assign permissions;
- user IDs (the `UID Field`) must be typed exactly, with no search;
- groups must be picked from the dropdown next to the text box, because any typed text is treated as a user;
- the dropdown shows only groups you belong to, although administrators or restricted administrators can join a group they are not in.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Users and Groups. Nothing removed.

Method: documentation only; no commands were run.
