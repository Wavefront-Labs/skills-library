---
id: computing-software.database-administration.postgresql.declarative-partitioned-tables
name: declarative-partitioned-tables
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, declarative-partitioning, table-partitioning, partition-by-range, partition-by-list, partition-by-hash, partition-key, primary-key-partition]
level: advanced
status: verified
description: "Design and create PostgreSQL range, list and hash partitioned tables: choosing the key, primary-key rules, partition counts and what partitioning does not fix."
sources:
  - https://www.postgresql.org/docs/current/ddl-partitioning.html
  - https://www.postgresql.org/docs/current/sql-createtable.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declarative partitioning

**Goal:** partition only when it buys something concrete (cheap retention by
dropping partitions, pruning for time-bounded queries, smaller per-partition
vacuum), with a key the queries actually filter on.

## The three strategies
```sql
-- RANGE: time series, retention by dropping old partitions
CREATE TABLE measurements (
  device_id bigint NOT NULL, ts timestamptz NOT NULL, value double precision,
  PRIMARY KEY (device_id, ts)                       -- must include the partition key
) PARTITION BY RANGE (ts);
CREATE TABLE measurements_2026_10 PARTITION OF measurements
  FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');   -- upper bound exclusive

-- LIST: tenant tiers, regions
CREATE TABLE orders (...) PARTITION BY LIST (region);
CREATE TABLE orders_eu PARTITION OF orders FOR VALUES IN ('de','fr','nl');

-- HASH: spread a big table evenly (no retention benefit)
CREATE TABLE sessions (...) PARTITION BY HASH (user_id);
CREATE TABLE sessions_p0 PARTITION OF sessions FOR VALUES WITH (MODULUS 8, REMAINDER 0);
```
Sub-partitioning is allowed (`PARTITION OF ... PARTITION BY ...`) but multiplies counts.

## Sizing rules of thumb
- Keep total partitions in the hundreds to low thousands; planning time and
  lock-manager overhead grow with partitions touched per query.
- Aim for partitions from roughly 1 GB to 100s of GB; monthly vs daily follows from that.
- Queries without the key in WHERE touch every partition: slower than one table.

## Constraints
- PK/unique constraints must include all partition key columns; global
  uniqueness on another column alone is not possible.
- Foreign keys **to** a partitioned table are supported (PG12+); from it too.
- Indexes created on the parent propagate to all partitions (see partitioned indexes).
- Rows that change key value move partitions on UPDATE (PG11+), costing a delete+insert.

## Converting an existing big table
No in-place conversion. Options: create the partitioned table, attach the old
table as one partition (needs a matching CHECK constraint to avoid a scan), and
let new data go into new partitions; or copy with logical replication / batched inserts.

## Verify
```sql
SELECT relname, pg_get_expr(relpartbound, oid) FROM pg_class WHERE relispartition AND relname LIKE 'measurements%';
\d+ measurements
```
`EXPLAIN` of a typical query lists only the expected partitions.

## Checked
- PostgreSQL 17.6: range, list and hash partitions with the exact DDL above, exclusive upper bound, sub-partitioning, PK/unique must include the key, FK from a partitioned table, row movement on UPDATE, and attaching a table with a matching CHECK skips the scan. Sizing figures are rules of thumb, not tested.
