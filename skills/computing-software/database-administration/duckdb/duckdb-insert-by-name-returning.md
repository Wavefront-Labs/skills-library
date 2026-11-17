---
id: computing-software.database-administration.duckdb.duckdb-insert-by-name-returning
name: duckdb-insert-by-name-returning
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, insert, by-name, by-position, returning, default]
level: practitioner
status: docs-checked
description: "Control DuckDB INSERT column mapping with BY POSITION / BY NAME and read generated values back with RETURNING."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/insert.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: map insert values to columns safely and capture generated values.

Column order: `BY POSITION` is the default and associates VALUES / query columns with the table (or an explicit column list) left to right. Columns not covered get their declared default, else `NULL`. If a value is not of the correct data type, automatic type conversion is attempted.

```sql
CREATE TABLE tbl (a INTEGER, b INTEGER);
INSERT INTO tbl VALUES (5, 42);            -- a=5, b=42
INSERT INTO tbl (b, a) VALUES (5, 42);     -- b=5, a=42
INSERT INTO tbl BY POSITION (b, a) VALUES (5, 42);   -- same as above
INSERT INTO tbl (a) VALUES (1), (DEFAULT), (3);      -- explicit DEFAULT allowed
```

`BY NAME` matches the SELECT output names to table column names, so order and missing columns do not matter:

```sql
INSERT INTO tbl BY NAME (SELECT 42 AS b, 32 AS a);
INSERT INTO tbl BY NAME (SELECT 22 AS b);   -- a becomes NULL (or its default)
```

A misspelled or non-existent name is an error. Missing columns take the default.

`RETURNING` returns the inserted rows, useful for sequence-generated keys or computed columns. It accepts `*`, aliased expressions, and `*` plus extra expressions (no aggregates):

```sql
CREATE TABLE t2 (i INTEGER, j INTEGER);
INSERT INTO t2 SELECT 2 AS i, 3 AS j RETURNING *, i * j AS i_times_j;

CREATE TABLE t3 (i INTEGER PRIMARY KEY, j INTEGER);
CREATE SEQUENCE 't3_key';
INSERT INTO t3 SELECT nextval('t3_key') AS i, 42 AS j
  UNION ALL SELECT nextval('t3_key'), 43 RETURNING *;   -- i = 1, 2
```

For conflict handling see `duckdb-insert-on-conflict-upsert`.

## Checked

2026-11-07. Read the INSERT Statement page in full and confirmed BY POSITION as default, the default-or-NULL fill rule, the column-list and explicit DEFAULT examples, BY NAME matching with the misspelling error and missing-column defaults, RETURNING with `*`, aliases, extra expressions and no aggregates, and the sequence example returning 1 and 2 (the page uses 42 and 43 for j). Reworded the type-conversion sentence to 'attempted' and removed the Verify step.

Method: documentation only; no commands were run.
