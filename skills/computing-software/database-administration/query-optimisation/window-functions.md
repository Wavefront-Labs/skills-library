---
id: computing-software.database-administration.query-optimisation.window-functions
name: window-functions
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, sql, advanced-sql, window-functions, row-number, rank, lag-lead, running-total, partition-by, frame-clause, top-n-per-group]
level: practitioner
status: gated
description: "Write SQL window functions (ROW_NUMBER, RANK, LAG/LEAD, running totals with frame clauses) for top-N-per-group, deltas and moving averages, and index for them."
sources:
  - https://www.postgresql.org/docs/current/tutorial-window.html
  - https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS
  - https://modern-sql.com/feature/over
  - https://www.sqlite.org/windowfunctions.html
  - https://www.postgresql.org/docs/16/tutorial-window.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Window functions

**Goal:** per-row calculations over related rows (rank in group, previous value,
running sum) in one pass, without self-joins or correlated subqueries.

## Anatomy
```sql
fn(...) OVER (PARTITION BY <group cols> ORDER BY <order cols> <frame>)
```
Works the same in PostgreSQL, MySQL 8+ (gated: unconfirmed, source is paywalled or blocked), SQL Server, Oracle (gated: unconfirmed, source is paywalled or blocked), SQLite 3.25+ (sqlite.org: window functions arrived in 3.25.0, 2018-09-15). All the patterns below were run on PostgreSQL 16.4.

## Patterns
```sql
-- Latest order per customer (top-1 per group)
SELECT * FROM (
  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) AS rn
  FROM orders o) t
WHERE rn = 1;

-- Change from previous reading
SELECT device_id, ts, value,
       value - LAG(value) OVER (PARTITION BY device_id ORDER BY ts) AS delta
FROM readings;

-- Running total and 7-row moving average
SELECT day, revenue,
       SUM(revenue) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running,
       AVG(revenue) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma7
FROM daily_revenue;

-- Share of group total
SELECT region, product, sales, sales * 100.0 / SUM(sales) OVER (PARTITION BY region) AS pct
FROM sales_by_product;
```
`RANK` leaves gaps after ties (1,1,3), `DENSE_RANK` does not (1,1,2),
`ROW_NUMBER` breaks ties arbitrarily unless ORDER BY is unique.

## The frame trap
With ORDER BY and no explicit frame, the default is
`RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`: rows with equal ORDER BY
values are peers and all included, so running totals jump at ties, and
`LAST_VALUE(x)` returns the current row's peer group value, not the partition's
last (checked: values 10, 20, 5, 7 by day with a tie on day 2 give a default running sum of 35 on both tied rows against 30 and 35 with `ROWS`, and `last_value` 5 on the tied rows). Write `ROWS BETWEEN ...` explicitly, or for last value use
`FIRST_VALUE(x) OVER (... ORDER BY ts DESC)`.

## Performance
- Windows are computed after WHERE/GROUP BY; you cannot filter on them in the same
  level (wrap in a subquery/CTE, or `QUALIFY` in some engines).
- An index on `(partition cols, order cols)` lets the engine read rows pre-sorted
  and skip the sort. For top-1 per group on huge tables, a LATERAL/`DISTINCT ON`
  or loose index scan can beat ROW_NUMBER over everything.
- Several windows with the same OVER clause share one sort; name it with `WINDOW w AS (...)`.

## Verify
Compare results to a known self-join version on a sample; `EXPLAIN` shows one
WindowAgg/Window operator and ideally no Sort node when the index matches.
