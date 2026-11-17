---
id: computing-software.messaging-and-integration.ntfy.access-control-users-acl
name: access-control-users-acl
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, access-control, acl, users, auth-default-access]
level: advanced
status: docs-checked
description: "Manage ntfy users and per-topic ACLs with ntfy user and ntfy access, roles, wildcards, and the auth-default-access setting."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Users and ACLs

By default the server is open: everyone can read and write any topic. Enable auth with `auth-file` (or `database-url`).

```yaml
auth-file: "/var/lib/ntfy/user.db"
auth-default-access: "deny-all"
```

`auth-default-access`: `read-write` (default), `read-only`, `write-only`, `deny-all`.

## Users

```
ntfy user list
ntfy user add phil
ntfy user add --role=admin phil
ntfy user change-pass phil
ntfy user change-role phil admin
ntfy user del phil
```

## ACLs

```
ntfy access
ntfy access phil mytopic rw
ntfy access everyone mytopic rw
ntfy access --reset phil
```

Permissions: `read-write` (`rw`), `read-only` (`read`, `ro`), `write-only` (`write`, `wo`), `deny` (`none`). Topic patterns support only `*` (zero or more characters, for example `alerts_*`). `everyone` and `*` both mean anonymous.

## Gotchas

- `ntfy user/access/token` write the auth database directly, so run them on the server.
- Provisioned users and ACLs (`auth-users`, `auth-access` in config) are deleted from the database on restart when removed from config.

## Checked

2026-11-04. Confirmed against the ntfy config page (Access control, Users and roles, ACL): `auth-file`, `database-url`, `auth-default-access` values and `read-write` default, user and access commands, permission aliases, `*` wildcard, `everyone`/`*`, direct database editing, provisioning deletion. Removed: the Verify step (status codes not on the page).
Method: documentation only; no commands were run.
