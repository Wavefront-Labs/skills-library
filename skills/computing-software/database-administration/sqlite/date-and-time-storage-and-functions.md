---
id: computing-software.database-administration.sqlite.date-and-time-storage-and-functions
name: date-and-time-storage-and-functions
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-date-functions, date-time, timezone, unixepoch, sqlite-schema]
level: practitioner
status: verified
description: "Store dates in SQLite as ISO-8601 text, Unix epoch integers or Julian days, and use date(), datetime(), strftime(), unixepoch() and modifiers correctly with time zones."
sources:
  - https://sqlite.org/lang_datefunc.html
  - https://sqlite.org/datatype3.html#date_and_time_datatype
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date and time storage and functions

SQLite has no date type. Pick one representation per column and stick to it.

## Representations
| Storage | Example | Pros |
|---|---|---|
| TEXT ISO-8601 (UTC) | `2026-10-18 03:15:00` or `2026-10-18T03:15:00Z` | Readable, sorts correctly as text |
| INTEGER Unix seconds | `1792293300` | Compact, fast compare, easy in apps |
| REAL Julian day | `2461331.635` | Fractional-day arithmetic |

Store UTC; convert to local time only for display.

## Functions (all return UTC unless 'localtime')
```sql
SELECT date('now');                                  -- 2026-10-18
SELECT datetime('now', '-7 days');
SELECT strftime('%Y-%m', created_at) AS month, count(*) FROM orders GROUP BY 1;
SELECT unixepoch('now');                             -- newer function, needs a recent SQLite
SELECT datetime(1792293300, 'unixepoch');            -- epoch to text
SELECT datetime(created_epoch, 'unixepoch', 'localtime');   -- uses the host's TZ
SELECT date('now', 'start of month', '+1 month', '-1 day');  -- last day of month
SELECT timediff('2026-10-18', '2026-01-01');          -- returns text like '+0000-09-17 00:00:00.000'
SELECT strftime('%W', 'now');                        -- week number
```
Fractional seconds: `strftime('%Y-%m-%d %H:%M:%f', 'now')` (`%f` = SS.SSS). the `subsec` modifier (`datetime('now','subsec')` returns milliseconds on 3.50.4). Check release notes for the version each function appeared in.

## Constraints keep data consistent
```sql
created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
  CHECK (created_at GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T*')
```

## Pitfalls
- Mixed formats in one column (`2026-10-18` and `18/10/2026`) break sorting and functions; the functions return NULL for unrecognised strings (`date('18/10/2026')` is NULL) and for bad modifiers (modifiers are case-sensitive).
- `'localtime'` uses the server process time zone, not the user's; only numeric `[+-]HH:MM` or `Z` indicators are accepted, no named zones (do conversions in the application). Behaviour comes from the C library `localtime_r`; `localtime` on a non-UTC value is undefined.
- Indexes: compare the stored column directly (`created_at >= '2026-10-01'`); wrapping it in `date(created_at)` prevents index use unless you create an index on that expression.

## Verify
`SELECT count(*) FROM orders WHERE datetime(created_at) IS NULL` returns 0 (all values parse).
