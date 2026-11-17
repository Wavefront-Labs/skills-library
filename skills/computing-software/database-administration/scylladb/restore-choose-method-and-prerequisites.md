---
id: computing-software.database-administration.scylladb.restore-choose-method-and-prerequisites
name: restore-choose-method-and-prerequisites
category: computing-software
field: database-administration
product: scylladb
tags: [restore, schema, truncate, encryption-at-rest, backup]
level: practitioner
status: docs-checked
description: "Choosing a ScyllaDB restore method (cluster backup, object storage, load and stream, identical cluster) and shared prerequisites: recreate schema as superuser, TRUNCATE tables."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/backup-restore/restore.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Restore: choosing a method and prerequisites

Restoring needs all snapshot files of the tables, plus incremental backup files taken after the snapshot if available. Pick by where the files are and whether topology changed:

- **Cluster backup** (made with `nodetool cluster backup`): into a tablet table; each replica downloads its own tablets straight from object storage.
- **Object storage** (made with `nodetool backup`): running cluster, any topology; uses load and stream.
- **Load and stream**: SSTable files on disk uploaded to a running cluster; works regardless of topology changes.
- **Identical cluster**: copy snapshot files back and restart nodes; needs the same node count and token distribution, and each node uses its own backup.
ScyllaDB Manager can also orchestrate backup and restore.

Prerequisites for all methods:
1. From one node, as a superuser, recreate the schema:

```
cqlsh -e "SOURCE '/path_to_schema/db_schema.cql'"
```
2. If tables already exist with data, truncate them so existing data does not override restored data. Truncating a base table also truncates its materialized views and secondary indexes:

```
cqlsh -e "TRUNCATE mykeyspace.team_players"
```
3. For encrypted backups, configure ScyllaDB with the same keys that encrypted the data before you start restoring.

## Checked

2026-11-04. Confirmed against backup-restore/restore.rst: the four methods and their conditions, Manager mention, schema recreation as superuser, truncate and materialized view note, encrypted backup note. Nothing removed.

Method: documentation only; no commands were run.
