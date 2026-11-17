---
id: computing-software.database-administration.cassandra.snapshots-and-incremental
name: snapshots-and-incremental
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, nodetool-snapshot, incremental-backups, clearsnapshot, snapshot, incremental-backup, restore, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Hardlink snapshots"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/backups.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshots and incremental backups

Goal: take per-node backups.
- A snapshot is a copy of a table's SSTable files at a point in time, created via hard links with `nodetool snapshot`; the table DDL is stored with it. Remove one with `nodetool clearsnapshot`.
- `auto_snapshot` (default true) snapshots before keyspace truncation or dropping a table; `snapshot_before_compaction` defaults to false.
- Incremental backups are off by default; enable with `incremental_backups` in `cassandra.yaml` or `nodetool`, and Cassandra hard-links each flushed or streamed SSTable into a `backups/` subdirectory.
- Incremental backups are normally paired with snapshots.
Verify: restore into a scratch cluster and compare counts.

## Checked

2026-11-02. Checked against the Backups page (snapshot definition, auto_snapshot, snapshot_before_compaction, incremental_backups, backups/ subdirectory, clearsnapshot). Removed: the '-t nightly' form, the DESCRIBE SCHEMA tip, 'you must clean it' and the 'cluster-wide restore needs every node' statement (not stated).

Method: documentation only; no commands were run.
