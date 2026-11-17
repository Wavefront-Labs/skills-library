---
id: computing-software.database-administration.sql.interval-arithmetic
name: interval-arithmetic
category: computing-software
field: database-administration
product: sql
tags: [sql, interval-arithmetic]
level: practitioner
status: docs-checked
description: "Add and subtract dates and intervals correctly, including month-end behaviour."
sources: ["https://www.postgresql.org/docs/current/functions-datetime.html", "https://www.postgresql.org/docs/current/datatype-datetime.html", "https://www.sqlite.org/lang_datefunc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interval arithmetic and date differences

- PostgreSQL: adding an interval to a timestamp applies the months, days and microseconds fields in turn. A months step keeps the day of month unless it would pass the end of the new month, in which case the last day of that month is used, so `date '2024-01-31' + interval '1 month'` gives 2024-02-29 in a leap year (the page's own example is March 31 plus 1 month becoming April 30). Note `date + interval` returns a timestamp.
- PostgreSQL: `date - date` returns an integer number of days; `timestamp - timestamp` returns an interval (24-hour spans shown as days); `age(ts1, ts2)` returns a "symbolic" result in years, months and days, and its month count is ambiguous (it uses the month of the earlier date).
- PostgreSQL: `interval '1 day'` and `interval '24 hours'` differ across a daylight-saving change in a `timestamptz` (the page shows 12:00 versus 13:00 in America/Denver); intervals store months, days and microseconds separately because month and day lengths vary.
- SQLite: `date('now', '+1 month', 'start of month')` works, and `julianday(b) - julianday(a)` gives a precise day difference (`timediff()` gives a human-friendly span). When a month shift is ambiguous (2023-12-31 plus two months) SQLite defaults to "ceiling", choosing the later date; add the `floor` modifier for the last day of the previous month.
- Do not convert months to days by multiplying by 30; month and year lengths vary.
- Self-check: add one month to Jan 31 and verify the result matches your business rule.

## Checked

Date: 2026-11-07. Read the PostgreSQL date/time operator table and the passage on adding intervals to timestamps (functions-datetime), the interval storage paragraph (datatype-datetime) and the SQLite date function modifiers (month shifts, ceiling and floor) and julianday/timediff text. Confirmed all items above. Corrected: SQLite does not clamp like PostgreSQL; default is ceiling. The page named for the `ceiling` default is SQLite lang_datefunc; "start of month" modifier confirmed in the same list.
Method: documentation only; no commands were run.
