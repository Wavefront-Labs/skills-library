---
id: computing-software.database-administration.sql.sql-json-and-semi-structured-data
name: sql-json-and-semi-structured-data
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-json, jsonb, sql-json-path, json-operators, generated-columns]
level: advanced
status: docs-checked
description: "Store and query JSON in PostgreSQL and SQLite: jsonb vs json, operators, SQL/JSON functions, GIN and expression indexes."
sources: ["https://www.postgresql.org/docs/current/datatype-json.html", "https://www.postgresql.org/docs/current/functions-json.html", "https://www.postgresql.org/docs/current/indexes-expressional.html", "https://www.sqlite.org/json1.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON in SQL

- PostgreSQL `jsonb` is stored in a decomposed binary format: slower to input, much faster to process, indexable. It does not preserve white space or key order and keeps only the last value of a duplicate key. `json` stores an exact copy of the input text and must be reparsed on each use. The manual says most applications should prefer `jsonb`.
- Operators: `->` (returns json/jsonb), `->>` (returns text), `#>` / `#>>` (path as `text[]`), `@>` containment, `?` top-level key or array element exists. Containment is nested; existence is top level only. `jsonb_path_query` and the `@?` / `@@` operators use SQL/JSON path.
- The PostgreSQL 18 manual documents the SQL/JSON query functions `JSON_EXISTS`, `JSON_QUERY`, `JSON_VALUE` and `JSON_TABLE` (which presents JSON as a relational view in `FROM`). `JSON_VALUE` returns SQL NULL for a JSON null; `JSON_QUERY` returns the JSON null.
- GIN index on a `jsonb` column: the default operator class supports `?`, `?|`, `?&`, `@>`, `@?`, `@@`; `jsonb_path_ops` supports only `@>`, `@?`, `@@` but is usually smaller and faster. `jsonb_path_ops` makes no entries for structures with no values such as `{"a": {}}`.
- An index is used only when the operator is applied directly to the indexed expression: `jdoc -> 'tags' ? 'qui'` cannot use a plain GIN index on `jdoc`, but can use `CREATE INDEX ... USING GIN ((jdoc -> 'tags'))`. Expression indexes cost extra on insert and non-HOT update. `jsonb` btree/hash indexes are mainly useful for whole-document equality.
- SQLite: JSON functions are built in from 3.38.0 (unless compiled out with `SQLITE_OMIT_JSON`); `json_extract`, the `->` and `->>` operators, and the table-valued `json_each` / `json_tree`.
- Keep JSON documents to a fairly fixed structure and a manageable size: any update takes a row-level lock on the whole row.
- Promote hot keys to real columns so you get types and constraints; an expression index on one key is the lighter alternative.
- `jsonb` numbers map to `numeric` (no precision loss in PostgreSQL), but other JSON implementations often use IEEE 754 doubles, so large ids exchanged with them can lose precision; send ids as strings.

## Checked

2026-11-08. Confirmed against the PostgreSQL 18 pages "JSON Types" (json vs jsonb, containment and existence, GIN operator classes, expression-index example, row-lock note, number precision note), "JSON Functions and Operators" (operators, JSON_EXISTS/QUERY/VALUE/TABLE, JSON null behaviour), "Indexes on Expressions", and the SQLite JSON page (built in from 3.38.0, `->`/`->>`, `json_each`/`json_tree`). Removed as unconfirmed: MySQL and SQL Server JSON claims (the MySQL manual is blocked to fetch), the claim that PostgreSQL 17 added the SQL/JSON functions (version not stated on the fetched pages), and "foreign keys cannot point inside JSON".
Method: documentation only; no commands were run.
