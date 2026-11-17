---
id: computing-software.messaging-and-integration.debezium.mysql-snapshot-locking-modes
name: mysql-snapshot-locking-modes
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mysql, snapshot, global-read-lock, table-locks]
level: advanced
status: docs-checked
description: "Understand how MySQL snapshots lock tables: global read lock, snapshot.locking.mode and the table-level lock fallback."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mysql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The default initial snapshot uses a global read lock to get a consistent schema and binlog position. Setting `snapshot.locking.mode` (default `minimal`) controls how long it is held:

- `minimal`: the global lock is held only during the first phase, reading schemas and metadata. It is then released and the connector reads rows within a `REPEATABLE READ` transaction, which keeps the data consistent even though other clients may write again.
- `extended`: blocks all writes for the entire snapshot. Use it if clients run operations that clash with `REPEATABLE READ`.
- `none`: acquires no table locks during the snapshot.

When the connector detects that global read locks are not permitted, as on hosted services, it automatically uses table-level locks. The connector account then needs the `LOCK TABLES` privilege.

```json
"snapshot.locking.mode": "minimal",
"snapshot.mode": "initial"
```

By default the snapshot captures data for all non-system tables; narrow it with `table.include.list` or `table.exclude.list`.

Large snapshots can outlast the server connection. Raise `interactive_timeout` and `wait_timeout` (in seconds) in the MySQL configuration so the connection is not closed while tables are read.

Gotcha: `extended` blocks all writes for the whole snapshot, and `none` is safe only if no schema changes occur meanwhile. MyISAM tables are locked regardless.

Check: watch for application write stalls during the first snapshot window.

## Checked

2026-11-03. Page used: the Debezium mysql connector reference, https://debezium.io/documentation/reference/stable/connectors/mysql.html.
Confirmed against it: snapshot.locking.mode default and the three modes, REPEATABLE READ, table-level lock fallback with LOCK TABLES, interactive_timeout and wait_timeout, MyISAM note.
Removed or reworded: nothing.
Method: documentation only; no commands were run.
