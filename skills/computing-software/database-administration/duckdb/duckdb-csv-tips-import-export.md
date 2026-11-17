---
id: computing-software.database-administration.duckdb.duckdb-csv-tips-import-export
name: duckdb-csv-tips-import-export
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, csv, copy, import, export, union-by-name]
level: intro
status: docs-checked
description: "Practical DuckDB CSV recipes: header and names overrides, partial type overrides, COPY into tables, union_by_name, INSERT BY NAME, and CSV export."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/csv/tips.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/guides/file_formats/csv_import.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/guides/file_formats/csv_export.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: handle the common CSV import and export jobs with the shortest correct statement.

Import into new or existing tables:

```sql
CREATE TABLE new_tbl AS FROM read_csv('input.csv');   -- FROM-first, no SELECT *
INSERT INTO tbl SELECT * FROM read_csv('input.csv');
COPY tbl FROM 'input.csv';                            -- uses tbl's schema, no type detection
```
`SELECT * FROM 'input.csv'` also works: the extension picks the reader.

Fixes for detection problems:
- Header not detected (all-string files): `read_csv('f.csv', header = true)`.
- No header, want names: `read_csv('f.csv', names = ['DateOfFlight','CarrierName'])`.
- Override only some types: `read_csv('f.csv', types = {'FlightDate': 'DATE'})` (struct of name to type).
- Wrong type from a late value: `sample_size = -1` makes the sniffer read the whole file.
- Prefer `COPY` into a pre-typed table when you know the schema; it speeds up detection and avoids mistakes.

Files with different schemas: `read_csv('flights*.csv', union_by_name = true)` fills missing columns with NULL (more memory than positional). When the target table has more columns than the file, name-match on insert:

```sql
INSERT INTO tbl BY NAME SELECT * FROM read_csv('input.csv');
```

Export:

```sql
COPY tbl TO 'output.csv' (HEADER, DELIMITER ',');
COPY (SELECT * FROM tbl) TO 'output.csv' (HEADER, DELIMITER ',');
```
Further COPY options are in the COPY statement docs (CSV options section). Related: duckdb-read-csv-options, duckdb-csv-sniffer-auto-detection.

## Checked

2026-11-07. Read the CSV Import Tips and CSV Export pages in full and confirmed the options and examples. Removed the Verify step, which the pages do not state.

Method: documentation only; no commands were run.
