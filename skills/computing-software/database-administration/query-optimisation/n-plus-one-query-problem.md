---
id: computing-software.database-administration.query-optimisation.n-plus-one-query-problem
name: n-plus-one-query-problem
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, sql, query-anti-patterns, n-plus-one, orm-performance, eager-loading, pg-stat-statements, batching-queries, chatty-application]
level: practitioner
status: draft
description: "Detect N+1 query patterns from the database side (call counts, pg_stat_statements, slow log digests) and fix them with joins, IN-list batching or ORM eager loading."
sources:
  - https://www.postgresql.org/docs/current/pgstatstatements.html
  - https://docs.djangoproject.com/en/stable/ref/models/querysets/#prefetch-related
  - https://guides.rubyonrails.org/active_record_querying.html#eager-loading-associations
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The N+1 query problem

**Goal:** a page that runs 1 + N tiny queries (one per row of a list) runs 1-2
queries instead, cutting latency dominated by round trips.

## Recognise it from the database
Each query is fast, so slow logs miss it. Look at **call counts**:
```sql
-- PostgreSQL
SELECT calls, round(mean_exec_time::numeric,2) AS ms, round(total_exec_time::numeric) AS total_ms, left(query,80)
FROM pg_stat_statements ORDER BY calls DESC LIMIT 10;
```
A `SELECT ... FROM customers WHERE id = $1` with calls in the millions and
sub-millisecond mean, whose calls track a list endpoint's traffic × page size,
is the signature. MySQL: `sys.statements_with_runtimes_in_95th_percentile` / `performance_schema.events_statements_summary_by_digest`
ordered by `COUNT_STAR`. SQL Server: Query Store execution counts. APM traces
showing dozens of identical spans per request confirm it.

## Fixes
1. **Join** when you need columns from both:
   ```sql
   SELECT o.id, o.total, c.name FROM orders o JOIN customers c ON c.id = o.customer_id
   WHERE o.created_at >= $1 ORDER BY o.created_at DESC LIMIT 50;
   ```
2. **Batch the second query** (avoids row multiplication for one-to-many):
   ```sql
   SELECT * FROM order_items WHERE order_id = ANY($1);    -- PostgreSQL array param
   SELECT * FROM order_items WHERE order_id IN (?, ?, ...);  -- others; chunk lists to ~1000
   ```
3. **ORM eager loading**: Django `select_related` (join) / `prefetch_related`
   (batched IN), Rails `includes`/`preload`, Hibernate `JOIN FETCH` / `@BatchSize`,
   Entity Framework `.Include()`, SQLAlchemy `selectinload`/`joinedload`.
4. GraphQL resolvers: DataLoader-style batching per request.

## Gotchas
- Joining several one-to-many relations at once multiplies rows (cartesian
  explosion); use separate batched queries per relation.
- Huge IN lists: plan-cache churn (different list lengths) and parser limits;
  array parameters (`= ANY($1)`) or temp tables avoid that.
- Fixing N+1 can move cost into one heavier query: check its plan and indexes.

## Verify
Per-request query count (ORM debug toolbar, APM, `pg_stat_statements` calls delta
under a fixed load) drops from 1+N to a constant; endpoint p95 latency falls.
