---
id: computing-software.database-administration.sql.gaps-and-islands
name: gaps-and-islands
category: computing-software
field: database-administration
product: sql
tags: [sql, gaps-and-islands]
level: advanced
status: docs-checked
description: "Find consecutive runs and gaps in sequences using ROW_NUMBER differences."
sources: ["https://www.postgresql.org/docs/current/functions-window.html", "https://www.postgresql.org/docs/current/functions-datetime.html", "https://www.sqlite.org/windowfunctions.html", "https://www.sqlite.org/lang_datefunc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gaps and islands with row-number differencing

- Islands of consecutive ids: `SELECT min(id), max(id) FROM (SELECT id, id - row_number() OVER (ORDER BY id) AS grp FROM t) x GROUP BY grp;` (`row_number()` counts from 1 within the ordered window; consecutive ids keep `id - rn` constant).
- Dates, PostgreSQL: `d - row_number() OVER (ORDER BY d)::int` (`date - integer` gives a date, `date - date` gives a day count). SQLite: `julianday(d) - row_number() OVER (ORDER BY d)`; `julianday()` returns a number of days, so the difference is constant over a daily run.
- Dedupe first (`DISTINCT` or `GROUP BY`): `row_number()` increments on duplicates while the value does not, so repeated values split an island.
- Gaps: `lead(id) OVER (ORDER BY id) - id > 1`. `lead` returns NULL on the last row (no next row), so that row never matches. Window functions are not allowed in `WHERE`, so compute `lead` in a sub-select and filter outside.
- Self-check: the island sizes sum to the input row count.

## Checked

Date: 2026-11-07. Read the PostgreSQL window function table (row_number, lead, lag) and the date/time operator table (date - integer, date - date, date + interval), and the SQLite window function sections for row_number() and lead(), plus the julianday() entry in the date functions page. Confirmed each function's behaviour. Corrected: the PostgreSQL date form now uses `date - integer`, which the operator table lists (the interval multiplication form returns a timestamp); the gaps predicate must sit in an outer query. The arithmetic about duplicates is reasoning from row_number semantics, not a quoted claim.
Method: documentation only; no commands were run.
