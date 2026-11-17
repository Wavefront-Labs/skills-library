---
id: computing-software.database-administration.duckdb.duckdb-read-csv-options
name: duckdb-read-csv-options
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, csv, read-csv, copy, import, ingestion]
level: practitioner
status: docs-checked
description: "Load CSV files in DuckDB with read_csv or COPY: key parameters, defaults, schema overrides, and when to pick COPY over read_csv."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/csv/overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read a CSV into DuckDB correctly, overriding only the options the sniffer gets wrong.

Basic forms:

```sql
SELECT * FROM 'flights.csv';                       -- options auto-inferred
SELECT * FROM read_csv('flights.csv', delim='|', header=true,
    columns={'FlightDate':'DATE','UniqueCarrier':'VARCHAR'});
CREATE TABLE ontime AS FROM 'flights.csv';
COPY ontime FROM 'flights.csv' (DELIMITER '|', HEADER);
```

`COPY ... FROM` loads into an existing table: create the table first with the correct schema (matching the CSV's column order and fitting its values); `COPY` detects the CSV's configuration options automatically. `columns` disables auto detection of the schema.

Parameters (name, default):
- `delim`/`sep` `,` (up to 4 bytes); `quote` `"`; `escape` `"`; `header` false; `skip` 0 lines.
- `names`/`column_names` list of names; `types`/`dtypes`/`column_types` list (by position) or struct (by name); `all_varchar` false.
- `nullstr`/`null` (string or list), `force_not_null` (columns where empty is not NULL), `null_padding` false (pad short rows with NULL), `allow_quoted_nulls` true.
- `dateformat`, `timestampformat` (strptime-style), `decimal_separator` `.`, `thousands` (single char, differs from decimal separator).
- `compression` auto (none/gzip/zstd from extension), `encoding` utf-8 (also utf-16, latin-1; other encodings need the `encodings` extension or iconv), `comment`, `new_line`, `normalize_names` false.
- `sample_size` 20480 lines, `auto_type_candidates` (default list `['NULL','BOOLEAN','BIGINT','DOUBLE','TIME','DATE','TIMESTAMP','VARCHAR']`, VARCHAR always a fallback), `max_line_size` 2000000 bytes, `buffer_size`, `parallel` true.
- `union_by_name` false (align multi-file schemas by name; costs memory), `hive_partitioning`, `filename` (virtual column since 1.3.0).
- `strict_mode` true: false lets the parser read structurally broken files but can be ambiguous.
- Error handling: `ignore_errors`, `store_rejects`, `rejects_table`, `rejects_scan`, `rejects_limit` (see duckdb-csv-faulty-rows-rejects).

In COPY, `date_format`, `timestamp_format`, `delimiter` are the alias names; `all_varchar`, `encoding`, `max_line_size` are not available there.

Gotchas: with `preserve_insertion_order` true (default) rows return in file order; set false to allow reordering. Stdin (page example): `cat flights.csv | duckdb -c "SELECT * FROM read_csv('/dev/stdin')"`. See duckdb-csv-sniffer-auto-detection for how the dialect is detected.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page data/csv/overview.md in full. Confirmed: basic forms, the parameter table (defaults and aliases for delim/sep, quote, escape, header, skip, names, types, all_varchar, nullstr, force_not_null, null_padding, allow_quoted_nulls, dateformat, timestampformat, decimal_separator, thousands, compression, encoding, comment, new_line, normalize_names, sample_size, auto_type_candidates default list, max_line_size 2000000, buffer_size, parallel, union_by_name, hive_partitioning, filename, strict_mode, rejects parameters), COPY-only aliases and unavailable options, encodings tip, preserve_insertion_order. Removed: "(-1 = whole file)" for sample_size, "header false when not detected", the claim that COPY is faster and avoids detection mistakes, and the invented Verify step.

Method: documentation only; no commands were run.
