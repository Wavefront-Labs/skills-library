---
id: computing-software.database-administration.duckdb.duckdb-json-create-and-export
name: duckdb-json-create-and-export
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, json, to-json, json-object, copy, json-serialize-sql]
level: practitioner
status: docs-checked
description: "Build JSON values in DuckDB (to_json, json_object, json_array, merge_patch), the JSON type semantics, write JSON with COPY, and serialize SQL to JSON."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/json/creating_json.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/json/json_type.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/json/writing_json.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/json/sql_to_and_from_json.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/copy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: produce JSON from SQL values, write it to files, and know how the JSON type behaves.

Creation functions:
- `to_json(any)` (aliases `json_quote`; `array_to_json` takes only LIST, `row_to_json` only STRUCT). LIST becomes an array; STRUCT and MAP become an object: `to_json({duck:42})` gives `{"duck":42}`.
- `json_array(a, b, ...)` gives `["duck",42,"goose",123]`.
- `json_object(k1, v1, ...)` needs an even number of arguments.
- `json_merge_patch(a, b)` merges two documents (`{"goose":123,"duck":42}` for the docs example).

JSON type: logically VARCHAR restricted to valid JSON, stored physically as VARCHAR. Consequences: `'unquoted'::JSON` fails (use `'"quoted"'::JSON`); whitespace and key order are significant for `=` (`'{ "a": 5 }'::JSON = '{"a":5}'::JSON` is false); duplicate keys are allowed; whitespace survives a roundtrip. Any DuckDB type casts to JSON and back, e.g. `'{"duck":42}'::JSON::STRUCT(duck INTEGER)`.

Write JSON files with COPY:

```sql
COPY cities TO 'cities.json';             -- newline-delimited objects
COPY (SELECT * FROM range(5) r(i)) TO 'numbers.json' (ARRAY true);   -- one JSON array
```
Default output is one object per line; `ARRAY true` wraps in an array. Read back with `COPY tbl FROM 'f.json' (ARRAY true)` (see duckdb-read-json-options).

SQL to JSON and back (SELECT statements only):
- `json_serialize_sql(varchar, skip_default := , skip_empty := , skip_null := , format := )` serializes semicolon-separated SELECTs to an AST; errors come back as `{"error":true,...}` rather than raising.
- `json_deserialize_sql(json)` returns SQL text; syntactic sugar such as `FROM x SELECT ...` is not preserved but meaning is.
- `json_execute_serialized_sql(varchar)` (table function, one statement at a time) runs it, in a separate query context so it cannot see uncommitted transaction changes. `PRAGMA json_execute_serialized_sql('...')` runs in the same context but needs a constant string, not a nested `json_serialize_sql(...)` call.

## Checked

2026-11-07. Read the Creating JSON, JSON Type, Writing JSON and SQL to/from JSON pages in full and confirmed the creation functions and aliases with their example outputs, the JSON type semantics (VARCHAR storage, whitespace and key order significant, duplicate keys, casts), the COPY to JSON example, and the serialize, deserialize and execute functions with their error, sugar and transaction-context behaviour. The ARRAY option and the ARRAY true read-back are on the COPY Statement page (added to sources). Removed the Verify step.

Method: documentation only; no commands were run.
