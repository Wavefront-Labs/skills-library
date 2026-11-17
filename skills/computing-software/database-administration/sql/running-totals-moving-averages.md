---
id: computing-software.database-administration.sql.running-totals-moving-averages
name: running-totals-moving-averages
category: computing-software
field: database-administration
product: sql
tags: [sql, running-totals-moving-averages]
level: practitioner
status: docs-checked
description: "Compute cumulative sums and moving averages with window frames."
sources: ["https://www.postgresql.org/docs/current/sql-expressions.html", "https://www.postgresql.org/docs/current/tutorial-window.html", "https://www.sqlite.org/windowfunctions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running totals and moving averages

- Running total: `sum(v) OVER (ORDER BY ts ROWS UNBOUNDED PRECEDING)`; an omitted frame end defaults to `CURRENT ROW`.
- 7-row moving average: `avg(v) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`. It counts physical rows, so it is a 7-day average only with exactly one row per day (gap-fill first); near the partition start the frame holds fewer rows.
- Per group: add `PARTITION BY k`.
- Default frame trap: with ORDER BY and no frame clause the frame is `RANGE UNBOUNDED PRECEDING` (through the current row's last peer), so tied rows get the same running value (PostgreSQL's tutorial shows two 4800 salaries both at 25700). Without ORDER BY the frame is the whole partition. SQLite uses the same default. Write `ROWS` explicitly when ties must advance one row at a time.
- RANGE with an offset needs exactly one ORDER BY column and measures value distance (for example `RANGE BETWEEN '1 day' PRECEDING AND CURRENT ROW` on dates in PostgreSQL); GROUPS counts peer groups.
- Self-check: the last running total equals `sum(v)`.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual pages sql-expressions.html (window frames) and tutorial-window.html and the SQLite windowfunctions.html page; the draft's "ROWS is faster" claim is not supported by any of them and was replaced with the tie-handling explanation.
