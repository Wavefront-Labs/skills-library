---
id: computing-software.database-administration.sql.is-distinct-from
name: is-distinct-from
category: computing-software
field: database-administration
product: sql
tags: [sql, is-distinct-from]
level: practitioner
status: docs-checked
description: "Compare values treating NULL as a value with IS [NOT] DISTINCT FROM."
sources: ["https://www.postgresql.org/docs/current/functions-comparison.html", "https://www.sqlite.org/lang_expr.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IS DISTINCT FROM and null-safe equality

- `a IS DISTINCT FROM b` is true if different, treating two NULLs as equal; `IS NOT DISTINCT FROM` is the null-safe equals. SQLite accepts both forms and also spells them `IS NOT` / `IS`.
- Useful in change detection: `WHERE new.v IS DISTINCT FROM old.v`.
- Self-check: `SELECT NULL IS NOT DISTINCT FROM NULL` returns true.

## Checked

2026-11-02. Confirmed: IS [NOT] DISTINCT FROM semantics with NULL (PostgreSQL comparison functions page); SQLite's IS NOT DISTINCT FROM as an alternative spelling of IS (SQLite expressions page). Removed: the MySQL operator and the index-use remark.
Method: documentation only; no commands were run.
