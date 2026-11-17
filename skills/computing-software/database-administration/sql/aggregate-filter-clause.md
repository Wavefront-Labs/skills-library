---
id: computing-software.database-administration.sql.aggregate-filter-clause
name: aggregate-filter-clause
category: computing-software
field: database-administration
product: sql
tags: [sql, aggregate-filter-clause]
level: practitioner
status: docs-checked
description: "Use aggregate FILTER (WHERE ...) to count or sum a subset in one pass."
sources: ["https://www.postgresql.org/docs/current/sql-expressions.html", "https://www.postgresql.org/docs/current/functions-aggregate.html", "https://www.sqlite.org/lang_aggfunc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FILTER clause on aggregates

- `count(*) FILTER (WHERE status = 'paid')` counts only rows for which the filter expression is true (PostgreSQL, SQLite).
- Gotcha: engines without FILTER need CASE; `count(CASE WHEN c THEN 1 END)` is the portable form because `count(expression)` skips NULLs.
- Self-check: the sum of filtered counts across disjoint filters equals `count(*)`.

## Checked

2026-11-02. Confirmed: FILTER (WHERE ...) syntax on an aggregate in PostgreSQL (SQL expressions page), and SQLite's FILTER clause includes only rows for which the expression is true (aggregate functions page). Removed: version numbers, MySQL and SQL Server claims, the claim that it works for every aggregate.
Method: documentation only; no commands were run.
