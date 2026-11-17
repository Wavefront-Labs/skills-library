---
id: computing-software.database-administration.sql.lateral-unnest-functions
name: lateral-unnest-functions
category: computing-software
field: database-administration
product: sql
tags: [sql, lateral-unnest-functions]
level: advanced
status: docs-checked
description: "Expand arrays and JSON per row with LATERAL set-returning functions."
sources: ["https://www.postgresql.org/docs/current/queries-table-expressions.html", "https://www.postgresql.org/docs/current/functions-array.html", "https://www.sqlite.org/json1.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LATERAL with set-returning functions

- In PostgreSQL a function in `FROM` may reference earlier `FROM` items without writing `LATERAL` (the keyword is optional for functions): `FROM t, unnest(t.tags) AS tag`.
- `unnest(array)` expands an array into rows in storage order. Adding `WITH ORDINALITY` appends a `bigint` column numbering rows from 1, named `ordinality` unless aliased.
- `LEFT JOIN LATERAL unnest(t.tags) AS tag ON true` keeps source rows for which the function returns no rows, with NULLs in the function columns.
- Multi-array `unnest(a, b)` is only allowed in `FROM`; shorter arrays are padded with NULLs.
- SQLite equivalent: `FROM t, json_each(t.doc)` (supported since 3.9.0); `json_tree` walks recursively.
- Self-check: the row count equals the sum of array lengths.

## Checked

2026-11-08. Confirmed on the PostgreSQL table expressions page: optional `LATERAL` for functions, `LEFT JOIN LATERAL ... ON true`, `WITH ORDINALITY`. Confirmed on the PostgreSQL array functions page: `unnest` behaviour and multi-array padding. Confirmed on the SQLite json1 page: `json_each`/`json_tree` in `FROM`, 3.9.0. Removed the `jsonb_array_elements` name (not on any page read) and the claim about NULL arrays (the array page is silent on it).
Method: documentation only; no commands were run.
