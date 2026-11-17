---
id: computing-software.database-administration.duckdb.duckdb-set-operations
name: duckdb-set-operations
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, union, union-by-name, intersect, except, set-operations]
level: practitioner
status: docs-checked
description: "Combine DuckDB queries with UNION, INTERSECT and EXCEPT in set or ALL (bag) form, and UNION BY NAME to match columns by name with NULL fill."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/setops.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: combine result sets and know when duplicates are kept.

Vanilla `UNION`, `INTERSECT`, `EXCEPT` use set semantics (remove duplicates). The `ALL` variants use bag semantics (keep duplicates). Positional operations need the same number of columns, may implicitly cast to a common type (error if impossible) and take column names from the first query.

```sql
SELECT * FROM range(2) t1(x) UNION     SELECT * FROM range(3) t2(x);  -- 0,1,2 (any order)
SELECT * FROM range(2) t1(x) UNION ALL SELECT * FROM range(3) t2(x);  -- 0,1,0,1,2
SELECT * FROM range(2) t1(x) INTERSECT SELECT * FROM range(6) t2(x);  -- 0,1
SELECT * FROM range(5) t1(x) EXCEPT    SELECT * FROM range(2) t2(x);  -- 2,3,4
```

Bag semantics:
```sql
SELECT unnest([5,5,6,6,6,6,7,8]) AS x INTERSECT ALL SELECT unnest([5,6,6,7,7,9]);  -- 5,6,6,7
SELECT unnest([5,5,6,6,6,6,7,8]) AS x EXCEPT ALL    SELECT unnest([5,6,6,7,7,9]);  -- 5,8,6,6
```
`EXCEPT` returns rows that occur only in the left query. The page's own outputs are not sorted (UNION shows 2,1,0), so add `ORDER BY` if order matters.

`UNION [ALL] BY NAME` matches columns by name instead of position; the inputs may have different column counts and missing columns are filled with NULL. Plain `UNION BY NAME` removes duplicates, `UNION ALL BY NAME` keeps them.

```sql
CREATE TABLE capitals (city VARCHAR, country VARCHAR);
CREATE TABLE weather (city VARCHAR, degrees INTEGER, date DATE);
SELECT * FROM capitals UNION BY NAME SELECT * FROM weather;   -- columns city, country, degrees, date
```

## Checked

2026-11-07. Read the DuckDB 1.4 docs page sql/query_syntax/setops.md in full. Confirmed: set versus bag semantics, positional matching with same column count, implicit casts and error when impossible, first query's column names, all six example queries and their results, `UNION [ALL] BY NAME` with NULL fill and different column counts, set versus bag behaviour of BY NAME, the capitals/weather example columns, EXCEPT meaning. Changed: replaced the "row order not guaranteed" statement with what the page shows (unsorted example output); removed the invented Verify step.

Method: documentation only; no commands were run.
