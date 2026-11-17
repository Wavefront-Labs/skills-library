---
id: computing-software.database-administration.sql.null-in-aggregates-and-ordering
name: null-in-aggregates-and-ordering
category: computing-software
field: database-administration
product: sql
tags: [sql, null-in-aggregates-and-ordering]
level: practitioner
status: docs-checked
description: "Know how NULL behaves in aggregates, ORDER BY, UNIQUE and CHECK."
sources: ["https://www.postgresql.org/docs/current/functions-aggregate.html", "https://www.postgresql.org/docs/current/queries-order.html", "https://www.postgresql.org/docs/current/ddl-constraints.html", "https://www.sqlite.org/nulls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NULL in aggregates sorting and constraints

- `count(*)` counts input rows; `count(col)` counts rows where col is not NULL. `sum` and `avg` use only non-NULL inputs, and except for `count` the standard aggregates return NULL when no rows are selected (`sum` of nothing is NULL, not 0; wrap in `coalesce`).
- Sorting in PostgreSQL: NULLs sort as if larger than any non-NULL, so NULLS LAST is the default for ASC and NULLS FIRST for DESC; override with `NULLS FIRST|LAST`.
- UNIQUE: by default NULLs are not considered equal, so PostgreSQL permits several rows with NULL in a unique column; `UNIQUE NULLS NOT DISTINCT` changes that. SQLite likewise treats NULLs as distinct in a UNIQUE column, while its own comparison table notes Informix and MS-SQL treat them as indistinct.
- CHECK is satisfied when the expression evaluates to true or NULL, so add NOT NULL to forbid NULLs.
- Self-check: verify with a column containing NULLs and zeros.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual pages functions-aggregate.html, queries-order.html and ddl-constraints.html and the SQLite nulls.html page; the draft's SQLite/MySQL NULL sort-order and Oracle UNIQUE claims were dropped because none of these pages support them.
