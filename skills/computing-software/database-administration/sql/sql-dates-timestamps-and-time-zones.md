---
id: computing-software.database-administration.sql.sql-dates-timestamps-and-time-zones
name: sql-dates-timestamps-and-time-zones
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-datetime, timestamp-with-time-zone, date-arithmetic, date-trunc, interval]
level: practitioner
status: docs-checked
description: "Store and query dates and times in SQL with correct time zone handling, intervals and truncation."
sources: ["https://www.postgresql.org/docs/current/datatype-datetime.html", "https://www.postgresql.org/docs/current/functions-datetime.html", "https://www.sqlite.org/lang_datefunc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dates, timestamps, time zones

- PostgreSQL types: `date`, `time`, `timestamp` (without zone), `timestamp with time zone` (`timestamptz`, a PostgreSQL abbreviation) and `interval`. Plain `timestamp` means `timestamp without time zone`, as the SQL standard requires. Time-zone-aware values are stored internally in UTC and converted for display to the session `TimeZone` setting; the zone itself is not kept. Prefer types holding both date and time when zones matter; the docs do not recommend `time with time zone`.
- Store instants in UTC (`timestamptz`); store local civil times (appointments) as local date/time plus a zone name. PostgreSQL accepts full IANA names such as `America/New_York`, which carry daylight-saving rules; abbreviations such as `PST` are a fixed offset, and `TimeZone` cannot be set to an abbreviation.
- Arithmetic in PostgreSQL: `ts + INTERVAL '1 day'`. Adding an interval handles months, then days, then microseconds in turn; local time of day is kept for months and days, and March 31 plus 1 month gives April 30. Across a DST change `+ interval '1 day'` and `+ interval '24 hours'` differ: in `America/Denver` on 2005-04-03, noon plus 1 day is 12:00 while plus 24 hours is 13:00. Choose by intent, calendar day or elapsed time.
- SQLite has no interval type: functions `date()`, `time()`, `datetime()`, `julianday()`, `unixepoch()` and `strftime()` take a time-value (ISO 8601 text, Julian day number, or Unix timestamp with the `unixepoch`/`auto` modifier) plus modifiers applied left to right, e.g. `datetime(ts, '+1 day')`, `start of month`. They use UTC internally; a trailing `Z` is a no-op and a `+HH:MM` suffix is subtracted to get UTC. The `localtime` modifier converts to local time.
- Truncate for bucketing: `date_trunc('month', ts)` in PostgreSQL (the `timestamptz` form accepts a zone argument as a third parameter, so bucket boundaries follow that zone); `start of month` / `strftime` in SQLite. Half-open ranges avoid end-of-day bugs: `ts >= '2025-01-01' AND ts < '2025-02-01'`, rather than `BETWEEN` with midnight bounds.
- `EXTRACT(field FROM ts)`: PostgreSQL offers `isoyear` (the ISO 8601 week-numbering year), whose value can differ from the calendar year near 1 January; `dow` is Sunday 0 to Saturday 6 while `isodow` is Monday 1 to Sunday 7.
- DST gaps and overlaps make local-time arithmetic ambiguous; the PostgreSQL docs warn that a fixed-offset default zone cannot adapt to DST in date arithmetic. Do arithmetic on UTC instants or with a named zone.
- In saved views, prepared statements and function definitions, avoid the input strings `now`, `today`, `tomorrow`; they can freeze at a stale value. Use `CURRENT_DATE + 1` instead.

## Checked

2026-11-08. Read: PostgreSQL 8.5 Date/Time Types (types table, time zone section, special input values), 9.9 Date/Time Functions (operators table, interval-addition text and DST example, `date_trunc` signatures, `extract` `dow`/`isodow`/`isoyear` entries), SQLite date and time functions page (time-values, UTC handling, modifiers list). Removed unconfirmed claims: SQL Server `datetimeoffset`/`DATEADD`/`DATETRUNC` and its version, MySQL `TIMESTAMP` range/2038 and `DATE_ADD`/`DATE_FORMAT`, and that `CAST(ts AS DATE)` blocks index use (not on these pages).
Method: documentation only; no commands were run.
