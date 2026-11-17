---
id: computing-software.systems-network-administration.audiobookshelf.api-keys-create
name: api-keys-create
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [api-keys, authentication, admin, expiration, automation]
level: practitioner
status: docs-checked
description: "Create an Audiobookshelf API key as an admin, with name, user, optional expiry and active flag, and store it because it is shown once."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/api-keys.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
API keys authenticate scripts and automation tools. They belong to the JWT authentication system introduced in server version 2.26.0 and replace the previous token-based approach. They are for server-to-server communication; for third-party apps use the standard JWT flow.

Properties of a key:

- It acts on behalf of one user and inherits that user's permissions.
- It can have an optional expiration date.
- It can be deactivated or deleted without affecting other sessions.

Only an **admin** can create keys. Go to Settings, Users, API Keys (or the `/api/api-keys` endpoint), choose Create API Key, and fill in:

- **Name** - a descriptive label such as "Backup Script" or "Home Assistant Integration".
- **User** - the account the key acts as.
- **Expiration** - optional date.
- **Active** - enable or disable.

After saving, the key is displayed once. Copy and store it securely; it will not be shown again. Pick a least-privileged user for each key, since the key inherits that user's permissions.

## Checked

Method: docs-checked 2026-11-09 against the API Keys page of the Audiobookshelf docs repo (full raw markdown read). Dropped the unconfirmed lost-key advice.
