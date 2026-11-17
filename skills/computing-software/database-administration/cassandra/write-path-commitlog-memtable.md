---
id: computing-software.database-administration.cassandra.write-path-commitlog-memtable
name: write-path-commitlog-memtable
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, commitlog, write-path, memtable-flush, storage-engine, lsm-tree, memtable, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Commit log sync modes and memtable flushing"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/architecture/storage-engine.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Write path: commit log, memtable, flush

Goal: explain write durability and latency.
- `commitlog_sync` is `periodic` (default) or `batch`. In periodic mode writes are acknowledged immediately and the commit log is synced every `commitlog_sync_period` (default 10000ms); in batch mode writes are not acknowledged until the commit log is fsynced.
- Memtables flush to immutable SSTables; a flush is triggered when the commit log approaches `commitlog_total_space` (forcing flushes so segments can be freed), by memtable limits, or manually with `nodetool flush` or `nodetool drain`.
- Commit log data is purged once the corresponding memtable data is flushed.
Verify: `nodetool tablestats` shows memtable and flush counts for the table.

## Checked

2026-11-02. Checked against the Storage Engine page (commitlog_sync modes and defaults, flush triggers, nodetool flush and drain, commit log purge). Removed: the dedicated commit log device advice and the tablestats field-level claim (not stated).

Method: documentation only; no commands were run.
