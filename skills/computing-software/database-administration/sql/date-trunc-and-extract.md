---
id: computing-software.database-administration.sql.date-trunc-and-extract
name: date-trunc-and-extract
category: computing-software
field: database-administration
product: sql
tags: [sql, date-trunc-and-extract]
level: practitioner
status: docs-checked
description: "Truncate, extract and format dates with date_trunc, EXTRACT and to_char."
sources: ["https://www.postgresql.org/docs/current/functions-datetime.html", "https://www.postgresql.org/docs/current/functions-formatting.html", "https://www.sqlite.org/lang_datefunc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# date_trunc extract and formatting

- `date_trunc('day', ts)`, `extract(dow from ts)` (Sunday 0 to Saturday 6), `extract(isodow from ts)` (Monday 1 to Sunday 7; ISO weeks start on Monday), `to_char(ts, 'YYYY-MM-DD HH24:MI')`.
- SQLite: `strftime('%Y-%m', ts)`, `%w` weekday 0 = Sunday.
- `date_trunc(field, timestamptz, zone)` truncates in the given time zone, for example `date_trunc('day', ts, 'UTC')`.
- Self-check: truncate a known timestamptz with two different zone arguments and compare the day boundaries.

## Checked

2026-11-02. Confirmed: dow and isodow numbering, ISO weeks start on Monday, the three-argument date_trunc with a zone, to_char on timestamps (PostgreSQL date/time and formatting pages); SQLite `%w` is day of week 0-6 with Sunday 0 (date functions page). Removed: the PostgreSQL 12 attribution and the unstated session-TimeZone claim.
Method: documentation only; no commands were run.
