---
id: computing-software.messaging-and-integration.ntfy.private-instance-setup
name: private-instance-setup
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, private-instance, deny-all, auth-users, auth-access]
level: advanced
status: docs-checked
description: "Lock down a self-hosted ntfy server with deny-all default access, provisioned users, ACLs and tokens, plus UnifiedPush exceptions."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# A private instance

```yaml
auth-file: "/var/lib/ntfy/user.db"
auth-default-access: "deny-all"
auth-users:
  - "phil:$2a$10$YLiO8U21sX1uhZamTLJXHuxgVC0Z/GKISibrKCLohPgtG7yIxSk4C:admin"
  - "backup-script:$2a$10$/ehiQt.w7lhTmHXq.RNsOOkIwiPPeWFIzWYO3DRxNixnWKLX8.uj.:user"
auth-access:
  - "backup-script:backups:rw"
auth-tokens:
  - "phil:tk_3gd7d2yftt4b8ixyfe9mnmro88o76:My personal token"
```

- `auth-users` format: `<username>:<password-hash>:<role>`. Generate hashes with `ntfy user hash`.
- `auth-access` format: `<username>:<topic-pattern>:<access>`, for example `"*:announcements:ro"`.
- `auth-tokens` format: `<username>:<token>[:<label>]`.

## UnifiedPush on a private server

```
ntfy access '*' 'up*' write-only
```

## Gotchas

- Setting `database-url` also enables auth but keeps default `read-write`; still set `deny-all`.
- `require-login: true` makes all web app actions require a login; `web-root: disable` turns the web app off.
- Users, ACLs and tokens removed from config are deleted on restart.

## Checked

2026-11-04. Confirmed against the ntfy config page (Example: private instance, users/ACL/tokens via config, removal deletes entries, database-url implies auth, UnifiedPush ntfy access command, require-login, web-root). Removed: the Verify curl test and its 401/403 claim.
Method: documentation only; no commands were run.
