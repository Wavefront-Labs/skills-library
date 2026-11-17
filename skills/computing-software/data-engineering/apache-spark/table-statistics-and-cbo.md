---
id: computing-software.data-engineering.apache-spark.table-statistics-and-cbo
name: table-statistics-and-cbo
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark-sql, cost-based-optimizer, analyze-table, table-statistics, column-statistics, join-reorder, broadcast-threshold]
level: advanced
status: docs-checked
description: "Collect Spark table and column statistics with ANALYZE TABLE and turn on the cost-based optimizer for join reordering and better broadcast decisions."
sources:
  - https://spark.apache.org/docs/latest/sql-ref-syntax-aux-analyze-table.html
  - https://spark.apache.org/docs/latest/sql-performance-tuning.html
  - https://spark.apache.org/docs/latest/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table statistics and the cost-based optimizer

**Goal:** give Catalyst real sizes and cardinalities so it picks broadcast joins and join order correctly at planning time.

## Collect statistics
```sql
ANALYZE TABLE sales.orders COMPUTE STATISTICS;                         -- number of rows + size in bytes
ANALYZE TABLE sales.orders COMPUTE STATISTICS FOR COLUMNS customer_id, order_date;
ANALYZE TABLE sales.orders COMPUTE STATISTICS FOR ALL COLUMNS;
ANALYZE TABLE sales.orders PARTITION (dt='2026-10-17') COMPUTE STATISTICS;   -- partition statistics
ANALYZE TABLES IN sales COMPUTE STATISTICS NOSCAN;                     -- size only, cheap
```
Inspect:
```sql
DESCRIBE EXTENDED sales.orders;                 -- "Statistics" row, e.g. bytes and rows
DESCRIBE EXTENDED sales.orders customer_id;     -- min, max, num_nulls, distinct_count, avg_col_len, max_col_len, histogram
```

## Enable the CBO
```properties
spark.sql.cbo.enabled=true
spark.sql.cbo.joinReorder.enabled=true
spark.sql.cbo.joinReorder.dp.threshold=12
spark.sql.statistics.histogram.enabled=true      # equi-height histograms; costs an extra table scan
spark.sql.cbo.planStats.enabled=true             # logical plan fetches row counts and column stats from the catalog
```
```sql
EXPLAIN COST select ...;   -- plan nodes show estimated statistics
```

## When it matters
- Multi-way joins: `spark.sql.cbo.joinReorder.enabled` enables join reordering; `dp.threshold` (default 12) is the maximum number of joined nodes in the dynamic programming algorithm; `spark.sql.cbo.starSchemaDetection` is a separate option.
- Broadcast decisions use `spark.sql.autoBroadcastJoinThreshold` (default 10 MB; -1 disables broadcasting) against the estimated table size, so a bad size estimate gives a bad broadcast choice.
- `spark.sql.statistics.fallBackToHdfs` (default false) falls back to file sizes when table statistics are unavailable, for non-partitioned Hive tables.

## Keeping stats fresh
Stats are a snapshot. Re-run ANALYZE after large loads. A table that grew a lot but still has old statistics can look small enough to broadcast. `spark.sql.statistics.size.autoUpdate.enabled` (default false) updates table size when data changes, but can be slow for tables with very many files.

## Verify
- [ ] `EXPLAIN COST` shows row counts on scan nodes.
- [ ] Join order in the physical plan starts with the most selective dimension; no broadcast of a table larger than threshold.

## Checked
2026-11-09. Confirmed against the Spark ANALYZE TABLE page (syntax, NOSCAN, FOR COLUMNS, FOR ALL COLUMNS, partition spec, DESC EXTENDED column fields, `ANALYZE TABLES ... IN`), the SQL performance tuning page (`autoBroadcastJoinThreshold` default 10 MB, -1 disables) and the configuration page (`spark.sql.cbo.*` and `spark.sql.statistics.*` keys and defaults). Removed: the AQE timing claim, Delta, Databricks and Iceberg platform notes, the 4+ dimension rule, and daily/weekly refresh schedules.
Method: documentation only; no commands were run.
