---
id: computing-software.database-administration.query-optimisation.exists-in-and-the-not-in-null-trap
name: exists-in-and-the-not-in-null-trap
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, advanced-sql, anti-join, not-in-null, semi-join, not-exists, subqueries]
level: practitioner
status: gated
description: "Write semi-joins and anti-joins correctly: EXISTS vs IN, why NOT IN returns nothing when the subquery has a NULL, and NOT EXISTS / LEFT JOIN IS NULL rewrites."
sources:
  - https://www.postgresql.org/docs/current/functions-subquery.html
  - https://use-the-index-luke.com/sql/join
  - https://learn.microsoft.com/en-us/sql/t-sql/language-elements/in-transact-sql
  - https://www.postgresql.org/docs/16/queries-table-expressions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EXISTS, IN and the NOT IN NULL trap

## Semi-join: "rows that have a match"
```sql
SELECT c.* FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
SELECT c.* FROM customers c WHERE c.id IN (SELECT customer_id FROM orders);
```
Modern optimizers (PostgreSQL, SQL Server, Oracle, MySQL 8.0.16+ (gated: unconfirmed, source is paywalled or blocked)) turn both into the same
semi-join plan. Avoid the join-plus-DISTINCT form (`SELECT DISTINCT c.* FROM customers c JOIN orders o ...`),
which multiplies rows then removes duplicates.

## Anti-join: "rows with no match"
```sql
-- correct and fast everywhere
SELECT c.* FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- equivalent
SELECT c.* FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE o.customer_id IS NULL;
```

## The NOT IN trap
```sql
SELECT c.* FROM customers c WHERE c.id NOT IN (SELECT customer_id FROM orders);
```
If **any** `orders.customer_id` is NULL, this returns **zero rows**. `x NOT IN (1, 2, NULL)`
means `x <> 1 AND x <> 2 AND x <> NULL`, and `x <> NULL` is UNKNOWN, so the whole predicate is
never TRUE. It is a correctness bug that appears only when a NULL sneaks into the data.
It also often plans worse (PostgreSQL cannot use a hashed anti-join for NOT IN with a nullable
subquery; it uses a "hashed SubPlan" or a slow nested scan). Checked on PostgreSQL 16.4 (10,000 customers, 5,000 orders): EXISTS and IN both plan as `Hash Semi Join`, NOT EXISTS as `Hash Anti Join`, NOT IN as `Seq Scan ... Filter: NOT (hashed SubPlan 1)`, and adding the NULL row made NOT IN return 0 rows against 5,000 for NOT EXISTS. PostgreSQL also kept the hashed SubPlan for NOT IN after adding `WHERE customer_id IS NOT NULL`: it does not rewrite NOT IN to an anti-join, so NOT EXISTS is still the way to get one.

Rules:
- Use `NOT EXISTS` for anti-joins. Always.
- If you must use NOT IN, make the subquery non-nullable: `WHERE customer_id IS NOT NULL`, or a
  `NOT NULL` column constraint.
- `IN (list of literals)` is fine; just never include NULL in a NOT IN list.

## Correlation and indexes
The subquery's correlated column (`orders.customer_id`) needs an index for the nested-loop
variant; hash anti-joins scan both sides once and suit large sets.

## Verify
```sql
INSERT INTO orders (customer_id) VALUES (NULL);   -- in a test
```
then compare result counts of the NOT IN and NOT EXISTS versions: NOT IN drops to 0, NOT EXISTS
stays correct. EXPLAIN should show `Hash Anti Join` / `Nested Loop Anti Join` (PostgreSQL) or
`Left Anti Semi Join` (SQL Server (gated: unconfirmed, source is paywalled or blocked)) for NOT EXISTS.
