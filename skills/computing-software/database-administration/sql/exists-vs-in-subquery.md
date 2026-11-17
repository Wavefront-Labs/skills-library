---
id: computing-software.database-administration.sql.exists-vs-in-subquery
name: exists-vs-in-subquery
category: computing-software
field: database-administration
product: sql
tags: [sql, exists-vs-in-subquery]
level: practitioner
status: docs-checked
description: "Choose EXISTS or IN for membership tests and know the NULL behaviour."
sources: ["https://www.postgresql.org/docs/current/functions-subquery.html", "https://www.sqlite.org/lang_expr.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Correlated EXISTS versus IN

- `WHERE EXISTS (SELECT 1 FROM o WHERE o.cid = c.id)` is true if the subquery returns at least one row and false otherwise, so it is never NULL. PostgreSQL generally runs the subquery only long enough to find one row, but says not to depend on that (avoid side effects in the subquery). The select list is normally unimportant; `SELECT 1` is a convention.
- `WHERE c.id IN (SELECT cid FROM o)` gives true if any equal row is found; if none is found and the subquery contains a NULL (or the left side is NULL), the result is NULL, not false. With no NULLs it matches the EXISTS form. PostgreSQL defines `IN` as `= ANY`.
- `NOT IN` is never true when the subquery contains a NULL and no equal value, so the WHERE returns no rows for those cases; use `NOT EXISTS`. PostgreSQL defines `NOT IN` as `<> ALL`.
- SQLite: `IN`/`NOT IN` follow the same NULL matrix, and `EXISTS` returns 1 or 0 and treats rows with NULLs like any other.
- Self-check: insert one NULL into the subquery source and re-run NOT IN versus NOT EXISTS.

## Checked

Date: 2026-11-07. Read the whole PostgreSQL Subquery Expressions page (9.24: EXISTS, IN, NOT IN, ANY, ALL) and sections 8 (IN and NOT IN, with its result matrix) and 10 (EXISTS) of the SQLite Expressions page (rest of that page located by search only). Confirmed the NULL behaviour, IN = ANY, NOT IN = <> ALL, and EXISTS true/false only. Removed: "modern planners turn both into semi-joins" (not on either page) and the "stops at the first match" absolute (the page says "generally"). Corrected "NOT IN returns no rows if the subquery yields any NULL": the page says the result is NULL rather than true only when no equal value exists.
Method: documentation only; no commands were run.
