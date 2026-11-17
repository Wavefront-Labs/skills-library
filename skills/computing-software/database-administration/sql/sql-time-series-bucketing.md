---
id: computing-software.database-administration.sql.sql-time-series-bucketing
name: sql-time-series-bucketing
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-time-series, date-bucketing, running-totals, moving-average, generate-series-dates]
level: practitioner
status: docs-checked
description: "Bucket events by period, fill gaps in time series and compute running totals and moving averages."
sources: ["https://www.postgresql.org/docs/current/functions-datetime.html", "https://www.postgresql.org/docs/current/functions-srf.html", "https://www.postgresql.org/docs/current/sql-expressions.html", "https://www.postgresql.org/docs/current/functions-window.html", "https://www.postgresql.org/docs/current/functions-conditional.html", "https://www.postgresql.org/docs/current/brin.html", "https://www.sqlite.org/lang_with.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time series in SQL

- Bucket: `date_trunc('day', ts AT TIME ZONE 'Europe/London')` (for `timestamptz` input) so buckets follow the business time zone. `AT TIME ZONE` returns the local clock reading as a `timestamp`; `date_trunc` also accepts a zone as a third argument for `timestamptz`.
- Fill empty buckets by left-joining a generated calendar (`generate_series(start, end, interval '1 day')` with timestamp arguments, a recursive CTE as in SQLite, or a calendar table) to the aggregated data and `COALESCE(count, 0)`.
- Running total: `SUM(x) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`. The default frame is `RANGE UNBOUNDED PRECEDING`, which with ORDER BY runs through the current row's last peer, so rows with equal `day` values share the same total; `ROWS` mode treats each row separately. State the frame explicitly.
- Moving average: `AVG(x) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`; the first rows have fewer than seven rows in the frame, so filter them if a full window is required.
- Period-over-period: `lag(x, 1) OVER (ORDER BY day)` (offset defaults to 1, default value to NULL when no earlier row exists) and `x / NULLIF(prev, 0) - 1`; `NULLIF(a, b)` returns NULL when the two are equal, avoiding division by zero.
- Indexing: a BRIN index suits very large tables whose column values correlate with physical row position, such as a date column on rows added in date order.

## Checked

2026-11-08. Confirmed against the PostgreSQL date/time function, set returning function, window frame (sql-expressions), window function (lag), conditional (NULLIF, COALESCE) and BRIN pages, and the SQLite WITH page. Removed the claims that the default frame is slower, that RANGE with intervals needs PostgreSQL 11, range partitioning, and TimescaleDB hypertables; none are stated on a fetched page.
Method: documentation only; no commands were run.
