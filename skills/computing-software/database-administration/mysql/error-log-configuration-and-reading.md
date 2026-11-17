---
id: computing-software.database-administration.mysql.error-log-configuration-and-reading
name: error-log-configuration-and-reading
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, mysql-server-logs, mysql-error-log, log-error-verbosity, log-sink-json, performance-schema-error-log, startup-failure, crash-diagnosis]
level: practitioner
status: docs-checked
description: "Configure and read the MySQL error log (log_error, verbosity, JSON sink, performance_schema.error_log) to diagnose startup failures, crashes and replication errors."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/error-log.html
  - https://dev.mysql.com/doc/refman/8.4/en/error-log-configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The MySQL error log

**Goal:** know where the error log is, keep the right detail in it, and read it
first whenever mysqld will not start, restarts, or replication stops.

## Where it is
```sql
SELECT @@log_error, @@log_error_verbosity, @@log_error_services;
```
Defaults: with `--log-error` absent or given without a file name, `<hostname>.err` in the data directory. Yum and APT packages commonly set a file under `/var/log` (for example `log-error=/var/log/mysqld.log`); remove the path from the option to fall back to the data directory file. If `log_error` is `stderr`, output goes to the console, where the service manager captures it.

## Configure (my.cnf, [mysqld])
```ini
log_error = /var/log/mysql/error.log
log_error_verbosity = 2        # 1 errors, 2 + warnings, 3 + information (default 2)
log_timestamps = SYSTEM        # default UTC; SYSTEM uses the local time zone
# JSON output in addition to classic:
log_error_services = 'log_filter_internal; log_sink_internal; log_sink_json'
```
Rotate by moving the file and running `FLUSH ERROR LOGS;` (mysqld reopens it).

## Query it with SQL
```sql
SELECT LOGGED, PRIO, ERROR_CODE, SUBSYSTEM, DATA
FROM performance_schema.error_log
WHERE PRIO IN ('Error','Warning') ORDER BY LOGGED DESC LIMIT 50;
```
Useful when you have SQL access but no shell (managed services expose the log
through their console instead).

## What to look for
- Startup failures: read upward from the final abort line to the real cause (bad option in my.cnf, port in use, data directory permissions).
- Crashes: a stack trace in the log. An OS out-of-memory kill leaves no trace here; check the OS kernel log.
- Replication: the SQL/applier thread error and its error code.

## Gotchas
- `log_error_verbosity = 3` in busy systems adds information-priority events; SYSTEM-priority messages (startup, shutdown) are logged regardless of the value.
- Error log is not the general log or slow log; those are separate files.

## Verify
Restart mysqld and confirm the startup messages appear with correct timestamps in the configured file.

## Checked

2026-11-01. Confirmed against MySQL 8.4 manual pages error-log-configuration, error-log-destination-configuration, error-log-components, server-system-variables (log_error_verbosity values and default 2, log_timestamps UTC default and SYSTEM), flush. Removed unconfirmed package paths, journalctl, logrotate, version gate and specific message codes.

Method: documentation only; no commands were run.
