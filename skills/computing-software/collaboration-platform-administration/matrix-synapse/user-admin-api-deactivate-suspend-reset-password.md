---
id: computing-software.collaboration-platform-administration.matrix-synapse.user-admin-api-deactivate-suspend-reset-password
name: user-admin-api-deactivate-suspend-reset-password
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, admin-api, users, deactivate, erase, gdpr, suspend, reset-password, logout-devices]
level: practitioner
status: docs-checked
description: "Use the Synapse user admin API to deactivate or erase an account, suspend or unsuspend it, and reset a password, including what deactivation does and does not remove."
sources:
  - https://element-hq.github.io/synapse/latest/admin_api/user_admin_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All calls need an admin `access_token`.

**Deactivate.** `POST /_synapse/admin/v1/deactivate/<user_id>` with `{"erase": true}`; `erase` is optional and defaults to false, and an empty body is accepted for backwards compatibility. Erase marks the user as GDPR-erased: their messages stay visible to people who were in the room when sent, but are hidden from anyone joining later.

Deactivation tries to unbind 3PIDs from the identity server and removes them from the homeserver, deletes all devices and E2EE keys, access tokens, pushers and the password hash, removes the user from every room and from the user directory, rejects pending invites, clears account validity data, and wipes account data (ignored users, push rules, secret storage and cross-signing keys). With `erase`, it also removes the display name, avatar URL and custom profile fields and marks the user erased.

It does not: remove SSO ID mappings, delete uploaded media (including avatar images), delete messages, remove the registration timestamp, remove rate limit overrides, remove the user from monthly active users, or clear consent information. Delete media separately with the user media API.

**Suspend.** `PUT /_synapse/admin/v1/suspend/<user_id>` with `{"suspend": true}`; send `{"suspend": false}` to lift it. A suspended user cannot send invites, join or knock on rooms, send messages, change profile data, or redact messages other than their own.

**Reset password.** `POST /_synapse/admin/v1/reset_password/<user_id>` with `{"new_password": "<secret>", "logout_devices": true}`. `new_password` is required; `logout_devices` defaults to true, logging the user out of every device. This API is disabled when Matrix Authentication Service integration is enabled; use the MAS admin API or CLI instead.

## Checked

Method: docs-checked 2026-11-09 against docs/admin_api/user_admin_api.md (Synapse develop branch, raw markdown; Deactivate, Suspend and Reset password sections read in full).
