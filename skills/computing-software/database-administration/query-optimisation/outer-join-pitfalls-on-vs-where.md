---
id: computing-software.database-administration.query-optimisation.outer-join-pitfalls-on-vs-where
name: outer-join-pitfalls-on-vs-where
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, outer-join, left-join, join-types, sql-fluency, anti-join]
level: practitioner
status: gated
description: "Write outer joins correctly: filters in ON versus WHERE, accidental inner joins, anti-joins with IS NULL, row multiplication from one-to-many joins, and FULL JOIN uses."
sources:
  - https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN
  - https://use-the-index-luke.com/sql/join
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/joins
  - https://www.postgresql.org/docs/16/queries-table-expressions.html#QUERIES-JOIN
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Join types and outer join pitfalls (ON vs WHERE)

## The classic bug
```sql
-- Intended: all customers, with their 2026 orders if any
SELECT c.id, o.id
FROM customers c LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.created_at >= '2026-01-01';          -- WRONG: removes customers with no orders
```
A WHERE condition on the right table discards the NULL-extended rows, silently turning the LEFT JOIN into an INNER JOIN (optimizers even rewrite it as one: PostgreSQL 16.4 plans it as a `Hash Join`). Checked on 2,000 customers and 100,000 orders: the WRONG form returned 15,041 rows while the ON form kept all 2,000 customers. Put right-table filters in `ON`:
```sql
FROM customers c LEFT JOIN orders o
  ON o.customer_id = c.id AND o.created_at >= '2026-01-01'
```
Rule: conditions that decide **which rows match** go in ON; conditions that decide **which result rows survive** go in WHERE.

## Anti-join (rows without a match)
```sql
SELECT c.* FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;               -- test a NOT NULL column of the right table (PK)
-- equivalent and often clearer:
SELECT c.* FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```
Avoid `NOT IN (subquery)` when the subquery column can be NULL: one NULL makes it return no rows.

## Row multiplication
Joining two independent one-to-many children multiplies rows:
```sql
SELECT c.id, sum(o.total), count(t.id)
FROM customers c JOIN orders o ON ... JOIN tickets t ON ...   -- sums inflated by ticket count (checked: customer 1 with 10 tickets showed sum 33,165,000 against the true 3,316,500)
```
Aggregate each child in a subquery/CTE or LATERAL first, then join the aggregates.

## Chained outer joins
`A LEFT JOIN B ... JOIN C ON C.b_id = B.id` turns the B join inner again (C requires B). Make the later join LEFT too, or nest: `A LEFT JOIN (B JOIN C ON ...) ON ...`.

## FULL OUTER JOIN
Reconciliation between two sources:
```sql
SELECT coalesce(a.id, b.id) AS id, a.amount, b.amount
FROM ledger_a a FULL JOIN ledger_b b ON a.id = b.id
WHERE a.amount IS DISTINCT FROM b.amount;
```
MySQL lacks FULL JOIN (gated: unconfirmed, source is paywalled or blocked): emulate with LEFT JOIN UNION ALL right-only anti-join. The reconciliation query was run on PostgreSQL 16.4 and returned the changed row (2) and the right-only row (4) while treating NULL = NULL as equal.

## Performance notes
- Outer joins constrain join order (the preserved side must be produced); some optimizers reorder less freely.
- Index the join columns on the inner/right side (`orders(customer_id)`).

## Verify
Count check: `SELECT count(*) FROM customers` must equal the row count of a LEFT JOIN query that should preserve all customers (when the right side is at most one row per customer).
