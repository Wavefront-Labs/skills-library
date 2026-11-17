---
id: computing-software.database-administration.query-optimisation.recursive-ctes
name: recursive-ctes
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, sql, advanced-sql, recursive-cte, common-table-expressions, with-recursive, hierarchical-query, cte-materialization, cycle-detection]
level: practitioner
status: gated
description: "Write CTEs and WITH RECURSIVE queries for hierarchies and series, control CTE materialisation, and guard against cycles and runaway recursion."
sources:
  - https://www.postgresql.org/docs/current/queries-with.html
  - https://dev.mysql.com/doc/refman/8.4/en/with.html
  - https://learn.microsoft.com/en-us/sql/t-sql/queries/with-common-table-expression-transact-sql
  - https://www.sqlite.org/lang_with.html
  - https://www.postgresql.org/docs/16/queries-with.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common table expressions and recursive queries

**Goal:** readable multi-step SQL, and tree/graph walks in one query without app-side loops.

## Plain CTEs
```sql
WITH recent AS (
  SELECT customer_id, sum(total) AS spend FROM orders WHERE created_at >= now() - interval '30 days' GROUP BY 1
)
SELECT c.name, r.spend FROM recent r JOIN customers c ON c.id = r.customer_id ORDER BY r.spend DESC LIMIT 10;
```
Materialisation: PostgreSQL 12+ inlines single-reference, side-effect-free CTEs; force with `AS MATERIALIZED` / `AS NOT MATERIALIZED`. Before 12 every CTE was an optimisation fence. SQL Server always inlines (CTE referenced twice = computed twice: use a temp table) (gated: unconfirmed, source is paywalled or blocked). MySQL 8 may merge or materialise (gated: unconfirmed, source is paywalled or blocked). Checked on PostgreSQL 16.4 with EXPLAIN: a single-reference CTE is inlined (plain Seq Scan), `AS MATERIALIZED` gives a CTE Scan, and a CTE referenced twice is materialised by default.

## Recursive: walk a tree
```sql
WITH RECURSIVE subordinates AS (
  SELECT id, manager_id, name, 1 AS depth, ARRAY[id] AS path   -- anchor
  FROM employees WHERE id = 42
  UNION ALL
  SELECT e.id, e.manager_id, e.name, s.depth + 1, s.path || e.id  -- recursive member
  FROM employees e JOIN subordinates s ON e.manager_id = s.id
  WHERE s.depth < 20 AND NOT e.id = ANY(s.path)                    -- depth cap + cycle guard
)
SELECT * FROM subordinates ORDER BY path;
```
- PostgreSQL 14+: `CYCLE id SET is_cycle USING path` and `SEARCH DEPTH FIRST BY id SET ord` (both run on 16.4; `CYCLE` flagged the repeated row, and when both are used `SEARCH` must come before `CYCLE`). The path/ARRAY query above returned the 5-level subtree, and with a deliberate cycle the `NOT e.id = ANY(s.path)` guard stopped it at 5 rows.
- SQL Server: no `RECURSIVE` keyword; `OPTION (MAXRECURSION 1000)` (the option exists per Microsoft docs; the default of 100 is (gated: unconfirmed, source is paywalled or blocked)).
- MySQL: `cte_max_recursion_depth` (default 1000 (gated: unconfirmed, source is paywalled or blocked)).
- Index the join column (`employees(manager_id)`) or each level scans the table.

## Series and gaps
```sql
WITH RECURSIVE d(day) AS (SELECT date '2026-10-01' UNION ALL SELECT day + 1 FROM d WHERE day < date '2026-10-31')
SELECT d.day, coalesce(count(o.id), 0) FROM d LEFT JOIN orders o ON o.created_at::date = d.day GROUP BY d.day ORDER BY 1;
```
(PostgreSQL also has `generate_series`.)

## Gotchas
- `UNION` (not ALL) in a recursive CTE dedups rows each step: stops simple cycles but is slower; it does not catch cycles when path columns differ.
- Recursive CTEs over large graphs explode; for deep hierarchies queried often consider closure tables or `ltree`.

## Verify
Recursive result row count equals the subtree size computed independently; a deliberately inserted cycle terminates.
