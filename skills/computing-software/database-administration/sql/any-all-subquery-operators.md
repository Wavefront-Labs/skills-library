---
id: computing-software.database-administration.sql.any-all-subquery-operators
name: any-all-subquery-operators
category: computing-software
field: database-administration
product: sql
tags: [sql, any-all-subquery-operators]
level: advanced
status: docs-checked
description: "Compare a value against a subquery with ANY, SOME and ALL."
sources: ["https://www.postgresql.org/docs/current/functions-subquery.html", "https://www.postgresql.org/docs/current/functions-comparisons.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ANY SOME and ALL comparison operators

- `x > ALL (SELECT v FROM t)` is true if x exceeds every v, and true when the subquery returns no rows. SOME is a synonym for ANY; IN is equivalent to `= ANY`, and NOT IN to `<> ALL`.
- PostgreSQL also takes array expressions: `x = ANY (ARRAY[1,2,3])`; ALL over an array with zero elements is also true.
- Self-check: test against an empty subquery result.

## Checked

2026-11-02. Confirmed in the PostgreSQL subquery expressions page and row and array comparisons page: ALL true for no rows, SOME synonym of ANY, IN as = ANY, NOT IN as <> ALL, array forms. Removed: the bind-parameter form, NULL-result and SQLite claims.
Method: documentation only; no commands were run.
