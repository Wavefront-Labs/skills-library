---
id: computing-software.database-administration.duckdb.duckdb-create-table
name: duckdb-create-table
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, create-table, ctas, temp-table, generated-columns, foreign-key, check]
level: practitioner
status: docs-checked
description: "Create DuckDB tables: constraints, CTAS from files, schema-only copies, temp tables, CREATE OR REPLACE, foreign key limits and virtual generated columns."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/create_table.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define tables correctly, including the limits that bite.

```sql
CREATE TABLE t1 (
    i INTEGER NOT NULL DEFAULT 0,
    decimalnr DOUBLE CHECK (decimalnr < 10),
    date DATE UNIQUE,
    time TIMESTAMP
);
CREATE TABLE t2 (id INTEGER, j VARCHAR, PRIMARY KEY (id, j));   -- composite key
CREATE OR REPLACE TABLE t1 (i INTEGER, j INTEGER);   -- drop + create
CREATE TABLE IF NOT EXISTS t1 (i INTEGER, j INTEGER); -- no-op if exists
```

CTAS (can read files directly, FROM-first):
```sql
CREATE TABLE flights AS FROM 'https://duckdb.org/data/flights.csv';
CREATE OR REPLACE TABLE t1 AS SELECT * FROM read_csv('path/file.csv');
```
Schema-only copy: `CREATE TABLE t1 AS FROM t2 WITH NO DATA;` or `... LIMIT 0`. Only names and types are copied (no indexes, constraints, defaults). CTAS cannot declare constraints such as primary keys or CHECKs.

Temporary tables: `CREATE TEMP TABLE` / `CREATE TEMPORARY TABLE`. Session-scoped, dropped when the connection closes, live in schema `temp.main`, and are held in memory even for a persistent database. They win name resolution over a same-named regular table (then use `memory.main.t1`). Set `SET temp_directory = '/path/to/directory/';` so they can spill to disk under memory pressure.

CHECK: column form `CHECK (0 <= percentage AND percentage <= 100)` or named `CONSTRAINT x_smaller_than_y CHECK (x < y)`; violation gives `Constraint Error: CHECK constraint failed: t1`.

FOREIGN KEY: `FOREIGN KEY (t1_id) REFERENCES t1 (id)`; composite keys supported; may reference a `UNIQUE` column. Limits: `ON DELETE CASCADE` is not supported; inserting into tables with self-referencing foreign keys is not supported.

Generated columns: `two_x AS (2 * x)` or `two_x FLOAT GENERATED ALWAYS AS (2 * x) VIRTUAL`. Type may be inferred; cannot be inserted into; only `VIRTUAL` (computed at read time, the default) is currently supported, `STORED` is not.

## Checked

2026-11-07. Read the CREATE TABLE Statement page in full and confirmed the column and constraint examples, CREATE OR REPLACE and IF NOT EXISTS, CTAS from files and URLs, schema-only copies, the no-constraints CTAS limit, temporary table behaviour (temp.main, priority, memory-resident, `temp_directory` spill), CHECK and FOREIGN KEY examples and limits, and generated columns (only VIRTUAL supported). Removed the Verify step.

Method: documentation only; no commands were run.
