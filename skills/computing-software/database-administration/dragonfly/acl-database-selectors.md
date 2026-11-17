---
id: computing-software.database-administration.dragonfly.acl-database-selectors
name: acl-database-selectors
category: computing-software
field: database-administration
product: dragonfly
tags: [database-selectors, acl-setuser, logical-databases, dragonfly]
level: advanced
status: docs-checked
description: "Restrict a Dragonfly ACL user to specific logical databases with the Dragonfly-specific $database selector rule."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/acl/setuser.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dragonfly ACL supports **database selectors**, a Dragonfly-specific feature restricting which logical databases an authenticated user may use.

Rule syntax: `$<database>` restricts the user to that database number. `$0` restricts to database 0, `$1` to database 1, and so on.

The rule is part of `ACL SETUSER username [rule ...]`, alongside the user management, command, key and pub/sub rules.

Related facts:

- Number of databases is set by `--dbnum` (default 16).
- Multi-shard cluster mode supports only database 0.

Procedure:

1. Create the user with the selector.
2. Inspect the result with `ACL GETUSER username`.
3. Test with `ACL DRYRUN` or by authenticating as the user.

`$all` allows every database and is the default when no selector is given.

## Checked

2026-11-04. Confirmed in the ACL SETUSER page (database selectors section: `$<database>`, `$all`, default behaviour, `--dbnum`), the flags page (`dbnum` default 16) and the Cluster Mode page (multi-shard supports only database 0). Added the documented `$all` rule. Removed the Memcached keyspace claim, which no fetched page states.

Method: documentation only; no commands were run.
