---
id: computing-software.database-administration.postgresql.default-partitions-and-partitioned-indexes
name: default-partitions-and-partitioned-indexes
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, declarative-partitioning, table-partitioning, default-partition, partitioned-index, create-index-on-only, index-attach, concurrently]
level: advanced
status: verified
description: "Use PostgreSQL default partitions safely and build indexes on large partitioned tables without long locks using CREATE INDEX ON ONLY plus per-partition CONCURRENTLY builds."
sources:
  - https://www.postgresql.org/docs/current/ddl-partitioning.html
  - https://www.postgresql.org/docs/current/sql-createindex.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default partitions and partitioned indexes

**Goal:** stray rows never cause insert errors, and adding an index to a 5 TB
partitioned table does not block writes for hours.

## Default partition
```sql
CREATE TABLE measurements_default PARTITION OF measurements DEFAULT;
```
Without it, an out-of-range row fails with `no partition of relation "measurements" found for row`.
With it, rows land there silently, and later:
- creating/attaching a partition whose range covers rows in the default fails
  (`updated partition constraint for default partition would be violated`) and
  otherwise scans the default under lock;
- `DETACH ... CONCURRENTLY` is disallowed.
So: keep a default only as a safety net, alert when `count(*) > 0`, and move rows out:
```sql
BEGIN;
ALTER TABLE measurements DETACH PARTITION measurements_default;
CREATE TABLE measurements_2027_01 PARTITION OF measurements FOR VALUES FROM ('2027-01-01') TO ('2027-02-01');
INSERT INTO measurements SELECT * FROM measurements_default;   -- routes to the right partitions
TRUNCATE measurements_default;
ALTER TABLE measurements ATTACH PARTITION measurements_default DEFAULT;
COMMIT;
```

## Partitioned indexes
`CREATE INDEX ON measurements (device_id)` builds on every partition in one
statement, holding a SHARE lock (blocks writes) throughout, and
`CONCURRENTLY` is not supported on a partitioned parent. Instead:
```sql
CREATE INDEX meas_dev_idx ON ONLY measurements (device_id);          -- invalid shell, instant
CREATE INDEX CONCURRENTLY meas_dev_2026_10 ON measurements_2026_10 (device_id);
ALTER INDEX meas_dev_idx ATTACH PARTITION meas_dev_2026_10;
-- repeat per partition; parent index becomes valid when all are attached
```
Script it over `pg_inherits`. Unique indexes follow the same pattern but must include the partition key.

## Gotchas
- New partitions created later get the parent's indexes automatically.
- `ALTER INDEX ... ATTACH PARTITION` rejects an index on other columns, with a `WHERE` clause or another access method (`The index definitions do not match.`). A partition that already has a matching index cannot take a second one (`Another index is already attached for partition`). In 17.6 a `(b DESC)` index was accepted as a match for `(b)`, so compare definitions yourself.
- Attaching a table with `ALTER TABLE ... ATTACH PARTITION` to a parent that already has an `ON ONLY` index creates (or adopts) the partition's index at that moment.
- `REINDEX` on a partitioned table or index reindexes every partition, each in its own transaction (not allowed inside a transaction block); `CONCURRENTLY` is accepted on the partitioned parent from PG14, or run it per partition.

## Verify
```sql
SELECT indexrelid::regclass, indisvalid FROM pg_index WHERE indrelid = 'measurements'::regclass;  -- valid = t
SELECT count(*) FROM measurements_default;  -- 0
```

## Checked
PostgreSQL 17.6: out-of-range insert gives `no partition of relation "measurements" found for row`; with a default partition holding a 2027 row, `CREATE TABLE ... PARTITION OF ... FOR VALUES` covering it fails with `updated partition constraint for default partition "measurements_default" would be violated by some row`; `DETACH PARTITION ... CONCURRENTLY` fails with `cannot detach partitions concurrently when a default partition exists`; the detach/insert/truncate/re-attach script works and routes the row; `CREATE INDEX CONCURRENTLY` on the parent fails (`cannot create index on partitioned table "measurements" concurrently`); `ON ONLY` index is invalid (`indisvalid = f`) until every partition index is attached, then `t`; a new partition gets the parent index automatically; a plain `CREATE INDEX` took ShareLock on the parent and partitions; a unique index without the partition key fails (`unique constraint on partitioned table must include all partitioning columns`); `REINDEX INDEX CONCURRENTLY` and `REINDEX TABLE CONCURRENTLY` on the parent ran. Docs: sql-reindex (partitioned relations).
