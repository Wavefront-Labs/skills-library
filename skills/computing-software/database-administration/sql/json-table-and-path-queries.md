---
id: computing-software.database-administration.sql.json-table-and-path-queries
name: json-table-and-path-queries
category: computing-software
field: database-administration
product: sql
tags: [sql, json-table-and-path-queries]
level: advanced
status: docs-checked
description: "Query JSON with jsonpath and shred it to rows with JSON_TABLE."
sources: ["https://www.postgresql.org/docs/current/functions-json.html", "https://www.postgresql.org/docs/17/release-17.html", "https://www.postgresql.org/docs/12/release-12.html", "https://www.sqlite.org/json1.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL/JSON path and JSON_TABLE

- PostgreSQL 12 added the SQL/JSON path language. `jsonb_path_query(doc, '$.items[*] ? (@.qty > 1)')` returns every matching item as a row; a filter is written `? (condition)`.
- Operators: `doc @? path` is true if the path returns any item; `doc @@ path` returns the result of a path predicate check, e.g. `'{"a":[1,2,3,4,5]}'::jsonb @@ '$.a[*] > 2'`.
- PostgreSQL 17 added `JSON_TABLE`, usable in `FROM`: `JSON_TABLE(doc, '$.items[*]' COLUMNS (sku text PATH '$.sku', qty int PATH '$.qty'))`. `id FOR ORDINALITY` numbers the rows.
- PostgreSQL 17 also added `JSON_EXISTS`, `JSON_QUERY` and `JSON_VALUE`. Use `JSON_VALUE` only for a single scalar (several values are an error); use `JSON_QUERY` for objects or arrays.
- SQLite has no JSON_TABLE: use the table-valued `json_each` (immediate children) or `json_tree` (recursive) in `FROM`, plus `json_extract(doc, '$.a.b')`. These have been supported since SQLite 3.9.0.
- Check the server version (`SELECT version()`) before using the PostgreSQL 17 functions.
- Self-check: the shredded row count equals the array length.

## Checked

2026-11-08. Confirmed on the PostgreSQL JSON functions page: `jsonb_path_query`, filter syntax, `@?`, `@@`, the `JSON_TABLE` COLUMNS/PATH syntax, `FOR ORDINALITY`, and the `JSON_VALUE` versus `JSON_QUERY` guidance. The PostgreSQL 12 and 17 release notes confirm the version claims. The SQLite json1 page confirms `json_each`, `json_tree`, the path grammar and 3.9.0. Removed nothing; added the version attributions and the single-scalar rule.
Method: documentation only; no commands were run.
