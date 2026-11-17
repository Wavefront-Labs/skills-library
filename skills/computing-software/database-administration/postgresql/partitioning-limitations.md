---
id: computing-software.database-administration.postgresql.partitioning-limitations
name: partitioning-limitations
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, declarative-partitioning, partition-key-unique-constraint, row-movement, partition-pruning, planning-overhead]
level: practitioner
status: verified
description: "Design around PostgreSQL partitioning limits: unique keys must include the partition key, row movement, FK and trigger rules, planning cost of many partitions."
sources:
  - https://www.postgresql.org/docs/current/ddl-partitioning.html#DDL-PARTITIONING-DECLARATIVE-LIMITATIONS
  - https://www.postgresql.org/docs/current/ddl-partitioning.html#DDL-PARTITIONING-BEST-PRACTICES
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partitioning limitations

## Unique constraints must include the partition key
```
ERROR:  unique constraint on partitioned table must include all partitioning columns
```
Each partition enforces uniqueness only locally, so a global `UNIQUE (email)` on a table
partitioned by `created_at` is impossible. Options:
- Include the key: `PRIMARY KEY (id, created_at)`. Lookups by `id` alone then scan every partition's index.
- Partition by something that is part of the natural key (tenant_id, region).
- Keep a separate non-partitioned lookup table with the global unique key, maintained in
  the same transaction.
- Generate IDs that embed time (UUIDv7, Snowflake) so the app can derive the partition.

## Row movement
`UPDATE ... SET created_at = ...` that crosses a bound moves the row (delete + insert) since
PG11. Side effects: triggers fire as DELETE+INSERT on partitions, a concurrent update of the
same row gets a serialization-style error (`tuple to be locked was already moved to another
partition`), and it is slower. Avoid updating partition keys.

## Foreign keys
- FK **from** a partitioned table: fine.
- FK **to** a partitioned table: PG12+, must reference the full unique key including the
  partition column.
- Detaching a partition referenced by FKs requires checking those rows.

## Indexes, triggers, and other objects
- Indexes created on the parent cascade to partitions, but `CREATE INDEX CONCURRENTLY` on a
  partitioned parent is not supported: `CREATE INDEX ... ON ONLY parent` (invalid until all
  attached), build each partition's index concurrently, then
  `ALTER INDEX parent_idx ATTACH PARTITION part_idx`.
- Row triggers defined on the parent are cloned to partitions; `BEFORE` row triggers cannot
  change which partition a row goes to.
- Exclusion constraints need to include partition key columns with equality operators (PG17).
- No global sequence of unique `ctid`/OIDs; `ON CONFLICT` works only with indexes that
  include the partition key.

## Planning and execution cost
- Every query plans over partitions not pruned at plan time; thousands of partitions cost
  planning time and lock-table slots (`max_locks_per_transaction`).
- Runtime pruning works with parameters (`$1`) and subquery results; check EXPLAIN for
  `Subplans Removed: N`.
- Keep counts sensible: hundreds, not tens of thousands. Partition size of 10-100 GB is a
  common target.

## Things that work fine
`TRUNCATE` / `DROP` of a partition for retention, `DETACH CONCURRENTLY` (PG14+), per-partition
VACUUM and tablespaces, logical replication of partitioned tables (`publish_via_partition_root`).

## Verify
Before committing to a design, run the top queries against a prototype with production-like
partition counts and check planning time in `EXPLAIN (ANALYZE, SUMMARY)`.

## Checked
- PostgreSQL 17.6: the unique-constraint error text; row movement on UPDATE; a BEFORE trigger that rewrites the key fails the partition constraint; FK to a partitioned table must reference the full key; `CREATE INDEX CONCURRENTLY` on a partitioned parent errors while `ON ONLY` plus per-partition concurrent builds plus `ALTER INDEX ... ATTACH PARTITION` turns `indisvalid` true; row triggers are cloned to partitions; exclusion constraints need an equality operator on the partition key (`<>` and `&&` rejected); `ON CONFLICT` needs the full key; generic-plan EXPLAIN shows `Subplans Removed`. The concurrent-update error text exists in the REL_17 source (heapam_handler.c). `uuidv7()` is absent on 17 (PG18).
