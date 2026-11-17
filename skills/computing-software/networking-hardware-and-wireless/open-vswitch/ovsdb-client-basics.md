---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ovsdb-client-basics
name: ovsdb-client-basics
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ovsdb-client, ovsdb, dump, monitor, backup, restore, transact, get-schema]
level: practitioner
status: docs-checked
description: "Query a running OVSDB server with ovsdb-client: list-dbs, get-schema, dump, monitor, transact, backup and restore, and the default socket and database."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovsdb-client.1.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ovsdb-client
ovsdb-client is a command-line client for a running ovsdb-server (ovsdb-client(1)). The `server` argument is an OVSDB active or passive connection method (ovsdb(7)); the default server is `unix:/usr/local/var/run/openvswitch/db.sock` and the default database is `Open_vSwitch`. The `method1,method2,...,methodN` syntax connects to a cluster, trying members in random order until it finds the leader; `--no-leader-only` accepts any member.

Server and schema commands:
- `list-dbs [server]` prints database names, one per line.
- `get-schema [server] [database]` prints the schema as JSON; `list-tables [server] [database]`; `list-columns [server] [database] [table]` (names and types; all tables if no table).
- `get-schema-version`, `get-schema-cksum` (blank if none); `needs-conversion [server] schema` prints yes or no; `convert [server] schema` converts the server's database to that schema atomically. Converting can cause unrecoverable data loss (data in columns or tables missing from the new schema is deleted), so back up first. Standalone databases may also be converted offline with ovsdb-tool convert.

Data commands:
- `dump [server] [database] [table [column...]]` prints the data as tables; with a table, only that table; with columns, only those.
- `transact [server] transaction` sends a JSON array (the params of a JSON-RPC transact request) and prints the reply; `query [server] transaction` is a read-only version (it appends an abort operation and strips its result).
- `backup [server] [database] > snapshot` prints a snapshot in the standalone/active-backup database format, suitable to serve directly with ovsdb-server or to use with restore; it excludes ephemeral columns. Copying the database file with cp is another safe way for standalone or active-backup databases.
- `[--force] restore [server] [database] < snapshot` checks that the schemas match, then atomically deletes all data in the database and replaces it with the snapshot. Row UUIDs differ from the snapshot; stopping the server and replacing the database file preserves UUIDs. Without `--force` it exits with failure if the schemas differ (convert first); `--force` proceeds regardless of schema differences, which may fail or give surprising results.
- `monitor [server] [database] table [column[,column]...]...` prints the initial contents then each change. Special column names `!initial`, `!insert`, `!delete`, `!modify` suppress that kind of output; each column may be named once. `monitor [server] [database] ALL` monitors every table. `monitor-cond [server] [database] conditions table ...` and `monitor-cond-since` take a JSON array of conditions (RFC 7047 5.1, where a condition may also be a boolean). With `--detach`, the client detaches after printing the initial contents.
- `wait [server] database state` waits for `added`, `connected` or `removed`; the database argument is mandatory and `server` must name a single server.
- Testing commands: `lock`, `steal`, `unlock [server] lock`.

## Checked
2026-11-04. Confirmed against ovsdb-client(1). Corrected `restore --force` (it overrides a schema mismatch, not an overwrite guard), dropped the unsourced `ovsdb-client dump Open_vSwitch Bridge name` example, the Verify line and the tcp/Unix gotcha, and fixed `list-columns` (table is optional).
Method: documentation only; no commands were run.
