---
id: computing-software.database-administration.sql.sql-case-coalesce-nullif
name: sql-case-coalesce-nullif
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-case-expression, coalesce, nullif, conditional-logic]
level: intro
status: docs-checked
description: "Write CASE, COALESCE and NULLIF expressions for conditional values and safe division."
sources: ["https://www.postgresql.org/docs/current/functions-conditional.html", "https://www.sqlite.org/lang_expr.html", "https://www.sqlite.org/lang_corefunc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CASE, COALESCE, NULLIF

- Searched form: `CASE WHEN cond THEN v ... ELSE d END`. Simple form: `CASE x WHEN 1 THEN ...`, which compares `x` to each value for equality (like a C switch). The first matching branch wins and the rest is not processed. Without `ELSE`, no match gives NULL. A NULL condition counts as not true.
- In PostgreSQL all result expressions must be convertible to a single output type.
- `CASE` can appear wherever an expression is valid, so it works in `ORDER BY`, in `UPDATE ... SET col = CASE ...` and inside aggregates.
- PostgreSQL and SQLite evaluate only the subexpressions a `CASE` needs, but PostgreSQL warns this is not ironclad: a constant `1/0` inside a never-taken arm can still fail at planning time. Prefer `n / NULLIF(d, 0)`, which returns NULL instead of a divide-by-zero error.
- `NULLIF(a, b)` returns NULL when `a = b`, otherwise `a`. It is the inverse of `COALESCE(x, default)`. In PostgreSQL the result type is that of the implied `=` operator's first argument, so `NULLIF(1, 2.2)` is numeric. SQLite's `nullif` uses the collating function of whichever argument defines one, else BINARY.
- `COALESCE(a, b, c)` returns the first non-NULL argument (NULL only if all are NULL) and, like `CASE`, stops evaluating at the first non-NULL. In PostgreSQL the arguments must share a common type. It is the SQL-standard counterpart of `NVL` and `IFNULL`. SQLite needs at least 2 arguments; its `ifnull(X,Y)` equals a two-argument `coalesce`.
- SQLite also has `iif(x,y,z)`, equivalent to `CASE WHEN x THEN y ELSE z END`.
- NULL-safe comparison: `IS DISTINCT FROM` / `IS NOT DISTINCT FROM`. SQLite also accepts the shorter `IS` / `IS NOT`, which is an SQLite extension.
- `GREATEST` and `LEAST` in PostgreSQL ignore NULL arguments, which deviates from the SQL standard.

## Checked

2026-11-08. Read in full: PostgreSQL section 9.18 Conditional Expressions, SQLite "Expressions" section 7 (CASE) and the `IS DISTINCT FROM` paragraph, SQLite core functions (`coalesce`, `ifnull`, `iif`, `nullif`). Removed the unsupported claims about "subtly different typing rules" of `ISNULL`/`NVL` and the "constant-fold" wording.
Method: documentation only; no commands were run.
