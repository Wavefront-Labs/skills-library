---
id: computing-software.database-administration.duckdb.duckdb-from-first-table-functions
name: duckdb-from-first-table-functions
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, from-first, table-function, with-ordinality, file-query, alias]
level: intro
status: docs-checked
description: "Use DuckDB FROM-first syntax, query files by name, call table functions with WITH ORDINALITY, use prefix aliases and select whole rows as structs."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/from.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write short exploratory queries with DuckDB's FROM clause features.

FROM-first: put FROM before SELECT or drop SELECT entirely (`SELECT *` is implied).

```sql
FROM tbl;                                   -- = SELECT * FROM tbl
FROM tbl SELECT i, s;                       -- = SELECT i, s FROM tbl
FROM range(100) AS t(i) SELECT sum(t.i) WHERE i % 2 = 0;
```

Files and table functions: `FROM 'test.csv'` is translated to `read_csv('test.csv')`. Table functions return whole tables and can be used like tables: `read_csv`, `read_parquet`, `range`, `generate_series`, `repeat`, `unnest`, `glob`. Name columns in the alias: `FROM range(100) AS t(i)`.

`WITH ORDINALITY` works on all table functions and adds an integer column `ordinality` starting at 1:

```sql
SELECT * FROM read_csv('test.csv') WITH ORDINALITY;
```
Unlike `row_number()`, it can number one side of a join without sub-queries.

Aliases and rows:
```sql
SELECT tn.* FROM tn: tbl;          -- prefix alias form
SELECT * FROM schema_name.tbl;
SELECT t FROM t;                   -- whole row as a STRUCT in one column
SELECT t FROM (SELECT unnest(generate_series(41, 43)) AS x, 'hello' AS y) t;
SELECT * FROM (SELECT * FROM tbl);     -- subquery without an alias
SELECT * FROM tbl TABLESAMPLE 10%;     -- see duckdb-sample
```

## Checked

2026-11-07. Read the FROM and JOIN Clauses page and confirmed FROM-first with and without SELECT, the implicit `read_csv` for quoted file names, the table-function list, `WITH ORDINALITY` starting at 1, the prefix alias form, whole-row-as-struct and TABLESAMPLE examples. Reworded the subquery comment (the page shows an unaliased subquery but does not state a rule) and removed the Verify step.

Method: documentation only; no commands were run.
