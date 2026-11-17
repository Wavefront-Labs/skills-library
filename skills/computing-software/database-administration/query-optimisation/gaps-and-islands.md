---
id: computing-software.database-administration.query-optimisation.gaps-and-islands
name: gaps-and-islands
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, advanced-sql, gaps-and-islands, window-functions, row-number, sessionization]
level: advanced
status: gated
description: "Solve gaps-and-islands problems in SQL with window functions: consecutive runs, missing sequence values, sessionizing events by inactivity, and merging overlapping ranges."
sources:
  - https://www.postgresql.org/docs/current/tutorial-window.html
  - https://www.postgresql.org/docs/current/functions-window.html
  - https://learn.microsoft.com/en-us/sql/t-sql/functions/lag-transact-sql
  - https://www.postgresql.org/docs/14/functions-aggregate.html
  - https://duckdb.org/docs/stable/sql/functions/window_functions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gaps and islands

"Islands" are runs of consecutive rows sharing a property; "gaps" are the missing values between
them. Window functions solve both in one pass.

## Islands: consecutive values (row_number difference)
Days a user was active in a row:
```sql
WITH d AS (
  SELECT user_id, day,
         day - (row_number() OVER (PARTITION BY user_id ORDER BY day))::int AS grp
  FROM (SELECT DISTINCT user_id, activity_date AS day FROM activity) x
)
SELECT user_id, min(day) AS streak_start, max(day) AS streak_end, count(*) AS days
FROM d GROUP BY user_id, grp ORDER BY user_id, streak_start;
```
For consecutive values, `value - row_number()` is constant within a run. Works for integers and
dates (date minus integer in PostgreSQL; `DATEADD(day, -ROW_NUMBER() ..., day)` in SQL Server (gated: unconfirmed, source is paywalled or blocked)). All five queries below were run in DuckDB 1.5.6 on small data and returned the expected islands, gaps (3-4, 7-8) and merged ranges (1-8, 10-13; ranges that touch at 12 merge).

## Islands by state change (lag + running sum)
Group consecutive rows with the same status, even if values are not consecutive numbers:
```sql
WITH flagged AS (
  SELECT *, CASE WHEN status = lag(status) OVER (PARTITION BY device ORDER BY ts)
                 THEN 0 ELSE 1 END AS is_start
  FROM device_status
), grouped AS (
  SELECT *, sum(is_start) OVER (PARTITION BY device ORDER BY ts) AS island
  FROM flagged
)
SELECT device, status, min(ts) AS from_ts, max(ts) AS to_ts
FROM grouped GROUP BY device, status, island ORDER BY device, from_ts;
```

## Sessionization (new session after 30 min idle)
Same pattern: `is_start = 1` when `ts - lag(ts) > interval '30 minutes'` or lag is NULL, then a
running sum gives a session number.

## Gaps: missing numbers
```sql
SELECT id + 1 AS gap_start, next_id - 1 AS gap_end
FROM (SELECT id, lead(id) OVER (ORDER BY id) AS next_id FROM invoices) t
WHERE next_id - id > 1;
```
Alternatively join to `generate_series(min, max)` and anti-join, simpler but heavier for large ranges.

## Merging overlapping ranges
```sql
WITH s AS (
  SELECT *, CASE WHEN start_ts <= max(end_ts) OVER (PARTITION BY room ORDER BY start_ts, end_ts
                     ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) THEN 0 ELSE 1 END AS is_start
  FROM bookings
), g AS (SELECT *, sum(is_start) OVER (PARTITION BY room ORDER BY start_ts, end_ts) AS grp FROM s)
SELECT room, min(start_ts), max(end_ts) FROM g GROUP BY room, grp;
```
(PostgreSQL: range types and `range_agg` / multiranges do this natively in 14+; `range_agg` is in the 14 aggregate docs and absent from 13.)

## Performance
One index on `(partition col, order col)` lets the window functions read in order without a sort.

## Verify
Test with edge cases: single-row islands, duplicates (use DISTINCT first), first and last rows,
and NULLs in the ordering column; compare with a small hand-computed expected result.
