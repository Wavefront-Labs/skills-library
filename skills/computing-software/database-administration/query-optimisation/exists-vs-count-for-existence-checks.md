---
id: computing-software.database-administration.query-optimisation.exists-vs-count-for-existence-checks
name: exists-vs-count-for-existence-checks
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, exists-vs-count, exists, semi-join, query-patterns, count-star]
level: practitioner
status: draft
description: "Check whether rows exist with EXISTS or LIMIT 1 instead of COUNT(*) > 0, so the database stops at the first match, and know when optimisers already rewrite it."
sources:
  - https://www.postgresql.org/docs/current/functions-subquery.html#FUNCTIONS-SUBQUERY-EXISTS
  - https://use-the-index-luke.com/sql/partial-results/top-n-queries
  - https://learn.microsoft.com/en-us/sql/t-sql/language-elements/exists-transact-sql
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EXISTS vs COUNT(*) for existence checks

## The anti-pattern
```sql
SELECT count(*) FROM orders WHERE customer_id = 42 AND status = 'open';
-- app: if count > 0 ...
```
COUNT must find **all** matching rows. For a customer with 50,000 open orders, that is 50,000 index entries (and maybe heap visits) to answer a yes/no question.

## Use EXISTS or LIMIT 1
```sql
SELECT EXISTS (SELECT 1 FROM orders WHERE customer_id = 42 AND status = 'open');
-- or
SELECT 1 FROM orders WHERE customer_id = 42 AND status = 'open' LIMIT 1;   -- TOP 1 / FETCH FIRST 1 ROW ONLY
```
Execution stops at the first match. With an index on `(customer_id, status)` it is a single index probe.

## In predicates
```sql
SELECT c.* FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.status = 'open');
```
Optimisers turn this into a semi-join (stop per customer at the first order). Replace `WHERE (SELECT count(*) ...) > 0` patterns with EXISTS; some optimisers (SQL Server often, Oracle sometimes) rewrite `count > 0` automatically, PostgreSQL and MySQL generally do not.

## When COUNT is right
When you need the number. For "show 99+" UI badges, cap the work: `SELECT count(*) FROM (SELECT 1 FROM t WHERE ... LIMIT 100) s;`.

## ORMs
Django `.exists()`, SQLAlchemy `session.query(q.exists()).scalar()` / `select(exists().where(...))`, Rails `.exists?`, EF `.Any()` all generate EXISTS/LIMIT 1. Using `.count() > 0` or loading rows defeats it.

## Verify
`EXPLAIN ANALYZE` for the EXISTS version shows `actual rows=1` on the index scan (`Limit` or semi-join stops early) versus thousands for the COUNT version; latency becomes independent of how many rows match.
