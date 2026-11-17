---
id: computing-software.database-administration.sql.jsonb-operators-and-indexes
name: jsonb-operators-and-indexes
category: computing-software
field: database-administration
product: sql
tags: [sql, jsonb-operators-and-indexes]
level: advanced
status: docs-checked
description: "Query jsonb with -> ->> @> and index it with GIN."
sources: ["https://www.postgresql.org/docs/current/datatype-json.html", "https://www.postgresql.org/docs/current/functions-json.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jsonb operators and GIN indexes

- `doc->'a'` returns jsonb for a jsonb document, `doc->>'a'` returns text, `doc #>> '{a,b}'` walks a path, `doc @> '{"k":1}'` tests containment, `doc ? 'key'` tests key existence.
- `CREATE INDEX ON t USING gin (doc jsonb_path_ops)` supports `@>`, `@?` and `@@` but not the key-exists operators.
- `jsonb` keeps only the last value of duplicate keys and does not preserve key order or whitespace; `json` stores an exact copy of the input text.
- Self-check: EXPLAIN shows the GIN index being used.

## Checked

2026-11-02. Confirmed: the -> / ->> / #>> / @> operators (JSON functions page); jsonb_path_ops operator support, and jsonb versus json storage behaviour (JSON types page). Removed: the expression b-tree suggestion and the Bitmap Index Scan detail.
Method: documentation only; no commands were run.
