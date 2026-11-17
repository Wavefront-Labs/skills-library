---
id: computing-software.database-administration.valkey.acl-users-and-rules
name: acl-users-and-rules
category: computing-software
field: database-administration
product: valkey
tags: [acl, acl-setuser, auth, users, permissions, selectors, passwords, default-user]
level: practitioner
status: docs-checked
description: "Valkey ACL users: AUTH forms, default user, ACL SETUSER rule syntax for commands, keys, channels, databases, passwords, selectors, plus ACL LIST/GETUSER."
sources:
  - https://valkey.io/topics/acl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Clients authenticate with `AUTH <username> <password>` or `AUTH <password>` (user `default`), or by TLS certificate. The default user starts as `user default on nopass ~* &* +@all`, so unauthenticated connections get full access until you restrict it. Use ACLs to give clients least privilege and to stop mistakes (a job worker never needs `FLUSHALL`).

Rules apply left to right. `ACL SETUSER name rules...` creates a user (off, no password, no commands, no keys, no channels) or incrementally modifies an existing one; repeated calls never reset it.
- State: `on`, `off` (existing connections keep working).
- Commands: `+cmd`, `-cmd`, `+config|get`, `+@category`, `-@category`, `allcommands`, `nocommands`. `AUTH`, `HELLO`, `RESET` cannot be removed.
- Keys: `~pattern`, `%R~pattern` (read), `%W~pattern` (write), `allkeys`, `resetkeys`.
- Channels: `&pattern`, `allchannels`, `resetchannels`; `PSUBSCRIBE` needs a literal match.
- Databases: `db=0,1,2`, `alldbs`, `resetdbs`.
- Passwords: `>pw`, `<pw`, `#sha256hex`, `!hash`, `nopass`, `resetpass`.
- Selectors: `(+SET ~key2)` adds an independent rule set; a command is allowed if root rules or any selector match. `clearselectors` drops them.
- Roles (9.2): `role=a,b`, `resetroles`. `reset` returns the user to its created state.

Example: `ACL SETUSER alice on >p1pp0 ~cached:* +get`. Then `GET foo` fails with `NOPERM ... keys`, `SET cached:1234 zap` with `NOPERM ... 'set' command`.

Inspect with `ACL LIST` (config-file format) or `ACL GETUSER alice` (flags, passwords as hashes, commands, keys, channels, databases, selectors). Define users in config, or in an external ACL file reloaded with `ACL LOAD`.

## Checked
2026-11-03. Confirmed against the Valkey ACL page (valkey.io/topics/acl/): AUTH forms, the default user line from `ACL LIST`, left-to-right rule order, incremental `ACL SETUSER`, every rule in the list (on/off, +/- commands and categories, `%R~`/`%W~`, `&`, `db=`/`alldbs`/`resetdbs`, `>`/`<`/`#`/`!` passwords, selectors, `role=` added in 9.2, `reset`), the alice example and its NOPERM replies, `ACL GETUSER` fields, and `ACL LOAD`. Nothing removed.
Method: documentation only; no commands were run.
