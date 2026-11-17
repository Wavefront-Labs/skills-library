---
id: computing-software.database-administration.postgresql.brin-indexes-for-append-only-tables
name: brin-indexes-for-append-only-tables
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-index-types, brin-index, block-range-index, time-series, pages-per-range, correlation, append-only, brin-summarize]
level: advanced
status: verified
description: "Use tiny BRIN indexes on huge append-only PostgreSQL tables (logs, time series) where values correlate with physical order, and keep them summarised."
sources:
  - https://www.postgresql.org/docs/current/brin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BRIN indexes

**Goal:** a range filter on `created_at` in a multi-TB events table uses an index
measured in MB rather than a B-tree measured in tens of GB.

## How it works
BRIN stores min/max per block range (`pages_per_range`, default 128 pages = 1 MB).
A query reads only ranges whose min/max can match. Effective only when the
column's values follow physical row order: insert-ordered timestamps or
sequence ids.

## Check suitability first
```sql
ANALYZE events;
SELECT attname, correlation FROM pg_stats WHERE tablename='events' AND attname='created_at';
```
`correlation` near 1 or -1: BRIN works. Near 0 (random order, heavy updates
moving rows): useless.

## Create
```sql
CREATE INDEX events_created_brin ON events USING brin (created_at) WITH (pages_per_range = 32);
-- PG14+: multi-minmax tolerates some out-of-order rows
CREATE INDEX ON events USING brin (created_at timestamptz_minmax_multi_ops);
```
Smaller `pages_per_range` = more precise, slightly bigger index.

## Keep it summarised
New block ranges at the end of the table are not summarised until VACUUM runs
(or with `autosummarize`):
```sql
ALTER INDEX events_created_brin SET (autosummarize = on);
SELECT brin_summarize_new_values('events_created_brin');
```
Unsummarised ranges are always scanned, so recent-data queries degrade if
autovacuum rarely visits an insert-only table (tune
`autovacuum_vacuum_insert_scale_factor`, PG13+).

## Gotchas
- Results are lossy: plan shows `Bitmap Heap Scan` with `Rows Removed by Index
  Recheck`; a high number means poor correlation or too-large ranges.
- Not for point lookups or uniqueness; keep the PK B-tree.
- `CLUSTER` or partitioning by time restores correlation if it degraded.

## Verify
`EXPLAIN (ANALYZE, BUFFERS) SELECT count(*) FROM events WHERE created_at >= now()-interval '1 day';`
shows `Bitmap Index Scan on events_created_brin` and few heap blocks read;
compare `pg_relation_size` of BRIN vs an equivalent B-tree.

## Checked
- PostgreSQL 17.6, 600,000 rows inserted in time order: correlation 1, BRIN 24 kB versus 13 MB for B-tree, `timestamptz_minmax_multi_ops` accepted (docs: present in 14, absent in 13), `autosummarize` and `brin_summarize_new_values()` ran (39 ranges summarised after an append), `autovacuum_vacuum_insert_scale_factor` exists (13 release notes), and the same data in random order (correlation -0.009) still used the BRIN but read nearly every block as lossy. Query timings were not benchmarked.
