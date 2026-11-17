---
id: computing-software.data-engineering.snowflake.copy-into-options-and-validation
name: copy-into-options-and-validation
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, copy-into, validation-mode, on-error, load-history, copy-history, match-by-column-name, purge, force, file-format, bulk-loading]
level: practitioner
status: docs-checked
description: "Bulk load with Snowflake COPY INTO: ON_ERROR, VALIDATION_MODE dry runs, 64-day load metadata, FORCE, MATCH_BY_COLUMN_NAME and COPY_HISTORY checks."
sources:
  - https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
  - https://docs.snowflake.com/en/user-guide/data-load-considerations-load
  - https://docs.snowflake.com/en/sql-reference/functions/copy_history
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# COPY INTO: options and validation

**Goal:** load staged files idempotently, catch bad files before they half-load, and know exactly what loaded.

## File format
```sql
create file format raw.landing.csv_std
  type = csv field_delimiter = ',' skip_header = 1
  field_optionally_enclosed_by = '"' null_if = ('', 'NULL')
  empty_field_as_null = true error_on_column_count_mismatch = true
  encoding = 'UTF8' compression = auto;
```
Parquet/JSON/Avro/ORC formats for semi-structured; `binary_as_text`, `strip_outer_array` (JSON) where relevant.

## Dry run first
```sql
copy into raw.orders from @raw.landing.orders_stage
  file_format = (format_name = 'raw.landing.csv_std')
  pattern = '.*orders_2026-10-15.*[.]csv[.]gz'
  validation_mode = return_errors;          -- or return_<n>_rows / return_all_errors; validates, does not load
```

`VALIDATION_MODE` does not work with a COPY that transforms via SELECT, nor with `MATCH_BY_COLUMN_NAME`.

## Load
```sql
copy into raw.orders (order_id, amount, ordered_at, _file, _loaded_at)
from (select $1, $2, $3, metadata$filename, current_timestamp() from @raw.landing.orders_stage)
  file_format = (format_name = 'raw.landing.csv_std')
  pattern = '.*2026-10-15.*'
  on_error = abort_statement;
```
Parquet with matching names: `match_by_column_name = case_insensitive` (no transformation select needed; the two cannot be combined). The `error_on_column_count_mismatch` format option is ignored when the COPY uses a SELECT.

## ON_ERROR
| Option | Effect |
|---|---|
| `abort_statement` (default for bulk COPY) | Nothing loads if any error |
| `skip_file` / `skip_file_<n>` / `skip_file_<n>%` | Skip whole bad files |
| `continue` | Load good rows, skip bad rows (silent data loss unless you check) |
Snowpipe defaults to `skip_file`. Whatever you choose, check results.

## Idempotency: load metadata
Snowflake keeps load metadata per table (file name, size, ETag, rows parsed, last load time, errors) for **64 days** and skips already-loaded files on re-run: re-running COPY is safe. Caveats:
- `force = true` reloads everything matched (duplicates).
- Files older than 64 days with unknown load status are skipped unless `load_uncertain_files = true`.
`purge = true` tries to delete successfully loaded files from the stage; if the purge fails no error is returned, so `LIST` the stage periodically.

## Check what happened
```sql
select file_name, status, row_count, row_parsed, first_error_message, last_load_time
from table(information_schema.copy_history(table_name => 'RAW.ORDERS', start_time => dateadd(hour, -24, current_timestamp())));
select * from table(validate(raw.orders, job_id => '_last'));   -- all errors of the last COPY in this session; no results for on_error=abort_statement
```
The Information Schema function covers only the last 14 days and `COPY_HISTORY` omits statements that aborted; for longer history use the COPY_HISTORY view in Account Usage.

## Verify
- [ ] Running the same COPY twice loads 0 rows the second time.
- [ ] Every load job's `copy_history` status is LOADED; partial loads alert.
- [ ] Row counts match source manifests.

## Checked
2026-11-09. Confirmed against the COPY INTO <table> reference (ON_ERROR values and defaults, VALIDATION_MODE values, FORCE, PURGE, LOAD_UNCERTAIN_FILES, MATCH_BY_COLUMN_NAME), "Loading data" (64-day load metadata), and the COPY_HISTORY and VALIDATE function pages (14-day window, STATUS values, _last, no results with ABORT_STATEMENT). Removed: MD5 checksum detail, changed-content reload claim, purge permission claim, and the 365-day/2-hour Account Usage figures (not on the pages read). Only the first three cited pages were read in full for the figures above; the file-format option names were matched by phrase search.
Method: documentation only; no commands were run.
