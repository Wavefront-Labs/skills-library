---
id: computing-software.database-administration.duckdb.duckdb-json-extraction-functions
name: duckdb-json-extraction-functions
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, json, json-extract, jsonpath, json-each, json-transform]
level: practitioner
status: docs-checked
description: "Query JSON in DuckDB: arrow operators, json_extract paths, json_transform to structs, json_each and json_tree, JSON aggregates, equality caveat."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/json/json_functions.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/json/caveats.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pull values out of JSON columns efficiently and correctly.

Extraction (operator forms need the `JSON` type, not VARCHAR):
- `json_extract(json, path)` / `->` returns JSON (alias `json_extract_path`). `json_extract_string` / `->>` returns VARCHAR (alias `json_extract_path_text`). `json_value(json,path)` returns NULL when the target is not a scalar. `json_exists(json,path)` returns a boolean.
- A `path` that is a LIST returns a LIST: `j->'species'->>['/0','/1']` gives `[duck, goose]`.
- Paths: JSON Pointer (`/duck/0`) or JSONPath (`$.duck[0]`). JSONPath also supports `[*]`, from-the-back `[#-1]`, and quoting `$."duck.goose"[1]`. Indices are 0-based in JSON, unlike SQL lists.
- Precedence gotcha: `->` binds loosely (lambda syntax). Write `((j->'field') = 42)` with parentheses.
- Several fields from one value: extract a list of paths once (`json_extract(j, ['family','species'])`, then index the list with 1-based `[1]`, `[2]`) instead of parsing the JSON repeatedly.

Inspection scalars: `json_array_length(json[,path])`, `json_contains(haystack, needle)` (string needle must include double quotes: `'"value"'`), `json_keys`, `json_structure`, `json_type` (ARRAY, BIGINT, BOOLEAN, DOUBLE, OBJECT, UBIGINT, VARCHAR, NULL), `json_valid` (the only one that does not error on invalid JSON), `json(x)` parse and minify.

Aggregates: `json_group_array(any)`, `json_group_object(key,value)`, `json_group_structure(json)`.

Transform to nested types in one pass:

```sql
SELECT json_transform(j, '{"family":"VARCHAR","coolness":"DOUBLE"}') FROM example;
```
`from_json` is an alias; missing keys become NULL; the `_strict` variants (`json_transform_strict`, `from_json_strict`) raise on a failed cast instead of returning NULL. The structure argument has the same form as the JSON returned by `json_structure`.

Table functions: `json_each(json[,path])` one row per top-level element; `json_tree(json[,path])` depth-first over everything. Columns: key, value, type, atom, id, parent, fullkey, path (virtual: json, root, rowid). They are lateral: `FROM example e, json_each(e.j, '$.species') je`.

Caveat: JSON equality is sometimes raw-text based, so `'[]'::JSON != '[ ]'::JSON` is true although content is equal.

## Checked

2026-11-07. Read the JSON Processing Functions and Caveats pages in full and confirmed the extraction functions, aliases and operators (JSON type required), list paths, JSON Pointer and JSONPath forms including `[#-1]` and quoted keys, 0-based indexing, arrow precedence, the multi-path extraction example, the scalar functions and json_type values, json_valid as the only non-erroring function, the aggregates, json_transform and its strict variants, json_each and json_tree columns and lateral use, and the equality warning. Reworded the structure-argument sentence, removed the unsupported advice to normalize with json() and removed the Verify step.

Method: documentation only; no commands were run.
