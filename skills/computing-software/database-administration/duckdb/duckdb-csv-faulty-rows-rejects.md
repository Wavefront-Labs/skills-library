---
id: computing-software.database-administration.duckdb.duckdb-csv-faulty-rows-rejects
name: duckdb-csv-faulty-rows-rejects
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, csv, ignore-errors, store-rejects, data-cleaning]
level: practitioner
status: docs-checked
description: "Read malformed CSV in DuckDB: error types, ignore_errors, and capturing bad lines in the reject_scans and reject_errors temp tables."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/csv/reading_faulty_csv_files.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/csv/overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: load what is valid from a broken CSV and find out exactly which lines failed and why.

Error types the scanner detects: `CAST` (value does not fit the column type), `MISSING COLUMNS`, `TOO MANY COLUMNS`, `UNQUOTED VALUE`, `LINE SIZE OVER MAXIMUM` (`max_line_size`), `INVALID ENCODING`. By default the first error aborts the read with a message that gives the line number, original line, and suggested fixes (override the type, `sample_size=-1`, or use COPY into a typed table).

Skip bad rows:

```sql
FROM read_csv('faulty.csv', columns={'name':'VARCHAR','age':'INTEGER'}, ignore_errors=true);
```
Gotcha: projection pushdown applies. `SELECT name FROM read_csv(...)` never casts `age`, so a row with a bad age is still returned.

Capture bad rows:

```sql
FROM read_csv('faulty.csv', columns={'name':'VARCHAR','age':'INTEGER'}, store_rejects=true);
FROM reject_scans;    -- scanner settings per scan/file
FROM reject_errors;   -- one row per error
```
Options: `store_rejects` (false), `rejects_scan` (table name, default `reject_scans`), `rejects_table` (default `reject_errors`), `rejects_limit` (max faulty lines recorded per file; 0 = no limit). Both are temporary tables. A line with several errors yields several rows.

`reject_errors` columns: scan_id, file_id, line, line_byte_position, byte_position, column_idx, column_name, error_type, csv_line, error_message. `reject_scans` columns: scan_id, file_id, file_path, delimiter, quote, escape, newline_delimiter, skip_rows, has_header, columns, date_format, timestamp_format, user_arguments. Join on scan_id and file_id.

Typical clean-up: `SELECT line, csv_line, error_message FROM reject_errors WHERE error_type='CAST';` then fix the source or re-read that column as VARCHAR via `types={'age':'VARCHAR'}`.

## Checked

2026-11-07. Read the Reading Faulty CSV Files page in full and confirmed the options and defaults, the two temporary rejects tables, the several-rows-per-line behaviour and the examples. Removed the advice to copy the temporary tables with CREATE TABLE AS and the Verify step, neither of which the page states.

Method: documentation only; no commands were run.
