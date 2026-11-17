---
id: computing-software.database-administration.sql.searched-vs-simple-case
name: searched-vs-simple-case
category: computing-software
field: database-administration
product: sql
tags: [sql, searched-vs-simple-case]
level: intro
status: docs-checked
description: "Write CASE expressions correctly and avoid type and ordering mistakes."
sources: ["https://www.postgresql.org/docs/current/functions-conditional.html", "https://www.sqlite.org/lang_expr.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Simple versus searched CASE

- Searched: `CASE WHEN score >= 90 THEN 'A' WHEN score >= 80 THEN 'B' ELSE 'C' END`; simple: `CASE status WHEN 'x' THEN 1 END`.
- The first true condition wins and the rest are not processed; with no ELSE and no true condition the result is NULL.
- In PostgreSQL all result expressions must be convertible to a single output type.
- Simple CASE compares the base expression to each WHEN value for equality, evaluating the base once. SQLite states that a NULL base expression always yields the ELSE result (or NULL), and a NULL condition counts as untrue, so `CASE col WHEN NULL` never matches; use `WHEN col IS NULL` in a searched CASE.
- PostgreSQL does not evaluate subexpressions not needed for the result, so CASE can guard a division (`WHEN x <> 0 THEN y/x`), but constant subexpressions can still be evaluated early at planning time.
- Self-check: test a NULL input and a value matching no branch.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual page functions-conditional.html (CASE) and the SQLite lang_expr.html page (CASE expression); the NULL base-expression rule is from the SQLite page because the PostgreSQL page does not describe it.
