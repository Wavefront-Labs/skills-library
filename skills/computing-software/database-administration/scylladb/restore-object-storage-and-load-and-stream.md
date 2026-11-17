---
id: computing-software.database-administration.scylladb.restore-object-storage-and-load-and-stream
name: restore-object-storage-and-load-and-stream
category: computing-software
field: database-administration
product: scylladb
tags: [restore, load-and-stream, upload-directory, primary-replica-only, object-storage]
level: advanced
status: docs-checked
description: "Restore into a running ScyllaDB cluster from S3 with nodetool restore (TOC paths, file lists, parallelising) or from local files with refresh --load-and-stream, plus MV/SI rules."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/backup-restore/restore.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Restore with object storage or load and stream

Both methods stream data to the nodes that own it, so they work regardless of topology changes. If the table has materialized views or secondary indexes, view updates are generated automatically as base data streams; restore base table SSTables only.

**From object storage** (made with `nodetool backup`):
1. Do the restore prerequisites (schema, truncate).
2. List TOC components under the backup prefix, relative to the prefix:
```
aws s3 ls --recursive s3://bucket-foo/ks/cf/24601/ | awk '/-TOC.txt$/ { print $4 }' | sed 's|^ks/cf/24601/||'
```
3. Run `nodetool restore --endpoint ... --bucket bucket-foo --prefix ks/cf/24601 --keyspace ks --table cf <TOC paths>`, or give the paths newline-separated with `--sstables-file-list sstables.list`.
4. By default it waits; `--nowait` returns a task ID for `nodetool tasks`.

Speed-up: one invocation runs on one node; split the SSTable list among nodes and run `nodetool restore` on each, with `--scope` to limit target replicas. With `--primary-replica-only` data goes only to the primary replica and you must run a full cluster repair afterwards.

**Load and stream from files:**
1. Copy the table SSTables into the table `upload` directory on one node (distribute across nodes, each file once) and set ownership:
```
sudo chown -R scylla:scylla <data dir>/mykeyspace/team_players-<uuid>/upload/
```
2. On each node holding files run `nodetool refresh mykeyspace team_players --load-and-stream`.

## Checked

2026-11-04: both restore methods, the MV and SI rule, the TOC listing example, parallelising with --scope, --primary-replica-only with repair, and the upload directory steps confirmed against the ScyllaDB restore procedure page.

Method: documentation only; no commands were run.
