---
id: computing-software.database-administration.scylladb.kb-flush-old-tombstones
name: kb-flush-old-tombstones
category: computing-software
field: database-administration
product: scylladb
tags: [tombstones, gc-grace-seconds, compaction, flush, large-partitions]
level: advanced
status: docs-checked
description: "Purge old tombstones from large ScyllaDB partitions: repair, set gc_grace_seconds to the time since the last repair, flush, compact the table, then restore the value."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/tombstones-flush.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Flushing old tombstones from a table

For large partitions full of tombstones. Precondition: the table must be repaired (nodetool repair or Manager) before the `gc_grace_seconds` threshold; tombstones older than the previous repair may then be purged. Find large partitions with the large-partition troubleshooting tables.

Steps:
1. Repair to synchronise the data:
```
nodetool repair <options>
```
2. Set `gc_grace_seconds` to the time since the last repair started (a repair one day ago means 86400):
```
ALTER TABLE <keyspace>.<mytable> WITH gc_grace_seconds = <newTimeValue>;
```
Timing matters: setting it too low would compact tombstones that some replicas have not yet seen. When unsure, ask support.
3. Run `nodetool flush <keyspace> <mytable>`.
4. Run `nodetool compact <keyspace> <mytable>`. Name the table, because the default is every keyspace and table.
5. Restore the original value:
```
ALTER TABLE <keyspace>.<mytable> WITH gc_grace_seconds = <oldValue>;
```
Repeat steps 3 and 4 on all nodes affected by the large tombstone partitions.

## Checked

2026-11-04. Confirmed against kb/tombstones-flush.rst: repair precondition, five steps, flush and compact arguments, repeat on affected nodes. Removed the unsupported advice about disk headroom and repairs during the procedure.

Method: documentation only; no commands were run.
