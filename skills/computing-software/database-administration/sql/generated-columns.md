---
id: computing-software.database-administration.sql.generated-columns
name: generated-columns
category: computing-software
field: database-administration
product: sql
tags: [sql, generated-columns]
level: practitioner
status: docs-checked
description: "Define stored and virtual generated columns."
sources: ["https://www.postgresql.org/docs/current/ddl-generated-columns.html", "https://www.sqlite.org/gencol.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generated columns

- PostgreSQL: `total numeric GENERATED ALWAYS AS (qty * price) STORED`; use the keywords VIRTUAL or STORED to make the kind explicit (the current docs say a generated column is virtual by default; check your version's docs).
- SQLite 3.31.0 and later: `GENERATED ALWAYS AS (expr) VIRTUAL|STORED`; VIRTUAL is the default, and generated columns can participate in indexes.
- PostgreSQL expressions can use only immutable functions, no subqueries, nothing but the current row; SQLite allows only scalar deterministic functions on the same row.
- A generated column cannot be written directly.
- Self-check: change an input column and read the generated column.

## Checked

2026-11-02. Confirmed in the PostgreSQL generated-columns page and the SQLite generated-columns page: syntax and kinds, defaults, immutable/deterministic limits, no direct writes, SQLite 3.31.0 introduction, indexing. Removed: PostgreSQL 12 and 18 version attributions.
Method: documentation only; no commands were run.
