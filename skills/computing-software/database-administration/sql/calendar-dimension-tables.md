---
id: computing-software.database-administration.sql.calendar-dimension-tables
name: calendar-dimension-tables
category: computing-software
field: database-administration
product: sql
tags: [sql, calendar-dimension-tables]
level: practitioner
status: docs-checked
description: "Generate a PostgreSQL calendar table with generate_series and extract(isodow ...), using typed timestamp arguments."
sources: ["https://www.postgresql.org/docs/current/functions-srf.html", "https://www.postgresql.org/docs/current/functions-datetime.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calendar dimension tables

- Generate rows with `generate_series(start, stop, interval '1 day')`. With `timestamp` arguments it returns `timestamp`; with `timestamptz` arguments it returns `timestamptz`, so cast literals deliberately, for example `timestamp '2026-01-01'`.
- `extract(isodow FROM d)` gives Monday (1) to Sunday (7); `extract` returns `numeric`.
- Derive weekday flags from `isodow`, for example `isodow IN (6, 7)` for a weekend flag. Holidays are not computed by any function; load them from your own list.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
Read: the generate_series entries on the set-returning functions page and the extract/isodow entries on the date/time functions page.
Trimmed: unsourced advice. Corrected: literals are typed as timestamp so the result type is known.
