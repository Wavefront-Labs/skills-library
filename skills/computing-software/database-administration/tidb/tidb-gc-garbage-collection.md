---
id: computing-software.database-administration.tidb.tidb-gc-garbage-collection
name: tidb-gc-garbage-collection
category: computing-software
field: database-administration
product: tidb
tags: [tidb, gc, garbage-collection, safe-point, gc-life-time, mvcc, resolve-locks, delete-ranges]
level: advanced
status: docs-checked
description: "Explain TiDB garbage collection: the GC leader, safe point, the Resolve Locks / Delete Ranges / Do GC steps, default 10 minute life time and lock scan modes."
sources: ["https://docs.pingcap.com/tidb/stable/garbage-collection-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb gc garbage collection

Because TiDB uses MVCC, updates keep old versions alongside new ones. Garbage collection (GC) removes obsolete versions.

A single TiDB instance is elected GC leader and drives the process. Each round computes a safe point (current time minus the GC life time) and clears data on the premise that every snapshot after the safe point stays intact. By default GC triggers every 10 minutes and retains the most recent 10 minutes. If a round runs long, the next does not start until it completes.

Three steps per round:
1. Resolve Locks: scan locks older than the safe point on all Regions and clear them. Under the Percolator two-phase commit model, a transaction has one primary lock and secondary locks; if the primary key is committed the lock is committed, otherwise rolled back, and an unfinished primary is treated as timed out and rolled back. The system variable `tidb_gc_scan_lock_mode` selects `LEGACY` (default, GC leader scans every Region) or `PHYSICAL` (Green GC, bypasses Raft, experimental and not recommended for production).
2. Delete Ranges: after `DROP TABLE` or `DROP INDEX`, TiDB records the range and deletion timestamp instead of deleting each key, then physically deletes the range quickly.
3. Do GC: delete versions committed before the safe point but keep each key's last write before the safe point unless it is a delete. TiDB just sends the safe point to PD and TiKV performs GC for the Region leaders on each node. From TiDB 5.0 this always uses `DISTRIBUTED` mode, replacing the old `CENTRAL` mode.

## Checked

2026-11-04. Confirmed against the GC Overview page: GC leader, safe point, 10 minute defaults, the three steps, `tidb_gc_scan_lock_mode` values, DISTRIBUTED mode from 5.0.
Method: documentation only; no commands were run.
