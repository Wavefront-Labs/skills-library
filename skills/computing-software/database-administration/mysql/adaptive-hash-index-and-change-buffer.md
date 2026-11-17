---
id: computing-software.database-administration.mysql.adaptive-hash-index-and-change-buffer
name: adaptive-hash-index-and-change-buffer
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, adaptive-hash-index, change-buffer, innodb-adaptive-hash-index, innodb-change-buffering, btr-search, innodb-tuning]
level: practitioner
status: docs-checked
description: "Decide whether to keep InnoDB's adaptive hash index and change buffer on: how they work, contention signs in SHOW ENGINE INNODB STATUS, and safe toggling."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-adaptive-hash.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-change-buffer.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-standard-monitor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adaptive hash index and change buffer

Both are InnoDB internal optimizations; in MySQL 8.4 the adaptive hash index defaults to OFF and `innodb_change_buffering` defaults to `none`. Know what you lose or gain before flipping them.

## Adaptive hash index (AHI)
InnoDB watches B-tree lookups and builds an in-memory hash index on hot index prefixes, turning repeated equality lookups into a hash probe.
```sql
SET GLOBAL innodb_adaptive_hash_index = ON;           -- dynamic
-- innodb_adaptive_hash_index_parts (default 8, max 512): each partition has its own latch
```
Helps: read-heavy workloads with repeated point lookups on a working set that fits in the buffer pool.
It may not help every workload; the manual says to benchmark with it enabled and disabled. Disabling empties the hash table immediately while queries continue via the B-trees.

Signals in `SHOW ENGINE INNODB STATUS`:
```
INSERT BUFFER AND ADAPTIVE HASH INDEX
...
1234.56 hash searches/s, 9876.54 non-hash searches/s
```
Low hash/non-hash ratio = AHI not helping. Many threads waiting on rw-latches created in `btr0sea` in the SEMAPHORES section = AHI contention: increase the partitions or disable the AHI. Benchmark both settings with your workload.

## Change buffer
Caches changes to **secondary index** pages that are not in the buffer pool (inserts, delete-marks, purges), merging them later when the page is read. Saves random I/O for write-heavy tables with many secondary indexes on slow disks.
```sql
SET GLOBAL innodb_change_buffering = 'all';     -- default none; see the manual for valid values
SET GLOBAL innodb_change_buffer_max_size = 25;  -- % of buffer pool (default 25)
```
- The manual suggests a larger `innodb_change_buffer_max_size` (0-50) for heavy insert/update/delete servers and a smaller one for mostly static reporting data.

Status: `Ibuf: size N, free list len, seg size, merges` line in the INSERT BUFFER section.

## Gotchas
- If performance changed after an upgrade, compare these two settings first: the 8.4 defaults are AHI off and change buffering `none`.
- Toggling AHI off empties the hash table at once; queries continue through the B-trees, so do it off-peak.

## Checked

2026-11-01. Confirmed against MySQL 8.4 manual pages innodb-adaptive-hash, innodb-change-buffer, innodb-standard-monitor, innodb-parameters (defaults, ranges, dynamic). Removed unconfirmed claims (workloads where AHI hurts, SSD value, unique-index limit, shutdown effects).

Method: documentation only; no commands were run.
