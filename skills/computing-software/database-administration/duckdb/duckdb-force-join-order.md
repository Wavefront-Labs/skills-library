---
id: computing-software.database-administration.duckdb.duckdb-force-join-order
name: duckdb-force-join-order
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, joins, join-order, optimizer, disabled-optimizers, temporary-tables]
level: advanced
status: docs-checked
description: "Force a join order in DuckDB by disabling join_order and build_side_probe_side optimizers or staging results in temporary tables."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/guides/performance/join_operations.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/configuration/pragmas.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: override the cost-based join order when the optimizer's cardinality estimates are wrong.

Background: DuckDB has a cost-based query optimizer that uses statistics in the base tables (stored in a DuckDB database or Parquet files) to estimate the cardinality of operations.

Option 1, disable the optimizers so the plan is a left-deep tree in the order written:

```sql
SET disabled_optimizers = 'join_order,build_side_probe_side';
SELECT ...
FROM ...
JOIN ...  -- performed first
JOIN ...; -- performed second
SET disabled_optimizers = '';   -- restore afterwards
```
`join_order` turns off reordering; `build_side_probe_side` turns off left/right swapping. List valid optimizer names with `duckdb_optimizers()`. The docs warn that `disabled_optimizers` is for debugging performance and should be avoided in production, so reset it right after the query.

Option 2, break the query into stages with temporary tables so each step has real statistics:

```sql
CREATE OR REPLACE TEMPORARY TABLE t1 AS ...;
CREATE OR REPLACE TEMPORARY TABLE t2 AS SELECT * FROM t1 ...;
SELECT * FROM t2 ...;
DROP TABLE IF EXISTS t1;
DROP TABLE IF EXISTS t2;
```

## Checked

2026-11-07. Read the Join Operations and Pragmas pages in full and confirmed the cost-based optimizer statement, `SET disabled_optimizers = 'join_order,build_side_probe_side'`, the left-deep tree in JOIN clause order, resetting with an empty string, the temporary-table staging pattern and cleanup, `duckdb_optimizers()` for listing optimizers and the debugging-only warning. Removed unsupported claims (Parquet statistics being weaker, loading Parquet into tables fixing plans, the EXPLAIN ANALYZE diagnosis step), the related-advice line and the Verify step. The skill's last staging SELECT reads from t2 where the page's example reads from t1; kept as a sensible reading of the page's own comment.

Method: documentation only; no commands were run.
