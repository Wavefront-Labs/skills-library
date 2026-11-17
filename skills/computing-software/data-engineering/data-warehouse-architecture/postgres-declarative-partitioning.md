---
id: computing-software.data-engineering.data-warehouse-architecture.postgres-declarative-partitioning
name: postgres-declarative-partitioning
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, postgres-partitioning, postgresql, partition-pruning, pg-partman]
level: advanced
status: verified
description: "Partition large PostgreSQL tables with declarative partitioning: range/list/hash, partition keys and pruning, indexes and constraints, pg_partman automation, and detaching."
sources:
  - https://www.postgresql.org/docs/current/ddl-partitioning.html
  - https://github.com/pgpartman/pg_partman/blob/development/doc/pg_partman.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Postgres declarative partitioning

**Goal:** large time-series or tenant tables in Postgres that stay fast to query, vacuum and expire.

## Create
```sql
CREATE TABLE events (
  event_id   bigint GENERATED ALWAYS AS IDENTITY,
  tenant_id  int NOT NULL,
  created_at timestamptz NOT NULL,
  payload    jsonb,
  PRIMARY KEY (event_id, created_at)          -- PK/unique must include the partition key (else: "unique constraint on partitioned table must include all partitioning columns")
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_10 PARTITION OF events
  FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
CREATE TABLE events_default PARTITION OF events DEFAULT;   -- optional catch-all; blocks DETACH ... CONCURRENTLY (see Retention) and is never pruned away
CREATE INDEX ON events (tenant_id, created_at);            -- created on every partition
```
- RANGE for time, LIST for categories/regions, HASH for even spreading by key.
- Sub-partitioning possible (range then hash) but adds planning overhead.

## Pruning
Queries must filter on the partition key with plan-time or execution-time known values: `WHERE created_at >= now() - interval '7 days'` prunes; functions on the column (`date(created_at) = ...`) do not. Check with `EXPLAIN` (look for only relevant partitions scanned / "Subplans Removed"). Run on PostgreSQL 18.6 (PGlite): `created_at >= '2026-10-02'` scanned `events_2026_10` plus `events_default`; `date(created_at) = '2026-10-02'` scanned every partition; `created_at >= now() - interval '7 days'` showed `Subplans Removed: 1`. A default partition is scanned by every query that is not provably outside it.

## Automate with pg_partman
```sql
CREATE EXTENSION pg_partman SCHEMA partman;
SELECT partman.create_partition(p_parent_table => 'public.events', p_control => 'created_at', p_interval => '1 month', p_premake => 3);
UPDATE partman.part_config SET retention = '13 months', retention_keep_table = false WHERE parent_table = 'public.events';
-- run partman.run_maintenance_proc() via pg_cron, the pg_partman background worker, or an external scheduler
-- (pg_partman 5.x docs name the function create_partition(); create_parent() is kept for backward compatibility. Not run here: pg_partman is not available in PGlite. pg_partman also creates its own default partition unless p_default_table is false.)
```

## Retention and maintenance
```sql
ALTER TABLE events DETACH PARTITION events_2025_09 CONCURRENTLY;   -- errors with "cannot detach partitions concurrently when a default partition exists"; use plain DETACH PARTITION then
DROP TABLE events_2025_09;      -- instant, no bloat, unlike DELETE
```

## Gotchas
- Too many partitions (thousands) slow planning; aim for partitions of a few GB to tens of GB.
- Rows landing in DEFAULT block creating overlapping partitions later (verified: creating a partition whose range holds rows already in the default fails with "updated partition constraint for default partition ... would be violated by some row"); monitor it.
- Foreign keys referencing a partitioned table are supported in modern versions but check yours; unique constraints across partitions need the key included.
- Converting an existing big table: create the partitioned table, attach the old one as a partition (with a matching CHECK constraint to skip validation), then split.

## Verify
`EXPLAIN` of top queries scans only expected partitions; retention job drops partitions on schedule.
