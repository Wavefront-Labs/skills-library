---
id: computing-software.database-administration.dragonfly.acl-basics
name: acl-basics
category: computing-software
field: database-administration
product: dragonfly
tags: [acl, acl-setuser, requirepass, acl-groups, dragonfly]
level: practitioner
status: docs-checked
description: "Create and manage Dragonfly users with ACL SETUSER: ON/OFF, passwords, command groups and rules, and how the default user behaves."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/acl.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/acl/setuser.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dragonfly ACL works like Redis ACL. Connections default to user `default`, which can `AUTH` with any password and run any command until you change it.

```
ACL SETUSER John ON >mypassword +@ADMIN +SET
```

If the user does not exist it is created; otherwise it is updated.

- `ON` / `OFF`: whether the user can authenticate. All users except `default` start `OFF`.
- `>password`: set the password. Each user has only one password; a later `>` replaces it.
- `nopass`: any password works.
- `+@GROUP` / `-@GROUP`: grant or revoke a command group (`@ALL` for all). List groups with `ACL CAT`; inspect a user with `ACL GETUSER`.
- `+GET` / `-SET`: individual commands; `+ALL` for every implemented command.

Example: `ACL SETUSER John +@ALL -@ADMIN -@FAST`.

Behaviour:

- Users authenticate with `AUTH <username> <password>`.
- Setting `default` to `OFF` or giving it a password forces all new connections to authenticate.
- Changing a password does not drop existing authenticated connections. `ACL DELUSER` kills the user's connections. `ACL SETUSER` permission changes apply to active connections.
- `--requirepass` sets the `default` user's password at startup.

## Checked

2026-11-04. Confirmed in the Dragonfly ACL guide (default user, ON/OFF, passwords, groups, command rules, authentication behaviour, `--requirepass`) and the ACL SETUSER page (syntax, rule list). Nothing removed.

Method: documentation only; no commands were run.
