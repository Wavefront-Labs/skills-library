---
id: computing-software.database-administration.schema-design.timestamps-and-time-zones
name: timestamps-and-time-zones
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, data-type-selection, timestamptz, time-zones, utc, datetimeoffset, local-time-events, iana-tz, dst]
level: practitioner
status: gated
description: "Store instants and civil times correctly: timestamptz/UTC for events, local time plus IANA zone for future appointments, and the per-engine type traps (MySQL, SQL Server, Oracle)."
sources:
  - https://www.postgresql.org/docs/current/datatype-datetime.html
  - https://dev.mysql.com/doc/refman/8.4/en/datetime.html
  - https://learn.microsoft.com/en-us/sql/t-sql/data-types/datetimeoffset-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timestamps and time zones

**Goal:** every time value means one unambiguous thing, across servers, DST
changes and client time zones.

## Two different kinds of time
1. **Instants** (something happened: order placed, login): store as an absolute
   point in time (UTC).
2. **Civil/wall-clock times** in the future (meeting at 09:00 Berlin next
   March): store local date-time **plus the IANA zone id** (`Europe/Berlin`),
   because DST rules can change before then; convert to an instant when needed.

## Per engine
| Engine | Instants | Notes |
|---|---|---|
| PostgreSQL | `timestamptz` | Stores UTC, converts on I/O using session `TimeZone`. `timestamp` (without tz) has no zone: avoid for instants |
| MySQL | `DATETIME(6)` with UTC by convention, or `TIMESTAMP` | `TIMESTAMP` converts via session time_zone and its range ends at 2038-01-19 03:14:07 UTC; DATETIME (1000-01-01 to 9999-12-31) has no conversion (MySQL manual) |
| SQL Server | `datetime2(3..7)` in UTC, or `datetimeoffset` | `datetime` legacy: 3.33 ms precision; `datetimeoffset` keeps an offset, not a zone (gated: unconfirmed, source is paywalled or blocked) |
| Oracle | `TIMESTAMP WITH TIME ZONE` or `TIMESTAMP WITH LOCAL TIME ZONE` | `DATE` has seconds but no fractional/zone (gated: unconfirmed, source is paywalled or blocked) |
| SQLite | ISO-8601 TEXT in UTC (`2026-10-16T14:03:12Z`) or unix epoch INTEGER | No native type |

## Rules
- Server/DB/session time zones: set to UTC for consistency (`timezone = 'UTC'`
  in postgresql.conf; MySQL `default-time-zone='+00:00'`), but write code that
  does not depend on it.
- Convert to local time at the edge (UI/report), using the user's IANA zone.
- Date-only business facts (birthday, invoice date) are `date`, not midnight timestamps.
- Range queries on day boundaries in a user's zone: compute the UTC bounds
  (`WHERE created_at >= '2026-10-16 00:00 Europe/Berlin'::timestamptz AND created_at < ...`; that literal is 2026-10-15 22:00 UTC, checked),
  don't wrap the column in a conversion function (kills index use).

## Gotchas
- Offsets (`+02:00`) are not zones: they don't know DST.
- Keep the OS/DB tz database updated (PostgreSQL bundles tzdata in some builds; MySQL needs its time zone tables loaded for named zones (gated: unconfirmed, source is paywalled or blocked)).
- JSON APIs: send ISO-8601 with `Z` or an offset; never naive strings.

## Verify
Insert a value from clients in two time zones and read it back in a third: the
instant is identical; schema review finds no `timestamp without time zone`/naive
DATETIME columns storing events without a documented UTC convention.
