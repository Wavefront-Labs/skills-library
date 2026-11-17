---
id: computing-software.database-administration.duckdb.duckdb-csv-sniffer-auto-detection
name: duckdb-csv-sniffer-auto-detection
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, csv, sniff-csv, auto-detection, types, dateformat]
level: practitioner
status: docs-checked
description: "How DuckDB's CSV sniffer detects dialect, types, header and date formats, and how to inspect or override it with sniff_csv and sample_size."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/csv/auto_detection.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand and steer what `read_csv` infers, and fix wrong guesses with the smallest override.

Run the sniffer alone:

```sql
FROM sniff_csv('my_file.csv');
FROM sniff_csv('my_file.csv', sample_size = 1000);
.mode line
SELECT Prompt FROM sniff_csv('my_file.csv');   -- ready-to-paste read_csv(..., auto_detect=false, ...) call
```
Output columns: Delimiter, Quote, Escape, NewLineDelimiter, Comment, SkipRows, HasHeader, Columns (list of name/type structs), DateFormat, TimestampFormat, UserArguments, Prompt.

Sampling: default `sample_size` is 20,480 rows; `-1` reads the whole file. Regular files are sampled from several locations; non-seekable inputs (.gz, stdin) are sampled only from the start, so a late-appearing value can break the inferred type.

Dialect candidates: `delim` in `,` `|` `;` tab; `quote` in `"` `'` (none); `escape` in `"` `'` `\` (none). The winner has a consistent column count per row and the highest column count.

Type detection: each column starts with all candidates; a failed cast removes one. Priority order: NULL, BOOLEAN, TIME, DATE, TIMESTAMP, TIMESTAMPTZ, BIGINT, DOUBLE, VARCHAR. Extra candidates only via `auto_type_candidates`: TINYINT, SMALLINT, INTEGER, DECIMAL, FLOAT. Quoting does not change detection ("42" is still numeric). `all_varchar = true` disables detection.

Override types: `types = ['INTEGER','VARCHAR','DATE']` (by position) or `types = {'quarter':'INTEGER'}` (by name); any valid type is allowed here. Use `typeof()` or DESCRIBE `column_type` to copy valid names, or the `Columns` field of sniff_csv.

Header: detected when the first row differs in types from the rest. If every column is VARCHAR the file is assumed to have a header; force with `header = false`. Headerless columns are named `column0`, `column1`, ...

Dates: ISO 8601 is default. Sniffer tries, in preference order for dates: `%y-%m-%d`, `%Y-%m-%d`, `%d-%m-%y`, `%d-%m-%Y`, `%m-%d-%y`, `%m-%d-%Y`; timestamps similarly with `%H:%M:%S` (and `%I:%M:%S %p`, `%f`). An ambiguous `01-02-2000` falls back to this order; set `dateformat`/`timestampformat` explicitly when wrong.

## Checked

2026-11-07. Read the CSV Auto Detection page in full and confirmed the detection steps, defaults and sniff_csv usage. Removed the Verify step, which the page does not state.

Method: documentation only; no commands were run.
