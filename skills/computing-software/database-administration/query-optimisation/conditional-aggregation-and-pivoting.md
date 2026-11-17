---
id: computing-software.database-administration.query-optimisation.conditional-aggregation-and-pivoting
name: conditional-aggregation-and-pivoting
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, conditional-aggregation, pivot, filter-clause, crosstab, sql-fluency]
level: practitioner
status: gated
description: "Compute several filtered aggregates in one pass with FILTER or CASE inside aggregates, and pivot rows to columns portably or with PIVOT/crosstab."
sources:
  - https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-AGGREGATES
  - https://learn.microsoft.com/en-us/sql/t-sql/queries/from-using-pivot-and-unpivot
  - https://www.postgresql.org/docs/current/tablefunc.html
  - https://www.postgresql.org/docs/16/sql-expressions.html#SYNTAX-AGGREGATES
  - https://www.postgresql.org/docs/16/tablefunc.html
  - https://www.sqlite.org/releaselog/3_30_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional aggregation and pivoting

## One scan, many metrics
Instead of one query per status:
```sql
SELECT
  count(*)                                         AS total,
  count(*) FILTER (WHERE status = 'paid')          AS paid,
  count(*) FILTER (WHERE status = 'refunded')      AS refunded,
  sum(total) FILTER (WHERE status = 'paid')        AS paid_revenue,
  avg(total) FILTER (WHERE channel = 'web')        AS web_avg
FROM orders
WHERE created_at >= date '2026-10-01';
```
`FILTER` is standard SQL (PostgreSQL 16.4 run; SQLite 3.30+, confirmed in its release notes and run on 3.50.4). The queries in this skill ran on PostgreSQL 16.4 with the expected counts, and the FILTER pivot and `crosstab()` returned identical results. Portable form with CASE (MySQL, SQL Server, Oracle):
```sql
sum(CASE WHEN status = 'paid' THEN 1 ELSE 0 END)          AS paid,
sum(CASE WHEN status = 'paid' THEN total END)             AS paid_revenue   -- NULLs ignored
```
Use `ELSE 0` for counts and no ELSE (NULL) for sums/averages so non-matching rows do not distort averages.

## Pivot rows into columns
Portable pivot = conditional aggregation grouped by the row key:
```sql
SELECT product_id,
  sum(qty) FILTER (WHERE month = 1) AS jan,
  sum(qty) FILTER (WHERE month = 2) AS feb,
  sum(qty) FILTER (WHERE month = 3) AS mar
FROM sales GROUP BY product_id;
```
SQL Server/Oracle `PIVOT` (the bracketed `[1], [2], [3]` list is SQL Server syntax; Oracle takes plain values or aliases such as `IN (1 AS jan, 2 AS feb)` (gated: unconfirmed, source is paywalled or blocked)):
```sql
SELECT * FROM (SELECT product_id, month, qty FROM sales) s
PIVOT (SUM(qty) FOR month IN ([1], [2], [3])) p;
```
PostgreSQL `crosstab()` (tablefunc extension) handles sparse data but needs a column definition list.

## Dynamic column lists
SQL needs columns known at parse time. For a variable set (all months present), generate the SQL in application code or with dynamic SQL, or return long format (`product_id, month, qty`) and pivot in the reporting tool.

## Unpivot
`UNPIVOT` (SQL Server/Oracle), `CROSS JOIN LATERAL (VALUES ...)` in PostgreSQL:
```sql
SELECT id, k, v FROM metrics m CROSS JOIN LATERAL (VALUES ('cpu', m.cpu), ('mem', m.mem)) AS x(k, v);
```

## Verify
Sum of the pivoted columns equals the unpivoted total for each key; the plan shows a single scan of the base table.
