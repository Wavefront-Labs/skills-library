---
id: computing-software.database-administration.sqlite.csv-import-and-export-in-sqlite3-shell
name: csv-import-and-export-in-sqlite3-shell
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite3, sqlite3-cli, sqlite-import-csv, dot-import, dot-mode, csv-export, dot-once, data-loading]
level: practitioner
status: verified
description: "Load and export CSV with the sqlite3 shell (.import --csv --skip, .mode, .once), control column types by pre-creating tables, and load large files fast."
sources:
  - https://sqlite.org/cli.html#importing_files_as_csv_or_other_formats
  - https://sqlite.org/cli.html#export_to_csv
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSV import/export in the sqlite3 shell

**Goal:** get a CSV into a properly typed SQLite table, and query results out
as CSV, in a repeatable command line.

## Import
```bash
sqlite3 data.db <<'SQL'
CREATE TABLE IF NOT EXISTS sales (
  id INTEGER PRIMARY KEY, sold_at TEXT NOT NULL, region TEXT, amount REAL
) STRICT;
.import --csv --skip 1 sales.csv sales
SQL
```
- `--csv` sets CSV parsing for this import only (added in 3.32.0 with `--ascii` and `--skip`, per the release log); older: `.mode csv` first.
- If the table **does not exist**, the first row becomes column names and the columns get
  no declared type (3.54 `PRAGMA table_info` showed an empty type; values arrive as text):
  create the table first for real types.
- `--skip N` is applied before the column names are read: with a missing table,
  `--skip 1` made the second line the column names (`"1","2026-01-01",...`), so never
  combine `--skip` with an uncreated table.
- If the table exists, every row (including the header) is data: `--skip 1` drops the header.
- Other options: `--ascii`, `--schema temp`, `--colsep`/`--rowsep`, `-v` (prints the CREATE
  TABLE it runs and a summary such as `Added 3 rows with 0 errors using 5 lines of input`).
- Field count mismatches print a warning (`expected 4 columns but found 3 - filling the rest with NULL`,
  or `found 5 - extras ignored`) and the row is still imported, padded with NULL or truncated.

## Fast bulk loads
`.import` runs inside one transaction already. For huge files, also:
```sql
PRAGMA journal_mode = OFF; PRAGMA synchronous = OFF;   -- only for a throwaway initial load
```
then create indexes **after** the import, and `ANALYZE`.

## Export
```bash
sqlite3 -header -csv data.db "SELECT region, sum(amount) FROM sales GROUP BY region;" > by_region.csv
```
Inside the shell:
```
.headers on
.mode csv
.once by_region.csv
SELECT region, sum(amount) FROM sales GROUP BY region;
```
`.once` redirects only the next query; `.output file` until `.output` alone.
`.excel` opens the result in a spreadsheet app. Other modes: `json`, `markdown`, `table`, `box`, `insert <table>` (`.mode --list` shows the full set).
A NULL exports as an empty field and an empty string as `""`.

## Gotchas
- Empty CSV fields import as empty strings, not NULL (checked: `typeof(region)` is `text`
  for an empty field): fix with
  `UPDATE sales SET region = NULL WHERE region = '';` (or NULLIF in an INSERT ... SELECT from a staging table).
- Dates stay text; store ISO-8601 (`YYYY-MM-DD HH:MM:SS`) so they sort and work with date functions.
- Windows line endings and BOMs end up in the first/last column; strip them first.

## Verify
`SELECT count(*) FROM sales;` equals `wc -l sales.csv` minus the header;
`SELECT typeof(amount), count(*) FROM sales GROUP BY 1;` shows only `real`.
