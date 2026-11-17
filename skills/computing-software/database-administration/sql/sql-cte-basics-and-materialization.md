---
id: computing-software.database-administration.sql.sql-cte-basics-and-materialization
name: sql-cte-basics-and-materialization
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-cte, with-clause, cte-readability, not-materialized]
level: practitioner
status: docs-checked
description: "Structure queries with WITH common table expressions and understand materialisation and scoping."
sources: ["https://www.postgresql.org/docs/current/queries-with.html", "https://www.sqlite.org/lang_with.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common table expressions

- `WITH a AS (...), b AS (SELECT ... FROM a) SELECT ...`: a CTE is like a temporary table that exists for one statement, and a later CTE can read an earlier one. The point of a plain SELECT in WITH is to break a complicated query into simpler, named parts.
- The WITH clause can be attached to a SELECT, INSERT, UPDATE or DELETE in both PostgreSQL and SQLite (PostgreSQL also allows MERGE). In SQLite it must sit at the start of a top-level SELECT or of a subquery, not on the second or later SELECT of a compound select.
- Column list syntax: `WITH t(a, b) AS (...)`.
- PostgreSQL: a CTE is normally evaluated once per execution of the parent query, even if referenced several times. The optimiser cannot push restrictions from the parent into a CTE that is referenced more than once.
- PostgreSQL folds a non-recursive, side-effect-free CTE into the parent query by default when it is referenced once, not when referenced more than once. Override with `AS MATERIALIZED` (force a separate calculation, which also evaluates an expensive function once per row) or `AS NOT MATERIALIZED` (force merging; risks duplicate computation but can use an index on the parent's filter).
- SQLite 3.35.0 (2021-03-12) and later accept the same two keywords as non-binding planner hints. `MATERIALIZED` acts as an optimisation fence; `NOT MATERIALIZED` means "treat like an ordinary subquery" and does not forbid materialisation. SQLite recommends leaving the hints off without a compelling reason.
- Recursive form: non-recursive term, `UNION` or `UNION ALL`, then recursive term. In PostgreSQL `UNION` discards duplicate rows (a partial guard against loops); `UNION ALL` does not. SQLite does not enforce the SQL:1999 rule that `RECURSIVE` follow `WITH`, and a compound recursive-select needs 3.34.0 or later.
- Data-modifying CTEs (PostgreSQL only here): only on the top-level statement, run exactly once to completion, and see the same snapshot as the main query. `RETURNING` is the only way to pass changed rows on.
- Do not nest ten CTEs to hide a bad join; read the plan.

## Checked

2026-11-08. Read in full: PostgreSQL 7.8 WITH Queries (current docs). SQLite WITH clause page: the intro, ordinary and recursive CTE rules, materialization hints and notes sections (worked examples skimmed). Removed unsupported claims: PostgreSQL version number for inlining, behaviour of SQL Server, MySQL and Oracle (including the Oracle hint), "no indexes, no statistics" comparison with temp tables, and "references earlier CTEs only" as a blanket rule.
Method: documentation only; no commands were run.
