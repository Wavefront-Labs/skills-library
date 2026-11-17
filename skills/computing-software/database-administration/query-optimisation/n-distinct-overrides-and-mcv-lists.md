---
id: computing-software.database-administration.query-optimisation.n-distinct-overrides-and-mcv-lists
name: n-distinct-overrides-and-mcv-lists
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, cardinality-estimation, n-distinct, most-common-values, pg-stats, statistics-target, histogram]
level: advanced
status: draft
description: "Read column statistics (pg_stats n_distinct, most common values, histograms), spot sampling errors on large skewed tables, and fix them with targets or n_distinct overrides."
sources:
  - https://www.postgresql.org/docs/current/planner-stats.html
  - https://www.postgresql.org/docs/current/view-pg-stats.html
  - https://www.postgresql.org/docs/current/sql-altertable.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# n_distinct overrides and MCV lists

Examples use PostgreSQL; the same concepts exist elsewhere (SQL Server `DBCC SHOW_STATISTICS`
density and histogram steps, Oracle `DBA_TAB_COL_STATISTICS` NUM_DISTINCT and histograms,
MySQL histograms in `information_schema.column_statistics`).

## Read the stats
```sql
SELECT attname, null_frac, n_distinct, most_common_vals, most_common_freqs,
       histogram_bounds, correlation
FROM pg_stats WHERE schemaname = 'public' AND tablename = 'orders' AND attname = 'customer_id';
```
- `n_distinct`: positive = absolute count; negative = fraction of rows (-1 = unique).
- `most_common_vals/freqs` (MCV): the values covering most rows and their frequencies; equality
  estimates for these are accurate.
- `histogram_bounds`: equal-frequency buckets for values **not** in the MCV list.
- `correlation`: physical order vs column order (affects index scan cost).

## Typical estimation failures
- **n_distinct underestimated** on big tables: ANALYZE samples 300 x statistics target rows
  (30,000 by default) and extrapolates distinct counts badly for skewed data. The planner then
  expects too many rows per value (`rows=50000` estimated vs `rows=12` actual) and picks scans or
  hash joins.
- **Skew outside the MCV list**: a value with many rows that did not make the top-N list gets the
  average estimate.
- **Correlated columns**: per-column stats multiply selectivities as if independent (needs
  extended statistics instead).

## Fixes
```sql
-- 1. bigger sample and longer MCV/histogram for that column
ALTER TABLE orders ALTER COLUMN customer_id SET STATISTICS 1000;   -- default_statistics_target 100, max 10000
ANALYZE orders (customer_id);

-- 2. override n_distinct when you know the truth (positive count or negative fraction)
ALTER TABLE orders ALTER COLUMN customer_id SET (n_distinct = 250000);
ALTER TABLE events ALTER COLUMN session_id SET (n_distinct = -0.05);   -- ~5% of rows distinct
ANALYZE orders;                                                         -- override applied at next ANALYZE
-- for partitioned/inheritance parents: n_distinct_inherited
```
Check actual distinct counts on a replica first:
`SELECT count(DISTINCT customer_id) FROM orders;`

## Gotchas
- Higher targets make ANALYZE slower and plans slightly costlier to compute; raise only for
  columns that matter.
- Overrides do not adapt as data grows; revisit them.
- Autovacuum's auto-analyze may not run often enough on append-only tables; schedule ANALYZE
  after big loads.

## Verify
`EXPLAIN ANALYZE` estimated rows for the problem predicate now track actual rows within a small
factor, and the plan changes accordingly.
