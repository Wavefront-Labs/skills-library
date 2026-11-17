---
id: computing-software.database-administration.sql.coalesce-nullif-patterns
name: coalesce-nullif-patterns
category: computing-software
field: database-administration
product: sql
tags: [sql, coalesce-nullif-patterns]
level: practitioner
status: docs-checked
description: "Use COALESCE for the first non-null value and NULLIF to turn a matching value into NULL, in PostgreSQL and SQLite."
sources: ["https://www.postgresql.org/docs/current/functions-conditional.html", "https://www.sqlite.org/lang_corefunc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# COALESCE and NULLIF patterns

- `COALESCE(a, b, ...)` returns its first non-null argument; arguments to the right of the first non-null one are not evaluated. The arguments must be convertible to a common type.
- `NULLIF(a, b)` returns NULL if `a` equals `b`, otherwise `a`; for example `x / NULLIF(y, 0)` treats a zero divisor as NULL.
- SQLite: `coalesce` takes two or more arguments, `ifnull` takes exactly two, and `nullif(X, Y)` returns X if they differ and NULL if they are the same.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
Read: the COALESCE and NULLIF sections of the PostgreSQL conditional-expressions page and the coalesce, ifnull and nullif entries of the SQLite core functions page.
Trimmed: the Oracle claim and the statement about text/integer errors (not on these pages).
