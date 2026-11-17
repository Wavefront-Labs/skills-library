---
id: computing-software.database-administration.valkey.acl-command-categories
name: acl-command-categories
category: computing-software
field: database-administration
product: valkey
tags: [acl, acl-cat, command-categories, dangerous, subcommands, first-arg, modules]
level: practitioner
status: docs-checked
description: "Valkey ACL command categories: @admin, @dangerous, @read, @write and others, ACL CAT, subcommand rules, module caveat and deprecated first-arg rules."
sources:
  - https://valkey.io/topics/acl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rather than listing commands one by one, grant categories: `ACL SETUSER antirez on +@all -@dangerous >42a979... ~*` allows everything then removes commands tagged dangerous.

Module caveat: categories never include module commands, except `+@all`, which also covers modules loaded later. So an additive-subtractive rule like `+@all -...` can expose module commands you did not intend; trust the internal table.

Categories (21): `keyspace`, `read`, `write`, `set`, `sortedset`, `list`, `hash`, `string`, `bitmap`, `hyperloglog`, `geo`, `stream`, `pubsub`, `admin`, `fast`, `slow`, `blocking`, `dangerous`, `connection`, `transaction`, `scripting`.
- `admin`: `REPLICAOF`, `CONFIG`, `DEBUG`, `SAVE`, `MONITOR`, `ACL`, `SHUTDOWN`.
- `dangerous`: `FLUSHALL`, `MIGRATE`, `RESTORE`, `SORT`, `KEYS`, `CLIENT`, `DEBUG`, `INFO`, `CONFIG`, `SAVE`, `REPLICAOF`.
- `connection`: `AUTH`, `SELECT`, `COMMAND`, `CLIENT`, `ECHO`, `PING`.
- `fast`: O(1) commands (may loop over arguments); `slow` is everything else.
- `read` and `write` apply to commands touching keys; commands without keys have neither.
Commands can sit in several categories, so `+@geo -@read` drops the read-only geo commands.

Discover: `ACL CAT` lists categories; `ACL CAT geo` lists its commands (`geoadd`, `geosearch`, `geosearchstore`, `geodist`, ...).

Subcommands use a pipe: `+config|get`, `-config|set`, for all commands except `DEBUG`.

Deprecated first-arg rule: `ACL SETUSER myuser -select +select|0` allows only `SELECT 0`; only additive (`+`), never `-select|1`, and not for commands with subcommands. Prefer database permissions (`db=`). Another example: `-debug +debug|digest`. List every valid first argument, as new ones may be added later.

## Checked
2026-11-03. Confirmed against the Valkey ACL page (valkey.io/topics/acl/): the 21 categories from the `ACL CAT` listing, the admin/dangerous/connection/fast/slow/read/write descriptions, the module caveat for `+@all`, `ACL CAT geo`, `+config|get` subcommand rules (all commands except DEBUG) and the deprecated first-arg rule with its `-select +select|0` and `-debug +debug|digest` examples. Nothing removed.
Method: documentation only; no commands were run.
