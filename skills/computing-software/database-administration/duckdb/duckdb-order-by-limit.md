---
id: computing-software.database-administration.duckdb.duckdb-order-by-limit
name: duckdb-order-by-limit
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, order-by, order-by-all, limit, offset, nulls-first, collation]
level: intro
status: docs-checked
description: "Sort and page DuckDB results: ORDER BY ALL, NULLS FIRST/LAST defaults and settings, COLLATE, plus LIMIT, OFFSET and percentage limits."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/orderby.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/limit.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: sort deterministically and restrict the number of rows.

ORDER BY is an output modifier applied near the end, just before LIMIT/OFFSET. Items are comma-separated and each is a scalar expression, a 1-based column position, or `ALL`. Each may take `ASC|DESC` (default ASC) and `NULLS FIRST|NULLS LAST` (default NULLS LAST, same as PostgreSQL). An empty ORDER BY is an error.

```sql
SELECT * FROM addresses ORDER BY city DESC NULLS LAST;
SELECT * FROM addresses ORDER BY city, zip;
SELECT * FROM addresses ORDER BY city COLLATE DE;   -- German collation
SELECT * FROM addresses ORDER BY ALL;               -- every column, left to right
SELECT * FROM addresses ORDER BY ALL DESC;
```
`ALL` must stand alone (not mixed with other expressions); it accepts ASC/DESC and NULLS modifiers.

Defaults can be changed:
```sql
SET default_null_order = 'NULLS_FIRST';  -- NULLS_FIRST, NULLS_LAST, NULLS_FIRST_ON_ASC_LAST_ON_DESC, NULLS_LAST_ON_ASC_FIRST_ON_DESC
SET default_order = 'DESC';              -- or 'ASC'
```
Text sorts by binary UTF-8 values by default, which can be wrong outside ASCII-style languages; use collations (see `duckdb-collations`).

LIMIT restricts rows; OFFSET skips the first N. Without ORDER BY the rows returned are not deterministic (fine for a quick peek).

```sql
SELECT * FROM addresses LIMIT 5;
SELECT * FROM addresses LIMIT 5 OFFSET 5;
SELECT * FROM addresses LIMIT 10%;      -- percentage
SELECT city, count(*) AS population FROM addresses GROUP BY city ORDER BY population DESC LIMIT 5;
```

## Checked

2026-11-07. Read the DuckDB 1.4 docs pages sql/query_syntax/orderby.md and sql/query_syntax/limit.md in full. Confirmed: ORDER BY placement before LIMIT/OFFSET, empty ORDER BY error, expression kinds, ASC and NULLS LAST defaults (same as PostgreSQL), ORDER BY ALL rules, `default_null_order` values, `default_order`, binary UTF-8 collation default, every example, LIMIT/OFFSET and `LIMIT 10%`, non-determinism without ORDER BY. Removed the invented Verify step. No other changes.

Method: documentation only; no commands were run.
