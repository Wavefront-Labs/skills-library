---
id: computing-software.database-administration.duckdb.duckdb-copy-from-import
name: duckdb-copy-from-import
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, copy, import, csv, parquet, json, load]
level: intro
status: docs-checked
description: "Load CSV, Parquet or JSON files into an existing DuckDB table with COPY ... FROM, including column lists, auto-detect and path expressions."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/copy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: append file data to an existing table with `COPY ... FROM`.

Rules: the data is appended to what is already in the table. Without a column list, the file column count must equal the table column count and values must be castable to the column types, else an error is thrown. With a column list, only those columns are filled and the others get their default values.

```sql
COPY test FROM 'test.csv';                          -- CSV options auto-detected
COPY category FROM 'categories.csv' (HEADER);
COPY lineitem FROM 'lineitem.tbl' (DELIMITER '|');
COPY lineitem FROM 'lineitem.tbl' (AUTO_DETECT true);   -- delimiter, quote, header
COPY category(name) FROM 'names.csv';               -- other columns get defaults
COPY lineitem FROM 'lineitem.pq' (FORMAT parquet);
COPY lineitem FROM 'lineitem.ndjson' (FORMAT json);  -- newline-delimited JSON
COPY lineitem FROM 'lineitem.json' (FORMAT json, ARRAY true);  -- JSON array file
```

Format comes from the file extension unless `FORMAT` is given. Path quoting is flexible: `'f.csv'`, `"f.csv"` and bare `f.csv` all work.

Dynamic paths: put an expression in parentheses.

```sql
SET VARIABLE source_file = 'lineitem.json';
COPY lineitem FROM (getvariable('source_file'));
PREPARE v1 AS COPY lineitem FROM ($1);
EXECUTE v1('lineitem.json');
```

Postgres-compatible spelling is accepted: `COPY tbl FROM 'tbl.csv' WITH DELIMITER '|' CSV HEADER;`.

Related: the write side is `duckdb-copy-to-file-options`.

## Checked

2026-11-07. Read the COPY Statement page in full and confirmed the append rule, column-count and castability rule, column-list behaviour, all listed COPY ... FROM examples (CSV, HEADER, DELIMITER, AUTO_DETECT, Parquet, NDJSON, ARRAY true), flexible path quoting, parenthesised expression and prepared-statement sources, and the PostgreSQL-compatible spelling. Removed the claim that COPY does not transform data and the INSERT ... SELECT alternative (not on the page) and the Verify step.

Method: documentation only; no commands were run.
