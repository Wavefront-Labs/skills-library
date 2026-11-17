---
id: computing-software.database-administration.scylladb.nodetool-refresh
name: nodetool-refresh
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, refresh, load-and-stream, sstable-upload, restore]
level: advanced
status: docs-checked
description: "nodetool refresh: load SSTables from the upload directory, local mode flags --skip-cleanup and --skip-reshape, load-and-stream with --scope, MV and index rules."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/refresh.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool refresh

Loads SSTables you placed in a table's `upload` directory without a restart. This is the only supported way to upload SSTables to a node; copying them into the data directory directly is unsupported and fails. Upload dir: `<data dir>/<keyspace>/<table>-<uuid>/upload`. Tables with materialized views or secondary indexes generate view updates from the uploaded data; do not upload MV or index SSTables (it fails).

**Local refresh** (default; not supported for tablets): SSTables are copied from the upload directory into the table's data directory, then cleanup removes partitions this node does not own and an off-strategy compaction reshapes the layout.
```
cp /path/to/sstables/* <upload dir>
nodetool refresh <keyspace> <table> [--skip-cleanup] [--skip-reshape]
```
`--skip-cleanup` risks extra disk use; `--skip-reshape` risks higher read amplification and latency. Use local mode only when the SSTables hold data for this node alone; it is inefficient for restoring backups.

**Load and stream**: each partition is read and streamed to its replicas, so each SSTable need only be uploaded once.
```
nodetool refresh ks tbl --load-and-stream [--primary-replica-only | --scope <scope>]
```
`--primary-replica-only` (`-pro`) streams only to the primary replica, so a repair is needed afterwards. `--scope`: `node`, `rack`, `dc`, or `all` (default); the two options are mutually exclusive.

Cassandra SSTables are accepted for supported versions, except those with trie-based indexes.

## Checked

2026-11-04: local refresh and load-and-stream behaviour, flags, scope values, the MV and SI rule and Cassandra compatibility confirmed against the ScyllaDB nodetool refresh documentation page.

Method: documentation only; no commands were run.
