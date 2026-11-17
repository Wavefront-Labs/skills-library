---
id: computing-software.database-administration.vitess.unmanaged-schema-changes
name: unmanaged-schema-changes
category: computing-software
field: database-administration
product: vitess
tags: [schema-changes, applyschema, unmanaged-ddl, reloadschema, direct-ddl, batch-size]
level: intro
status: docs-checked
description: "Apply unmanaged schema changes in Vitess via ApplySchema, VTGate or directly on MySQL, with --batch-size for CREATEs and ReloadSchema after out-of-band changes."
sources:
  - https://vitess.io/docs/25.0/user-guides/schema-changes/unmanaged-schema-changes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Unmanaged changes are direct, blocking statements; managed online schema changes are recommended for anything that would lock a table.

1. `vtctldclient ApplySchema --sql "ALTER TABLE demo modify id bigint unsigned" commerce`. Vitess finds the keyspace's shards and each primary and runs the statement on all shards concurrently, returning when all finish. ApplySchema validates the schema first, which can be too strict for some cases. When all statements are `CREATE TABLE` or `CREATE VIEW`, add `--batch-size=<n>` (for example `--sql-file /tmp/create.sql --batch-size=100`) to send CREATEs in batches; it applies only to unmanaged changes.
2. Through VTGate with any MySQL client: `ALTER TABLE demo ADD COLUMN sample INT;`. To hit one shard, connect to `commerce/-80`. If VTGate does not recognise the DDL syntax it rejects the statement, and the approach is not recommended for large tables.
3. Directly on the shard primaries' MySQL. VTTablet notices eventually, controlled by `--queryserver-config-schema-reload-time` (default 1800 seconds). Force it with `vtctldclient ReloadSchema zone1-0000000100` (a tablet alias).

The page recommends managed, online schema changes for large tables, since unmanaged statements are blocking.

## Checked

2026-11-08. Read in full on the Unmanaged Schema Changes page: all three approaches, the batch-size flag, the VTGate rejection caveat, the reload interval and ReloadSchema. Removed an uncited selection paragraph.

Method: documentation only; no commands were run.
