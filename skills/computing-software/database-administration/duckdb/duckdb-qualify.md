---
id: computing-software.database-administration.duckdb.duckdb-qualify
name: duckdb-qualify
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, qualify, window-functions, filtering, row-number, top-n-per-group]
level: practitioner
status: docs-checked
description: "Filter DuckDB window-function results directly with QUALIFY instead of a subquery or CTE, including placement, SELECT aliases and the WINDOW clause."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/qualify.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: filter on window function results (for example top-N per group) without wrapping the query in a CTE.

`QUALIFY` is to window functions what `HAVING` is to aggregates. Position in a SELECT: after the `WINDOW` clause (which is optional) and before `ORDER BY`. It filters on window functions in general, not only those defined in a `WINDOW` clause.

All four forms below return the same rows (first two function names per schema):

```sql
-- window expression written inside QUALIFY
SELECT schema_name, function_name,
       row_number() OVER (PARTITION BY schema_name ORDER BY function_name) AS function_rank
FROM duckdb_functions()
QUALIFY row_number() OVER (PARTITION BY schema_name ORDER BY function_name) < 3;

-- reference the SELECT alias
SELECT schema_name, function_name,
       row_number() OVER (PARTITION BY schema_name ORDER BY function_name) AS function_rank
FROM duckdb_functions()
QUALIFY function_rank < 3;

-- named window
SELECT schema_name, function_name, row_number() OVER my_window AS function_rank
FROM duckdb_functions()
WINDOW my_window AS (PARTITION BY schema_name ORDER BY function_name)
QUALIFY function_rank < 3;     -- or: QUALIFY row_number() OVER my_window < 3
```

The equivalent without QUALIFY is a `WITH ranked_functions AS (SELECT ... AS function_rank ...) SELECT * FROM ranked_functions WHERE function_rank < 3;`.

Note: in the first example the `function_rank` column in the SELECT list is only "for reference"; the filter is the window expression inside `QUALIFY`.

Related: `duckdb-order-by-limit`, window functions reference.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page sql/query_syntax/qualify.md in full. Confirmed: QUALIFY filters window function results like HAVING does for aggregates, avoids a subquery or WITH, the filter is on window functions not necessarily the WINDOW clause, position after WINDOW and before ORDER BY, all four example forms, the WITH equivalent and the output table. Removed: the claim about order of evaluation relative to WHERE (not on the page), the claim that QUALIFY works without the window function in the SELECT list (reworded to what the page says), and the invented Verify step.

Method: documentation only; no commands were run.
