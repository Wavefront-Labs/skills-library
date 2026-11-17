---
id: computing-software.database-administration.mysql.histograms-and-index-statistics
name: histograms-and-index-statistics
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, mysql-optimization, mysql-histograms, analyze-table, innodb-stats-persistent, index-statistics, cardinality, column-statistics]
level: advanced
status: verified
description: "Fix MySQL misestimates with persistent InnoDB index statistics (sample pages, ANALYZE TABLE) and column histograms for non-indexed or skewed columns."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/optimizer-statistics.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-persistent-stats.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Index statistics and histograms

**Goal:** the optimizer's row estimates match reality, so it picks the right
index and join order without hints.

## InnoDB index statistics
Persistent stats (default) sample `innodb_stats_persistent_sample_pages` (20)
leaf pages per index. On big or skewed tables 20 is too few:
```sql
ALTER TABLE orders STATS_SAMPLE_PAGES = 256;
ANALYZE TABLE orders;          -- recompute now (fast: samples, takes a brief lock)
SELECT index_name, stat_name, stat_value, sample_size
FROM mysql.innodb_index_stats WHERE table_name='orders';
SHOW INDEX FROM orders;        -- Cardinality column
```
Auto-recalc happens in the background after more than 10% of rows change (`innodb_stats_auto_recalc`, on by default; 8.4 manual), so statistics may lag a big DML. `innodb_stats_persistent_sample_pages` defaults to 20 (checked). With `STATS_SAMPLE_PAGES = 256` on a table of only 50 leaf pages, `sample_size` in `mysql.innodb_index_stats` was 50 (it cannot exceed the pages that exist).

## Histograms (8.0+) for non-indexed columns
Without an index, the optimizer guesses selectivity of `WHERE status='refunded'`
(fixed heuristics). A histogram gives the real distribution, which drives join
order and the `filtered` estimate:
```sql
ANALYZE TABLE orders UPDATE HISTOGRAM ON status, country WITH 64 BUCKETS;
SELECT column_name, JSON_EXTRACT(histogram,'$."histogram-type"') AS type,
       JSON_EXTRACT(histogram,'$."number-of-buckets-specified"') AS buckets
FROM information_schema.column_statistics WHERE table_name='orders';
ANALYZE TABLE orders DROP HISTOGRAM ON country;
```
Singleton type for few distinct values (`status`, `country`, `amt` came out singleton on 9.7.4), equi-height for many (`created_at` with 8 buckets). Bucket count is 1 to 1024, default 100. Histograms are
**not** maintained in the background. `ANALYZE TABLE ... UPDATE HISTOGRAM ON col WITH N BUCKETS AUTO UPDATE` only makes a later plain `ANALYZE TABLE` refresh that histogram (docs; 8.4 and later); refresh by hand after
big data changes. A column covered by a single-part unique index is refused (`The column 'id' is covered by a single-part unique index`). Effect seen on 9.7.4: for an unindexed `WHERE amt = 500` on 20,000 rows, EXPLAIN `filtered` was the 10.00 default guess before and 1.00 after the histogram (actual count 200 = 1%).

## When histograms do not help
- Columns with an index: the optimizer uses index dives
  (`eq_range_index_dive_limit`, 200) instead.
- Correlated predicates across columns: MySQL multiplies selectivities
  independently; a composite index is the fix.

## Gotchas
- Older advice says `ANALYZE TABLE` can wait behind long-running queries and stall new ones queued behind it. That did not reproduce on 9.7.4: with a `SELECT sleep(12)` running, and again with a transaction holding the table open, `ANALYZE TABLE` returned at once and a following `SELECT` was not blocked (the 8.4 ANALYZE TABLE page does not document such a wait). Still prefer a quiet period for big tables.
- MariaDB uses engine-independent statistics (`use_stat_tables`,
  `histogram_size`, `ANALYZE TABLE ... PERSISTENT FOR ALL`).

## Verify
`EXPLAIN ANALYZE` estimated rows now within a small factor of actual rows for the
problem query.
