---
id: computing-software.database-administration.mysql.time-zone-support-and-tzinfo
name: time-zone-support-and-tzinfo
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-time-zone, mysql-tzinfo-to-sql, time-zone, timestamp-vs-datetime, convert-tz, dst]
level: practitioner
status: verified
description: "Configure MySQL time zones: system vs server vs session time_zone, load zone tables with mysql_tzinfo_to_sql, and TIMESTAMP vs DATETIME behaviour."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/time-zone-support.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysql-tzinfo-to-sql.html
  - https://dev.mysql.com/doc/refman/8.4/en/datetime.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time zone support and loading time zone tables

## Three settings
- `system_time_zone`: the OS zone at startup (read-only; on this Windows host it read `E. Australia Standard Time`, a Windows name rather than an IANA one).
- `time_zone` (global, default `SYSTEM`): server's zone for sessions.
- `time_zone` (session): what the client sees. Set per connection: `SET time_zone = '+00:00';`.

Recommended: run hosts in UTC and set `default-time-zone = '+00:00'` in my.cnf so behaviour does not depend on the OS. With `SYSTEM`, every timestamp conversion calls the C library and can contend (a known scalability issue under load).

## Named zones need the zone tables
`SET time_zone = 'Europe/London'` fails with `Unknown or incorrect time zone` until `mysql.time_zone*` tables are loaded:
```bash
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
```
That is the Linux/macOS path (not run here). Reload after OS tzdata updates (DST rule changes). **On Windows** `mysql_tzinfo_to_sql` could not read a zoneinfo directory (the tzdata package's folder gave `Warning: ... is not regular file or directory` for every zone and `There were fatal errors`), so use the downloadable SQL package from https://dev.mysql.com/downloads/timezones.html as the manual says for systems without a zoneinfo database: the `timezone_2026e_posix_sql.zip` it linked unpacked to `timezone_posix.sql`, and `mysql mysql < timezone_posix.sql` loaded 598 names. The manual warns not to use the package on a system that has a zoneinfo database. Restart is not required, but cached zones in running sessions may keep old rules until reconnect (documented behaviour, not tested).

Verify:
```sql
SELECT CONVERT_TZ('2026-03-29 00:30:00', 'UTC', 'Europe/London');   -- NULL means tables not loaded (and `SET time_zone='Europe/London'` gives error 1298); after loading: 2026-03-29 00:30:00 (still GMT) and, for 01:30 UTC, 02:30:00 (BST began)
SELECT COUNT(*) FROM mysql.time_zone_name;
```

## TIMESTAMP vs DATETIME
| | TIMESTAMP | DATETIME |
|---|---|---|
| Stored as | UTC, converted from/to session `time_zone` | literal value, no conversion |
| Range | 1970-2038 (Y2038 limit; inserting 2040 gave `Out of range value for column` on 9.7.4) | 1000-9999 (manual) |
| Changing session zone | changes displayed value | no change |

Pick one convention: DATETIME holding UTC (app converts) avoids 2038 and surprises; TIMESTAMP is fine when all sessions set the zone consistently.

## Replication
Statement-based binlogs record the session `time_zone` with each event (`mysqlbinlog` showed `SET @@session.time_zone='Europe/London'` before the statement and `'+00:00'` before the next); row-based logs store values. Keep `time_zone` identical on source and replicas anyway, and load the same zone tables on every server (the manual's replication section covers how the zone tables replicate; not tested here).

## Gotchas
- `NOW()` returns session-zone time; `UTC_TIMESTAMP()` is unaffected.
- DST gaps: a local time that does not exist (for example `2026-03-29 01:30:00` in `Europe/London`) is **not** silently accepted in the default strict mode: inserting it into a TIMESTAMP failed with `ERROR 1292 Incorrect datetime value`; with `sql_mode=''` it was stored as `02:00:00` with warning 1299 `Invalid TIMESTAMP value`.
- Since 8.0.19 literals can carry an offset: `'2026-10-18 10:00:00+02:00'`. The offset is applied and not stored: with `time_zone='Europe/London'` the value was stored and read back as `2026-10-18 09:00:00` in both TIMESTAMP and DATETIME columns.
