---
id: computing-software.database-administration.sql.cte-chaining-and-reuse
name: cte-chaining-and-reuse
category: computing-software
field: database-administration
product: sql
tags: [sql, cte-chaining-and-reuse]
level: intro
status: docs-checked
description: "Structure complex queries as a chain of named CTE steps."
sources: ["https://www.postgresql.org/docs/current/queries-with.html", "https://www.sqlite.org/lang_with.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chaining multiple CTEs for readable queries

- `WITH a AS (...), b AS (SELECT ... FROM a), c AS (...) SELECT ... FROM b JOIN c ...;` one `WITH` clause can define several CTEs, and a later CTE can use an earlier one (the PostgreSQL example uses `regional_sales` inside `top_regions`).
- Name each step for what it returns; keep each step doing one transformation.
- A CTE exists only for one statement (PostgreSQL: "temporary tables that exist just for one query"; SQLite: "a view that exists for the duration of a single statement"). To reuse a result across statements, make a view or temp table instead.
- Gotcha: deep chains can hide an expensive step; EXPLAIN when slow.
- Self-check: run each CTE alone as `SELECT * FROM step` to validate intermediate rows.

## Checked

Date: 2026-11-07. Read the opening, the regional_sales example and the closing passages of the PostgreSQL WITH Queries page (queries-with; recursive section located by search only) and the Overview, "Ordinary Common Table Expressions" and MATERIALIZED passages of the SQLite WITH page (lang_with; read the matching passages, not the whole page). Confirmed: multiple CTEs in one WITH, output of one CTE used by the next, CTE lifetime of a single statement. No claims removed; wording tightened to the page text and the docs-root sources replaced by the two pages.
Method: documentation only; no commands were run.
