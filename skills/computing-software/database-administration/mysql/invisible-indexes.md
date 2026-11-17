---
id: computing-software.database-administration.mysql.invisible-indexes
name: invisible-indexes
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-optimization, invisible-indexes, unused-indexes, index-cleanup, use-invisible-indexes, sys-schema-unused-indexes, ignored-indexes]
level: practitioner
status: verified
description: "Drop unused MySQL indexes safely: find candidates with sys.schema_unused_indexes, make them INVISIBLE first, watch for regressions, then drop or instantly restore."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/invisible-indexes.html
  - https://dev.mysql.com/doc/refman/8.4/en/sys-schema-unused-indexes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Invisible indexes

**Goal:** remove index write overhead and disk use without the risk that some
monthly report suddenly scans a 500 GB table.

## Find candidates
```sql
SELECT * FROM sys.schema_unused_indexes WHERE object_schema='appdb';
SELECT * FROM sys.schema_redundant_indexes WHERE table_schema='appdb';   -- prefix duplicates
```
"Unused" means no reads since the last server restart (performance_schema
counters): make sure uptime covers month-end jobs, and check every replica too
(reads may only happen there).

## Hide, observe, then drop
```sql
ALTER TABLE orders ALTER INDEX idx_legacy_status INVISIBLE;   -- metadata-only, in place (ALGORITHM=INPLACE, LOCK=NONE accepted; ALGORITHM=INSTANT is rejected with error 1845 on 9.7.4)
-- wait through a full business cycle; watch slow log and app latency
ALTER TABLE orders DROP INDEX idx_legacy_status;              -- or:
ALTER TABLE orders ALTER INDEX idx_legacy_status VISIBLE;     -- rollback, no rebuild
```
An invisible index is still **maintained** on writes and still enforces
uniqueness; only the optimizer ignores it. So the rollback needs no
rebuild.

## Test a query with it visible again (session only)
```sql
SET SESSION optimizer_switch = 'use_invisible_indexes=on';
EXPLAIN FORMAT=TRADITIONAL SELECT ...;   -- plain EXPLAIN prints the TREE format on 9.x
```
On 9.7.4 with 5000 rows: with the index invisible, `WHERE status='open'` was `type ALL`; with `use_invisible_indexes=on` it used `ref` on the hidden index.

## Gotchas
- Primary keys cannot be invisible (nor an implicit PK from a unique NOT NULL index): both give `ERROR 3522 A primary key index cannot be invisible`.
- A unique index that is invisible still enforces uniqueness (`ERROR 1062` on a duplicate, run).
- Index hints (`FORCE INDEX (idx)`) naming an invisible index raise `ERROR 1176 Key 'idx' doesn't exist in table`:
  grep the code for the index name before hiding.
- Replicas: the visibility change replicates; hide on the source.
- MariaDB 10.6+ has `IGNORED` indexes (`ALTER TABLE t ALTER INDEX i IGNORED`), same idea.

## Verify
```sql
SELECT index_name, is_visible FROM information_schema.statistics
WHERE table_schema='appdb' AND table_name='orders';
```
After the observation window, no slow-query digests regressed, then drop.
