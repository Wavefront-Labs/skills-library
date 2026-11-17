---
id: computing-software.database-administration.query-optimisation.fast-approximate-counts
name: fast-approximate-counts
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, sql, query-anti-patterns, approximate-count, count-star, reltuples, explain-estimate, counter-table, hyperloglog-count]
level: practitioner
status: draft
description: "Avoid slow COUNT(*) on huge tables: catalog estimates (reltuples, sys.partitions, table_rows), EXPLAIN-based filtered estimates, counter tables, and capped counts for UIs."
sources:
  - https://wiki.postgresql.org/wiki/Count_estimate
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-partitions-transact-sql
  - https://dev.mysql.com/doc/refman/8.4/en/information-schema-tables-table.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fast approximate counts

**Goal:** "about 12.4M results" answered in milliseconds, with exact counts only
where the business needs them.

## Why COUNT(*) is slow
MVCC engines (PostgreSQL, InnoDB) cannot keep a single exact row count: each
transaction may see a different number, so `COUNT(*)` scans a table or index.
On 100M rows that is seconds to minutes.

## Whole-table estimates from the catalog
```sql
-- PostgreSQL (updated by VACUUM/ANALYZE)
SELECT reltuples::bigint FROM pg_class WHERE oid = 'public.events'::regclass;
-- SQL Server (exact-ish, maintained)
SELECT SUM(row_count) FROM sys.dm_db_partition_stats WHERE object_id = OBJECT_ID('dbo.events') AND index_id IN (0,1);
-- MySQL InnoDB (rough, can be off by 40%+)
SELECT table_rows FROM information_schema.tables WHERE table_schema='app' AND table_name='events';
```

## Filtered estimates
PostgreSQL: use the planner's estimate for any WHERE clause:
```sql
CREATE FUNCTION count_estimate(q text) RETURNS bigint LANGUAGE plpgsql AS $$
DECLARE plan jsonb;
BEGIN
  EXECUTE 'EXPLAIN (FORMAT JSON) ' || q INTO plan;
  RETURN (plan->0->'Plan'->>'Plan Rows')::bigint;
END $$;
SELECT count_estimate('SELECT 1 FROM events WHERE type = ''click''');
```
Only as good as statistics (see correlated columns); never pass user input unsanitised.

## When exactness matters
- **Counter table** maintained by triggers or the app (`UPDATE counters SET n = n + 1`):
  exact but a write hotspot; shard the counter (N rows, sum them) for high rates.
- **Capped count** for UIs: `SELECT count(*) FROM (SELECT 1 FROM events WHERE ... LIMIT 10001) t;`
  and show "10,000+".
- **Distinct counts** at scale: HyperLogLog (Redis PFCOUNT, `postgresql-hll`,
  BigQuery/ClickHouse approx functions).
- Index-only scans make exact counts faster (PostgreSQL needs a well-vacuumed visibility map).

## Gotchas
- `reltuples` is -1 for never-analyzed tables (PG14+).
- Pagination UIs rarely need total counts at all: keyset pagination plus "next" works.

## Verify
Compare estimate vs exact `COUNT(*)` occasionally off-peak; acceptable error for
the use case documented; endpoint latency no longer depends on table size.
