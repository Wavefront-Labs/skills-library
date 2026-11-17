---
id: computing-software.database-administration.scylladb.backup-snapshot-and-schema
name: backup-snapshot-and-schema
category: computing-software
field: database-administration
product: scylladb
tags: [backup, snapshot, schema, describe-schema, cqlsh]
level: practitioner
status: docs-checked
description: "Full ScyllaDB backup with snapshots: schema backup with DESC SCHEMA WITH INTERNALS AND PASSWORDS (cqlsh 6.0.23+), nodetool snapshot per node, schema.cql, encrypted SSTables."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/backup-restore/backup.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Full backup with snapshots

Snapshot backup is per node: repeat it on every node, or use cluster-wide native backup or ScyllaDB Manager. Backup works the same for encrypted and non-encrypted SSTables, so encryption at rest does not change the procedure.

1. Back up the schema first. Data can only be restored into a recreated table schema. As a superuser:

```
cqlsh -e "DESC SCHEMA WITH INTERNALS AND PASSWORDS" > db_schema.cql
```
This includes roles, permissions and service levels. You need cqlsh 6.0.23 or newer (`cqlsh --version`); restoring a schema backup made by an older cqlsh can cause data resurrection or data loss.

2. Take the snapshot:

```
nodetool snapshot mykeyspace
```
It is created under the data directory as `keyspace_name/table_name-UUID/snapshots/snapshot_name`. The default name is the current time in milliseconds since the Unix epoch; use `-t` for a tag, `--ttl` for automatic expiry, or `nodetool cluster snapshot` to snapshot all nodes with one command.

Each snapshot directory also has a `schema.cql` with the CREATE statement of that table (including dropped columns). It covers one table only, with no keyspace, roles, permissions or service levels, so it does not replace step 1.

The first command flushes memtables and then hard-links every SSTable. As compaction replaces files, the snapshot keeps the old ones and uses more disk, so delete old snapshots regularly.

## Checked

2026-11-04. Confirmed against backup.rst and snapshot.rst: per-node procedure, encrypted SSTables, DESC SCHEMA WITH INTERNALS AND PASSWORDS, superuser, cqlsh 6.0.23 warning, snapshot path, default name, --ttl, -t, nodetool cluster snapshot and schema.cql contents. Nothing removed.

Method: documentation only; no commands were run.
