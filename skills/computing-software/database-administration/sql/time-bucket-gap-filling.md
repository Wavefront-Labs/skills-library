---
id: computing-software.database-administration.sql.time-bucket-gap-filling
name: time-bucket-gap-filling
category: computing-software
field: database-administration
product: sql
tags: [sql, time-bucket-gap-filling]
level: practitioner
status: docs-checked
description: "Fill missing intervals in time series using generate_series and LEFT JOIN."
sources: ["https://www.postgresql.org/docs/current/functions-srf.html", "https://www.postgresql.org/docs/current/functions-datetime.html", "https://www.postgresql.org/docs/current/functions-conditional.html", "https://www.sqlite.org/lang_with.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time bucketing with gap filling

- PostgreSQL: `SELECT d.day, coalesce(c.n, 0) AS n FROM generate_series(timestamp '2024-01-01', timestamp '2024-01-31', interval '1 day') AS d(day) LEFT JOIN (SELECT date_trunc('day', ts AT TIME ZONE 'UTC') AS day, count(*) AS n FROM e GROUP BY 1) c ON c.day = d.day;`
- `generate_series(start, stop, step interval)` exists for `timestamp` and `timestamptz`. It returns zero rows if step is positive and start is greater than stop, or if any input is NULL, and it is an error for the step to be zero. The `timestamptz` form takes an optional time zone argument so day steps follow daylight-saving changes in that zone.
- `date_trunc('day', ts)` truncates to the precision named; for `timestamptz` an optional third argument names the zone. `timestamptz AT TIME ZONE zone` returns a `timestamp` as the clock would read in that zone, so truncate after converting when the buckets must follow a business time zone. Both sides of the join must have the same type.
- `coalesce(c.n, 0)` turns the NULL from the unmatched LEFT JOIN row into zero.
- In SQLite, build the series with a recursive CTE (a non-recursive seed SELECT, then a recursive SELECT joined with UNION or UNION ALL, referencing the CTE once).
- Use half-open ranges (`ts >= a AND ts < b`) to avoid counting a boundary row in two buckets.
- Self-check: output row count equals the number of buckets.

## Checked

2026-11-08. Confirmed against the PostgreSQL Set Returning Functions, date/time functions (date_trunc, AT TIME ZONE) and conditional expression (COALESCE) pages, and the SQLite WITH clause page (recursive CTE rules). Removed the date-typed generate_series example (the manual documents timestamp and timestamptz forms only) and the advice to store timestamps in UTC, which no page states.
Method: documentation only; no commands were run.
