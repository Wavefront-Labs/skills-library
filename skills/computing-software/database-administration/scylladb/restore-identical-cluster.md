---
id: computing-software.database-administration.scylladb.restore-identical-cluster
name: restore-identical-cluster
category: computing-software
field: database-administration
product: scylladb
tags: [restore, snapshot, commitlog, vnodes, offline-restore]
level: advanced
status: docs-checked
description: "Restore snapshot files in place on an identical vnode ScyllaDB cluster: drain, stop, clear commitlog and table files, copy back, chown, start."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/backup-restore/restore.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Restore to an identical cluster

Use only when restoring to the same cluster: same number of nodes and same token ranges, with each node restored from its own backup. Vnode keyspaces only; for tablet keyspaces use object storage or load and stream. If topology differs, load and stream is slower but safe.

Best practice for materialized views and secondary indexes: do not restore their SSTables. DROP the MV or index, restore the base table only, then recreate it from the CQL backup with CREATE MATERIALIZED VIEW or CREATE INDEX.

Do the schema and truncate prerequisites, then on each node:
1. `nodetool drain` to flush data.
2. Stop ScyllaDB.
3. Delete everything in the commitlog directory, so newer inserts cannot override the restored data.
4. Delete the files in `keyspace/table-UUID/`, but not the `snapshots` or `upload` directories (rm will report those two as directories; that is expected).
5. Choose the snapshot (usually the latest) from `table-UUID/snapshots/<snapshot_name>`.
6. Copy its content into the table directory: `sudo cp -r * <data dir>/mykeyspace/team_players-<uuid>`.
7. Copy files from the `backups` folder into the same directory if you have incremental backups.
8. `sudo chown -R scylla:scylla` the table directory.
9. Start the node.

Warning: copying files into the data directory is only allowed while ScyllaDB is stopped. For a running node use the `upload` directory and `nodetool refresh`.

After all nodes are restored, run a full cluster repair: `nodetool repair -pr` on every node for vnode keyspaces.

## Checked

2026-11-09. Confirmed the scope limits, MV and SI advice, per-node steps and the stopped-service warning against the ScyllaDB restore procedure page (all sections read). Added the documented final repair.

Method: docs-checked 2026-11-09 against the ScyllaDB docs page operating-scylla/procedures/backup-restore/restore.rst
