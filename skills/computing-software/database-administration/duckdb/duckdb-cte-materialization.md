---
id: computing-software.database-administration.duckdb.duckdb-cte-materialization
name: duckdb-cte-materialization
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, cte, with, materialized, not-materialized, inlining, performance]
level: advanced
status: docs-checked
description: "Control whether a DuckDB WITH CTE is evaluated once (MATERIALIZED) or inlined at each reference (NOT MATERIALIZED), and know the inlining heuristics."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/with.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand and, when needed, override how DuckDB executes common table expressions.

Basics: `WITH cte AS (SELECT 42 AS x) SELECT * FROM cte;` CTEs are scoped views; they can reference each other (`WITH cte1 AS (...), cte2 AS (SELECT i * 100 AS x FROM cte1)`) and can be nested. Column names can be given: `WITH cte(j) AS (SELECT 42 AS i) FROM cte;`.

Default: a CTE is materialized (evaluated once, stored in a temporary table). DuckDB may inline it (duplicate its definition at each reference, no temp table) when the heuristics hold:
- it is not referenced more than once,
- it contains no `VOLATILE` function,
- it is declared `AS NOT MATERIALIZED` and not `AS MATERIALIZED`,
- it does not perform a grouped aggregation.

Inlining is not always possible even if these hold, for example a CTE containing `read_csv` cannot be inlined.

Overrides:

```sql
-- evaluate the expensive query once, reuse thrice
WITH t(x) AS MATERIALIZED (<complex_query>)
SELECT * FROM t AS t1, t AS t2, t AS t3;

-- duplicate the definition at each reference
WITH t(x) AS NOT MATERIALIZED (<complex_query>)
SELECT * FROM t AS t1, t AS t2, t AS t3;
```

Guidance from the docs: explicit hints are generally not recommended because the optimizer decides from the structure and the heuristics; materializing helps when an expensive query is referenced several times, since it is then evaluated only once.

For recursion see `duckdb-with-recursive`.

## Checked

2026-11-07. Read the WITH Clause page in full and confirmed the basics, the materialization default, the inlining heuristics, the read_csv exception and the MATERIALIZED and NOT MATERIALIZED examples. Removed the Verify step.

Method: documentation only; no commands were run.
