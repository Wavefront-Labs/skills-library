---
id: computing-software.database-administration.sql.sql-subqueries-scalar-correlated
name: sql-subqueries-scalar-correlated
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-subqueries, scalar-subquery, correlated-subquery, derived-table]
level: practitioner
status: docs-checked
description: "Use scalar, row, table and correlated subqueries and know when to replace them with joins or window functions."
sources: ["https://www.postgresql.org/docs/current/sql-expressions.html", "https://www.postgresql.org/docs/current/functions-subquery.html", "https://www.postgresql.org/docs/current/queries-table-expressions.html", "https://www.postgresql.org/docs/current/queries-with.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subqueries

- Scalar subquery: a parenthesised SELECT returning exactly one row and one column (PostgreSQL docs, 4.2.11). More than one row or column is an error; if it returns no rows during an execution there is no error and the scalar result is NULL.
- Derived table in FROM: the SQL standard requires a table alias (`FROM (SELECT ...) AS t`); PostgreSQL lets you omit `AS` and the alias, but write one for portability.
- Correlated subquery: it can refer to variables of the surrounding query, which act as constants during one evaluation of the subquery (so it runs per outer row). Whether the optimiser rewrites it into a join is not stated in the docs; check the plan.
- `IN` / `NOT IN` with NULLs: `NOT IN` yields NULL (not true) if the left side is NULL, or if there is no equal value and at least one subquery row is NULL, so the row is filtered out. `EXISTS` returns only true or false, never NULL, so use `NOT EXISTS` for anti-joins. `NOT IN` is equivalent to `<> ALL`.
- `ANY/SOME/ALL` compare against a set: `x > ALL (SELECT ...)`. Over an empty subquery, `IN` and `ANY` give false while `ALL` and `NOT IN` give true.
- Rewrite "latest per group" with a window function or a `LATERAL` subquery (which may reference preceding FROM items) rather than a correlated `MAX` subquery per row.
- CTE folding: a non-recursive, side-effect-free WITH query is folded into the parent by default if referenced once, and materialised if referenced more than once; override with `MATERIALIZED` or `NOT MATERIALIZED` (PostgreSQL docs, 7.8.3).

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the PostgreSQL pages for scalar subqueries, subquery expressions (9.24), table expressions (LATERAL, aliases) and WITH queries. Removed: the exact error message text, "most engines" alias claim, the optimiser decorrelation claim, the "equivalent for non-NULL values" claim, and the PostgreSQL 12 optimisation-fence claim (not on the cited pages).
