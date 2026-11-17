---
id: computing-software.database-administration.query-optimisation.set-operations-union-intersect-except
name: set-operations-union-intersect-except
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, union-all, set-operations, intersect, except, sql-fluency]
level: practitioner
status: gated
description: "Use UNION ALL versus UNION, INTERSECT and EXCEPT correctly and efficiently, with column matching rules, ordering, duplicates and index-friendly alternatives."
sources:
  - https://www.postgresql.org/docs/current/queries-union.html
  - https://dev.mysql.com/doc/refman/8.4/en/set-operations.html
  - https://learn.microsoft.com/en-us/sql/t-sql/language-elements/set-operators-union-transact-sql
  - https://www.postgresql.org/docs/16/queries-union.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Set operations (UNION / INTERSECT / EXCEPT)

## UNION ALL vs UNION
- `UNION ALL` concatenates: no sort, no hash, streams.
- `UNION` removes duplicates across the whole result: requires a sort or hash over all rows.
Default to `UNION ALL`; use `UNION` only when duplicates are possible **and** unwanted. A common waste is `UNION` over branches that are disjoint by construction (different `type` filters).

## Rules
- Same number of columns, compatible types by position; names come from the first branch.
- `ORDER BY` / `LIMIT` apply to the whole result unless a branch is parenthesised:
```sql
(SELECT id, created_at FROM orders_2025 ORDER BY created_at DESC LIMIT 10)
UNION ALL
(SELECT id, created_at FROM orders_2026 ORDER BY created_at DESC LIMIT 10)
ORDER BY created_at DESC LIMIT 10;
```
Pushing `LIMIT` into each branch lets each use its index for top-N.

## INTERSECT and EXCEPT
```sql
-- customers who bought in both years
SELECT customer_id FROM orders WHERE year = 2025
INTERSECT
SELECT customer_id FROM orders WHERE year = 2026;

-- products in catalogue but never sold
SELECT id FROM products
EXCEPT
SELECT product_id FROM order_items;
```
- Both remove duplicates by default; `INTERSECT ALL` / `EXCEPT ALL` keep multiplicity (PostgreSQL and DuckDB run; SQLite has no `ALL` variants, a syntax error on 3.50.4; MySQL 8.0.31+, SQL Server lacking them and Oracle using `MINUS` before 21c are (gated: unconfirmed, source is paywalled or blocked)).
- NULLs compare as equal in set operations (unlike `=`), which can be a feature for reconciliation (checked: `select null union select null` returns one row, and `null intersect null` returns a row, on SQLite and DuckDB).

## Alternatives that use indexes better
- `EXCEPT` → `NOT EXISTS` anti-join: can use an index on `order_items(product_id)` and stop at first match.
- `INTERSECT` → `EXISTS` semi-join or `GROUP BY customer_id HAVING count(DISTINCT year) = 2`.
Optimizers differ; compare plans.

## Data comparison idiom
```sql
(SELECT * FROM a EXCEPT SELECT * FROM b) UNION ALL (SELECT * FROM b EXCEPT SELECT * FROM a);
```
Empty result = identical sets (ignoring duplicates).

## Verify
Plans for `UNION` show a `HashAggregate`/`Sort` + `Unique` step that disappears with `UNION ALL`; row counts match expectations.
