---
id: computing-software.database-administration.query-optimisation.lateral-joins-and-top-n-per-group
name: lateral-joins-and-top-n-per-group
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, sql, advanced-sql, lateral-join, cross-apply, top-n-per-group, correlated-subquery, distinct-on]
level: practitioner
status: gated
description: "Use LATERAL joins (CROSS/OUTER APPLY in SQL Server) for top-N per group and per-row subqueries, with the indexes that make them fast."
sources:
  - https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-LATERAL
  - https://dev.mysql.com/doc/refman/8.4/en/lateral-derived-tables.html
  - https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql
  - https://www.postgresql.org/docs/16/queries-table-expressions.html#QUERIES-LATERAL
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LATERAL joins and top-N per group

**Goal:** "latest 3 orders per customer" and similar queries that run as index seeks, not full sorts.

## LATERAL
A subquery in FROM that can reference columns of tables to its left; evaluated per outer row.
```sql
-- PostgreSQL (run on 16.4) / MySQL 8.0.14+ (gated: unconfirmed, source is paywalled or blocked)
SELECT c.id, c.name, o.id AS order_id, o.created_at, o.total
FROM customers c
CROSS JOIN LATERAL (
  SELECT id, created_at, total FROM orders
  WHERE orders.customer_id = c.id
  ORDER BY created_at DESC LIMIT 3
) o
WHERE c.region = 'EU';
-- keep customers with no orders:
-- LEFT JOIN LATERAL (...) o ON true
```
SQL Server / Oracle 12c+ (not run here (gated: unconfirmed, source is paywalled or blocked)):
```sql
SELECT c.id, o.* FROM customers c
CROSS APPLY (SELECT TOP (3) id, created_at, total FROM orders WHERE customer_id = c.id ORDER BY created_at DESC) o;
-- OUTER APPLY = LEFT JOIN LATERAL
```

## The index that makes it fly
`CREATE INDEX ON orders (customer_id, created_at DESC) INCLUDE (total);` gives each lateral probe a seek + read of 3 rows (checked on 100,000 orders: `Index Scan using orders_customer_id_created_at_total_idx`, `loops=1000` for 1,000 EU customers, at most 3 rows per probe). The LEFT JOIN LATERAL ... ON true form kept all customers; the `DISTINCT ON` and `ROW_NUMBER() <= 3` forms returned 1,500 and 4,500 rows, matching the per-customer limits; `jsonb_array_elements` and `SELECT price * qty` laterals also ran. Without it, each probe sorts that customer's orders.

## Alternatives
| Approach | When better |
|---|---|
| `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC)` filtered `<= 3` | Most groups are needed and are small; reads everything once |
| LATERAL / APPLY | Few outer rows or many rows per group: seeks only what is needed |
| PostgreSQL `DISTINCT ON (customer_id) ... ORDER BY customer_id, created_at DESC` | Top-1 per group, concise |

## Other LATERAL uses
- Calling set-returning functions per row: `CROSS JOIN LATERAL jsonb_array_elements(o.items) item`.
- Reusing computed expressions: `CROSS JOIN LATERAL (SELECT price * qty AS line_total) x`.

## Gotchas
- LATERAL with a large outer set and no supporting index is a nested loop of sorts: slow.
- MySQL before 8.0.14 has no LATERAL (gated: unconfirmed, source is paywalled or blocked); use window functions.

## Verify
`EXPLAIN (ANALYZE)` shows a Nested Loop with an Index Scan on the lateral side using `(customer_id, created_at)` and `loops` = outer rows, each returning <= 3 rows.
