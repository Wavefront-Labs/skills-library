---
id: computing-software.database-administration.postgresql.log-file-rotation-and-retention
name: log-file-rotation-and-retention
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, logging-collector, log-rotation, log-truncate-on-rotation, log-filename, logrotate, disk-full]
level: practitioner
status: verified
description: "Rotate and expire PostgreSQL server logs with logging_collector (log_filename patterns, truncate-on-rotation) or logrotate, so logs never fill the data volume."
sources:
  - https://www.postgresql.org/docs/current/logfile-maintenance.html
  - https://www.postgresql.org/docs/current/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-WHERE
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log file rotation and retention

**Goal:** a bounded amount of log history, rotated automatically, on a volume
where a log burst cannot stop the database.

## Built-in collector with self-expiring names
```conf
logging_collector = on                   # restart required
log_directory = '/var/log/postgresql'    # outside the data dir; owned by postgres
log_filename = 'postgresql-%a.log'       # Mon..Sun: 7-day ring
log_rotation_age = 1d
log_rotation_size = 0                    # no size-based rotation: truncation happens only on time-based rotation
log_truncate_on_rotation = on            # overwrite last week's file instead of appending
```
Other patterns: `postgresql-%H.log` (24-hour ring, rotation_age 1h),
`postgresql-%Y-%m-%d_%H%M%S.log` (the default pattern: unique names, so it needs an external cleanup job).
Force a rotation now: `SELECT pg_rotate_logfile();`. Current file:
`SELECT pg_current_logfile();` (`pg_current_logfile('jsonlog')` for the JSON file).

## External rotation tools
If you only redirect the server's stderr to a file, the only way to truncate it is a restart; pipe it
to a rotation program or use the collector (docs, "Log File Maintenance"). You can also let an external
tool such as logrotate archive files the collector produces: the collector keeps naming and locating
them, and the tool must make the server write to a new file afterwards. Stanzas for those tools are not
reproduced here because they were not run.

## Shipping
For central logging, prefer `jsonlog` (one JSON object per line, PG15+) or `csvlog` with a log shipper
tailing the directory, or `log_destination = 'syslog'` (`eventlog` on Windows).

## Gotchas
- Default `log_directory = 'log'` lives inside PGDATA: a log storm (e.g. an error
  loop with `log_min_duration_statement = 0`) fills the data volume and stops the
  server. Put logs on a separate filesystem.
- `log_truncate_on_rotation` only truncates on **time-based** rotation to an
  existing file name, not on restart or size rotation.
- Retention may be governed by audit policy: confirm how long logs must be kept.

## Verify
Listing the log directory shows at most the expected number of files with recent mtimes;
`pg_rotate_logfile()` returns `t` and opens a new file. `pg_current_logfile()` changes only if the
name pattern produces a new name (with the `%a` ring it stays the same until the weekday changes).

## Checked
- PostgreSQL 18.6: `logging_collector = on` with `log_directory` set to an absolute directory, `log_filename = 'postgresql-%a.log'`, `log_rotation_size = 0`, `log_truncate_on_rotation = on` and `log_destination = 'jsonlog'` applied on reload (log_directory, filename and destination are `sighup`; `logging_collector` is `postmaster`); files `postgresql-Thu.json` (JSON lines) and `postgresql-Thu.log` appeared; `pg_current_logfile()` and `pg_current_logfile('jsonlog')` returned the JSON path; `pg_rotate_logfile()` returned `t`, and the name stayed `postgresql-Thu.json` as expected for a weekday ring. Default `log_directory` is `log` (relative to PGDATA), default `log_filename` `postgresql-%Y-%m-%d_%H%M%S.log`, default `log_rotation_age` 1440 min, `log_rotation_size` 10240 kB.
- Docs (runtime-config-logging, logfile-maintenance): truncate-on-rotation only for time-based rotation, the `%H` 24-file and `%a` 7-day examples, stderr redirect needs a restart to truncate, logrotate pairing with the collector; PG15 release notes add `jsonlog`.
- Removed the Debian `pg_ctlcluster` claim, the `find ... -delete` cron line and the logrotate stanza (Linux-only, not run).
