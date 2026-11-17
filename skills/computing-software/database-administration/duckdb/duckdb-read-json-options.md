---
id: computing-software.database-administration.duckdb.duckdb-read-json-options
name: duckdb-read-json-options
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, json, read-json, ndjson, import, schema-inference]
level: practitioner
status: docs-checked
description: "Load JSON into DuckDB with read_json, read_ndjson and read_json_objects: format and records settings, schema-inference limits, COPY FORMAT json."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/json/loading_json.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/json/format_settings.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/json/overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read JSON files of any layout into columns, with the right `format` and `records` settings.

Quick forms (the `json` extension auto-loads):

```sql
SELECT * FROM 'todos.json';
CREATE TABLE todos AS SELECT * FROM read_json('todos.json');
SELECT filename, * FROM 'todos-*.json';   -- filename virtual column since 1.3.0
```

Table functions: `read_json` (alias `read_json_auto`), `read_ndjson` (= `format='newline_delimited'`). Raw object readers returning one `json` column: `read_json_objects`, `read_ndjson_objects`, `read_json_objects_auto`.

`format`: `auto`, `unstructured` (concatenated top-level values, may span lines), `newline_delimited` (NDJSON, one value per line), `array` (one top-level array of elements). The parameter table lists the default as `array` for the `read_json_objects` family; `read_json_objects_auto` is the alias with `format` set to `auto`. Naming `format` explicitly is always possible.

`records`: `auto` (default), `true` (unpack objects into columns), `false` (keep each value in a single `json` column, needed for non-object JSON such as `[1,2,3]` lines).

read_json parameters (default): `auto_detect` true; `columns` struct (if you give a subset, only those columns are returned); `sample_size` 20480 (-1 = all); `maximum_depth` -1; `maximum_object_size` 16777216 bytes; `maximum_sample_files` 32; `dateformat`/`timestampformat` `iso`; `compression` auto_detect (none, gzip, zstd); `ignore_errors` false (only with newline_delimited); `union_by_name` false; `hive_partitioning`; `map_inference_threshold` 200 (a struct with more subfields becomes MAP; -1 disables); `field_appearance_threshold` 0.1 (rarely-present fields collapse to MAP). Missing keys become NULL, JSON arrays become LIST.

```sql
SELECT * FROM read_json(['b1.json','b2.json'],
  columns = {duck:'INTEGER', goose:'INTEGER[]', swan:'DOUBLE'});
```

COPY: `COPY numbers FROM 'numbers.json' (ARRAY true);` (default expects NDJSON), `(AUTO_DETECT true)` to detect (COPY's `auto_detect` defaults false), `convert_strings_to_integers` available.

Gotchas: JSON-type indexing is 0-based while LIST/ARRAY are 1-based. JSON extraction supports only `.key` and `[index]` JSONPath (plus JSON Pointer); keys containing `[` or `.` are written in double quotes inside the path, e.g. `'$."d[u]"'`. See duckdb-json-extraction-functions.

## Checked

2026-11-07. Read the DuckDB 1.4 docs pages data/json/loading_json.md, data/json/format_settings.md and data/json/overview.md in full. Confirmed: quick forms, the function and alias tables, `format` values, `records` values and their effect, every read_json parameter and default listed (including `map_inference_threshold` 200 and `field_appearance_threshold` 0.1), subset `columns` behaviour, missing keys NULL and arrays LIST, COPY `ARRAY true`, `AUTO_DETECT true` and `convert_strings_to_integers`, 0-based JSON indexing, JSONPath/JSON Pointer support, the quoted-key rule. Reworded: the `format` default and `read_json_objects` sentence to match the parameter table. Removed the invented Verify step.

Method: documentation only; no commands were run.
