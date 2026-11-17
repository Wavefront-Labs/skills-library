---
id: computing-software.data-engineering.polars.sql-select-and-table-functions
name: sql-select-and-table-functions
category: computing-software
field: data-engineering
product: polars
tags: [polars, sql, select, group-by, join, read-csv, table-functions, polars-sql-select, hive-partitioning]
level: practitioner
status: docs-checked
description: "Write SELECT queries in Polars SQL and use read_csv, read_ndjson, read_parquet and read_ipc table functions with name => value options."
sources:
  - https://docs.pola.rs/user-guide/sql/select/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: query data with Polars SQL SELECT, including reading files directly in the FROM clause.

Basics (frames registered in a `SQLContext`, e.g. `ctx = pl.SQLContext(population=df, eager=True)`)
- `SELECT country, AVG(population) as avg_population FROM population GROUP BY country`
- `SELECT city, population FROM population ORDER BY population`
- Join after `ctx.register_many(income=income)`: `SELECT income.*, population.population FROM population LEFT JOIN income ON population.city = income.city`
- Functions include math (`ABS`, `EXP`, `LOG`, `ASIN`...), string (`LOWER`, `UPPER`, `LTRIM`, `RTRIM`, `STARTS_WITH`, `ENDS_WITH`), aggregates (`SUM`, `AVG`, `MIN`, `MAX`, `COUNT`, `STDDEV`, `FIRST`) and array functions (`EXPLODE`, `UNNEST`, `ARRAY_SUM`, `ARRAY_REVERSE`).

Table functions: `read_csv`, `read_parquet`, `read_ndjson`, `read_ipc`, `read_json` (path only). The path may be a glob or a list: `read_parquet(['a.parquet', 'b.parquet'])`.

Options go after the path as `name => value` or `name := value`, with the same names as the `scan_*` function:
```sql
SELECT * FROM read_csv('iris.csv', infer_schema => false, skip_rows_after_header => 147)
SELECT * FROM read_ndjson('orders.ndjson', schema_overrides => {'date': 'DATE'})
SELECT id, path FROM read_parquet('alltypes_plain.parquet', include_file_paths => 'path') LIMIT 3
```
Value syntax: `NULL` means `None` (`infer_schema_length => NULL` scans the whole file, `quote_char => NULL` disables quoting); lists use brackets (`new_columns => ['a','b']`); `schema`, `schema_overrides`, per-column `null_values` take dictionaries with SQL type names (`{'id': 'INT', 'name': 'VARCHAR'}`); escapes need `E''` (`separator => E'\t'`).

Per-function notes
- `read_csv` unlike `scan_csv` parses dates by default (`try_parse_dates => true`). Options marked unstable in the `scan_csv` reference are unstable here too.
- `read_ndjson`: schema inferred from the first 100 rows, so a later-appearing key is dropped; nested objects read as `'VARCHAR'` keep their JSON text. For JSON arrays or pretty-printed JSON use `pl.read_json`.
- `read_parquet`: unlike `scan_parquet`, hive partitions are read by default for a single path (glob or file too); every `key=value` folder counts, even in parent folders. A list reads them only if it is a single directory. Set `hive_partitioning` true or false explicitly. With several files, the first defines columns unless `schema` is given; use `missing_columns => 'insert'`, `extra_columns => 'ignore'`.
- `read_ipc` follows the same hive rules.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/sql/select/. Corrected: Corrected the description to name => value options. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
