---
id: computing-software.database-administration.duckdb.duckdb-friendly-sql
name: duckdb-friendly-sql
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, friendly-sql, syntax-sugar, top-n, trailing-comma, lateral-alias, dialect]
level: practitioner
status: docs-checked
description: "Index of DuckDB friendly SQL shortcuts (FROM-first, GROUP BY ALL, prefix aliases, lateral column aliases, trailing commas) and the max(val, n) top-N-per-group idiom."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/dialect/friendly_sql.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the shortest DuckDB spelling for common SQL tasks.

Clauses: `CREATE OR REPLACE TABLE` (no DROP IF EXISTS), CTAS, `INSERT INTO ... BY NAME`, `INSERT OR IGNORE/REPLACE`, `DESCRIBE`, `SUMMARIZE`, FROM-first with optional SELECT, `GROUP BY ALL`, `ORDER BY ALL`, `SELECT * EXCLUDE/REPLACE`, `UNION BY NAME`, prefix aliases (`x: 42` for `42 AS x`, also in FROM), `LIMIT 10%`, `PIVOT` / `UNPIVOT`, SQL variables `SET VARIABLE` / `RESET VARIABLE`.

Query features: column aliases usable in `WHERE`, `GROUP BY` and `HAVING` (not in a JOIN's `ON` clause); `COLUMNS()` (regex, EXCLUDE/REPLACE, lambda); reusable lateral column aliases, e.g. `SELECT i + 1 AS j, j + 2 AS k FROM range(0, 3) t(i)`; `FILTER` clause; `GROUPING SETS` / `CUBE` / `ROLLUP`; `count()` shorthand for `count(*)`; `IN` for lists and maps; column names for CTEs and in JOIN; `VALUES` in JOIN and in the anchor part of CTEs.

Literals: identifiers are case-insensitive while the catalog keeps the original case; identifier deduplication; underscores as digit separators (`1_000`). Types: `MAP`, `UNION`. Import: CSV auto-detection, query files directly (`FROM 'my.csv'`, `'my.csv.gz'`, `'my.parquet'`), globbing (`FROM 'my-data/part-*.parquet'`), Python data frames via `FROM df`.

Functions: dot chaining (`SELECT ('hello').upper()`), `format()` with fmt syntax, `printf()`, list comprehensions, list and string slicing with negative index (`[-1]`), `STRUCT.*`, `[...]` list literals. Joins: ASOF, LATERAL, POSITIONAL.

Trailing commas are allowed in select lists and list literals:

```sql
SELECT 42 AS x, ['a', 'b', 'c',] AS y, 'hello world' AS z,;
```

Top-N per group without window functions: `max(arg, n)`, `min(arg, n)`, `arg_max(arg, val, n)`, `arg_min`, `max_by(arg, val, n)`, `min_by` return the top n as a list:

```sql
SELECT max(val, 3) FROM t1 GROUP BY grp;     -- grp a: [3,2,1], grp b: [6,5,4]
```
The conventional alternative is `array_agg` over `row_number() OVER (PARTITION BY grp ORDER BY val DESC)` filtered by `rid < 4`.

## Checked

2026-11-07. Read the Friendly SQL page in full and confirmed every listed clause, query feature, literal, type, import, function and join item, the trailing-comma example, the six top-N aggregate functions and the t1 example with its [3, 2, 1] and [6, 5, 4] results. Changed 'recursive CTE anchors' to the page's 'anchor part of common table expressions', and removed the pointer to QUALIFY (not on the page) and the Verify step.

Method: documentation only; no commands were run.
