---
id: computing-software.database-administration.query-optimisation.generate-series-unnest-and-calendar-tables
name: generate-series-unnest-and-calendar-tables
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, generate-series, unnest, calendar-table, set-returning-functions, sql-fluency]
level: practitioner
status: draft
description: "Fill gaps in time-series reports and expand arrays with generate_series, unnest and calendar tables, with equivalents for MySQL, SQL Server and SQLite."
sources:
  - https://www.postgresql.org/docs/current/functions-srf.html
  - https://www.postgresql.org/docs/current/functions-array.html
  - https://learn.microsoft.com/en-us/sql/t-sql/functions/generate-series-transact-sql
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Set-returning functions and calendar tables

## Zero-filled daily report
`GROUP BY day` omits days with no rows. Drive the query from a generated series:
```sql
SELECT d::date AS day, count(o.id) AS orders
FROM generate_series(date '2026-10-01', date '2026-10-31', interval '1 day') AS d
LEFT JOIN orders o ON o.created_at >= d AND o.created_at < d + interval '1 day'
GROUP BY d ORDER BY d;
```
The range condition (not `o.created_at::date = d`) keeps the index on `created_at` usable.

## Other engines
| Engine | Series |
|---|---|
| SQL Server 2022+ | `GENERATE_SERIES(1, 31)`; older: numbers table or recursive CTE |
| MySQL 8 | recursive CTE: `WITH RECURSIVE d AS (SELECT DATE('2026-10-01') AS day UNION ALL SELECT day + INTERVAL 1 DAY FROM d WHERE day < '2026-10-31') ...` (raise `cte_max_recursion_depth` beyond 1000) |
| SQLite | `generate_series` extension (shell) or recursive CTE |
| Oracle | `CONNECT BY LEVEL <= 31` |

## Calendar table
For business logic (holidays, fiscal periods, ISO weeks), a persisted table beats generated series:
```sql
CREATE TABLE calendar (
  day date PRIMARY KEY, iso_year int, iso_week int, month int, quarter int,
  is_weekend boolean, is_holiday boolean, fiscal_period text);
INSERT INTO calendar SELECT d, extract(isoyear FROM d), extract(week FROM d), extract(month FROM d),
  extract(quarter FROM d), extract(isodow FROM d) IN (6,7), false, NULL
FROM generate_series(date '2020-01-01', date '2040-12-31', '1 day') d;
```
"Business days between two dates" becomes `count(*) FROM calendar WHERE day BETWEEN ... AND NOT is_weekend AND NOT is_holiday`.

## unnest: arrays to rows
```sql
SELECT o.id, t.tag FROM posts o CROSS JOIN LATERAL unnest(o.tags) AS t(tag);
SELECT * FROM unnest(ARRAY[1,2,3], ARRAY['a','b','c']) AS x(n, s);     -- zip arrays
SELECT * FROM unnest($1::int[]) WITH ORDINALITY AS t(id, pos);          -- keep order
```
Batch lookups: `WHERE id = ANY($1::bigint[])` or join to `unnest($1)` instead of building huge IN lists.

## Verify
The report returns exactly one row per day in range (count equals days in month), with zeros where expected.
