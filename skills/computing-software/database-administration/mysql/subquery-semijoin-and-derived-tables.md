---
id: computing-software.database-administration.mysql.subquery-semijoin-and-derived-tables
name: subquery-semijoin-and-derived-tables
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, semijoin, antijoin, derived-table, derived-merge, materialization, firstmatch, loosescan, subquery-optimization]
level: practitioner
status: docs-checked
description: "Understand how MySQL optimizes IN/EXISTS subqueries (semijoin strategies, antijoin) and derived tables (merge vs materialize), and steer them with hints."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/semijoins.html
  - https://dev.mysql.com/doc/refman/8.4/en/subquery-optimization-with-exists.html
  - https://dev.mysql.com/doc/refman/8.4/en/derived-table-optimization.html
  - https://dev.mysql.com/doc/refman/8.4/en/optimizer-hints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subquery semijoin and derived table optimization

## Semijoin (IN / EXISTS subqueries)
`SELECT ... FROM customers c WHERE c.id IN (SELECT customer_id FROM orders WHERE total > 100)` is turned into a join that returns each customer once. Strategies, visible in EXPLAIN / optimizer trace:
| Strategy | EXPLAIN hint | Good when |
|---|---|---|
| Table pullout | subquery table becomes a normal join | unique key on the subquery side |
| FirstMatch | `FirstMatch(c)` | stop at first match per outer row |
| LooseScan | `LooseScan` | index on the subquery column allows reading distinct groups |
| Materialization | `<subquery2>`, `MATERIALIZED` | subquery result small; built once into a temp table with index |
| DuplicateWeedout | `Start temporary` / `End temporary` | general fallback; temp table removes duplicates |

Since 8.0.16, `EXISTS` subqueries get the same treatment, and `NOT IN`/`NOT EXISTS` become **antijoins** (8.0.17).

Hints:
```sql
SELECT /*+ SEMIJOIN(@sq FIRSTMATCH, LOOSESCAN) */ ... WHERE id IN (SELECT /*+ QB_NAME(sq) */ ...);
SELECT ... WHERE id IN (SELECT /*+ NO_SEMIJOIN() */ ...);
```
Or `optimizer_switch='semijoin=on,materialization=on,firstmatch=on,loosescan=on,duplicateweedout=on'`.

Semijoin is not possible when the subquery uses aggregates, `UNION`, `LIMIT` or `HAVING` (`GROUP BY` is permitted but ignored). Then MySQL falls back to materialization or per-row execution (`DEPENDENT SUBQUERY` in EXPLAIN = run for every outer row; often the slow one).

## Derived tables (subqueries in FROM, views, CTEs)
- **Merge**: the derived table is folded into the outer query (indexes on base tables usable). Default (`derived_merge=on`).
- **Materialize**: result written to an internal temp table first; the optimizer may add an auto-key on it (`<auto_key0>` in EXPLAIN).
Merge is impossible with aggregates, DISTINCT, GROUP BY, LIMIT, UNION, window functions in the derived table.
```sql
SELECT /*+ NO_MERGE(dt) */ ... FROM (SELECT ...) AS dt;    -- force materialize
SELECT /*+ MERGE(v) */ ... FROM some_view v;
```
The optimizer can push outer WHERE conditions down into materialized derived tables (`derived_condition_pushdown` optimizer switch).

## Diagnose
```sql
EXPLAIN FORMAT=TREE SELECT ...;
SET optimizer_trace = 'enabled=on'; SELECT ...; SELECT TRACE FROM information_schema.OPTIMIZER_TRACE\G
```
Look for `transformations_to_nested_joins` and `semijoin_strategy_choice` in the trace.

## Gotchas
- Rewriting `IN (subquery)` as a JOIN by hand can return duplicates; semijoin exists to avoid that.
- `NOT IN` with a nullable subquery column returns no rows if any NULL exists; use `NOT EXISTS`.
- Materialized derived tables that spill past `tmp_table_size` go to disk (`Created_tmp_disk_tables`).

## Checked

2026-10-31: confirmed the five semijoin strategies with their EXPLAIN indicators, EXISTS subqueries treated as semijoins from MySQL 8.0.16, antijoins from 8.0.17, the semijoin criteria (no aggregates, UNION, HAVING or LIMIT; GROUP BY and DISTINCT permitted but ignored), the semijoin/firstmatch/loosescan/materialization/duplicateweedout optimizer_switch flags and the SEMIJOIN()/NO_SEMIJOIN()/QB_NAME hint syntax (strategy names DUPSWEEDOUT, FIRSTMATCH, LOOSESCAN, MATERIALIZATION), derived-table merging rules (derived_merge on by default; aggregates/window functions, DISTINCT, GROUP BY, HAVING, LIMIT, UNION prevent merging), MERGE/NO_MERGE hints, and optimizer-added indexes on materialized derived tables on dev.mysql.com semijoin/derived-table/optimizer-hints pages. Removed the unconfirmed 8.0.21 and 8.0.22 version notes and corrected the restriction list.
Method: documentation only; no commands were run.
