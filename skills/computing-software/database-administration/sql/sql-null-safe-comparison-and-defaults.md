---
id: computing-software.database-administration.sql.sql-null-safe-comparison-and-defaults
name: sql-null-safe-comparison-and-defaults
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-null-handling, is-not-distinct-from, not-null-design, null-in-aggregates]
level: intro
status: docs-checked
description: "Handle NULL deliberately: IS NULL, NULL-safe equality, NOT IN pitfalls, sort order, aggregates and COALESCE defaults."
sources: ["https://www.postgresql.org/docs/current/functions-comparison.html", "https://www.postgresql.org/docs/current/functions-subquery.html", "https://www.postgresql.org/docs/current/queries-order.html", "https://www.postgresql.org/docs/current/functions-conditional.html", "https://www.sqlite.org/nulls.html", "https://www.sqlite.org/lang_aggfunc.html", "https://www.sqlite.org/lang_select.html", "https://www.sqlite.org/lang_expr.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NULL handling

- Ordinary comparisons yield NULL ("unknown"), not true or false, when either side is NULL: `7 = NULL` and `7 <> NULL` are both NULL, so `WHERE x = NULL` matches nothing. Write `x IS NULL` / `x IS NOT NULL`. Likewise `x <> 1` skips rows where `x` is NULL; add `OR x IS NULL` or use `x IS DISTINCT FROM 1`.
- `IS [NOT] DISTINCT FROM` treats NULL as an ordinary value: `NULL IS NOT DISTINCT FROM NULL` is true, `1 IS DISTINCT FROM NULL` is true, and for non-null inputs they behave like `<>` and `=`. PostgreSQL has these predicates SQLite accepts the same predicates and also the compact `IS` / `IS NOT`, which are SQLite extensions and never evaluate to NULL.
- `NOT IN (subquery)` returns NULL, not true, if the left side is NULL or if no right-hand value matches and at least one right-hand row is NULL. A single NULL in the subquery therefore empties the result; use `NOT EXISTS` or filter the NULLs out.
- Sorting: PostgreSQL treats NULL as larger than any value, so `NULLS LAST` is the default for ASC and `NULLS FIRST` for DESC. SQLite treats NULL as smaller than any value (first in ASC, last in DESC). Both accept `NULLS FIRST` / `NULLS LAST`; state it explicitly.
- Aggregates skip NULL inputs (`avg` averages non-null values; SQLite `count(X)` counts non-NULL values), while `count(*)` counts rows. Adding to or multiplying NULL gives NULL. `COALESCE(a, b, ...)` returns the first non-null argument and is the usual way to substitute a default.
- NULLs are distinct in a UNIQUE column (several NULL rows are allowed) in SQLite and PostgreSQL, but indistinct for `SELECT DISTINCT` and `UNION`. Other engines differ (SQLite's own comparison chart shows MS-SQL and Informix treat NULLs as indistinct in a UNIQUE column).
- Design: prefer `NOT NULL` with a sensible default; use NULL only for genuinely unknown or inapplicable values. Test queries with NULL rows in fixtures.

## Checked

2026-11-08. Confirmed against the PostgreSQL 18 pages "Comparison Functions and Operators" (NULL comparisons, IS DISTINCT FROM, `= NULL`), "Subquery Expressions" (NOT IN with nulls), "Sorting Rows" (NULL ordering defaults), "Conditional Expressions" (COALESCE), "Aggregate Functions" (non-null inputs), and the SQLite pages "NULL Handling in SQLite" (UNIQUE vs DISTINCT chart), "Aggregate Functions" (`count(X)` vs `count(*)`), "SELECT" (NULLs smaller than other values) and "Expressions" (`IS`, `IS DISTINCT FROM`). Removed as unconfirmed: MySQL and Oracle ordering defaults and "Oracle treats empty string as NULL".
Method: documentation only; no commands were run.
