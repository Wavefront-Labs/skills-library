---
id: computing-software.database-administration.mysql.general-query-log-capture
name: general-query-log-capture
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, mysql-server-logs, general-query-log, general-log, log-output, query-capture, audit-trail, troubleshooting]
level: practitioner
status: docs-checked
description: "Turn the MySQL general query log on briefly to capture every statement a client sends, route it to a file or table, and turn it off before it hurts the server."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/query-log.html
  - https://dev.mysql.com/doc/refman/8.4/en/log-destinations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The general query log

**Goal:** see exactly what an application sends (including connects, prepared
statement text), for minutes, not days.

## Enable at runtime (no restart)
```sql
SET GLOBAL general_log_file = '/var/lib/mysql/general-capture.log';
SET GLOBAL log_output = 'FILE';          -- or 'TABLE' (mysql.general_log) or 'FILE,TABLE'
SET GLOBAL general_log = ON;
-- reproduce the issue
SET GLOBAL general_log = OFF;
```
The log records client connects and disconnects and each SQL statement received from clients, with connection id and command type.

## Read it
```bash
grep -E '\s+[0-9]+ (Connect|Query)' general-capture.log | head
awk '$2==1234' general-capture.log    # one connection id (format: time id command argument)
```
With `log_output='TABLE'`:
```sql
SELECT event_time, thread_id, command_type, argument
FROM mysql.general_log WHERE argument LIKE '%orders%' ORDER BY event_time DESC LIMIT 100;
TRUNCATE mysql.general_log;
```

## Gotchas
- It logs every statement received, including personal data. The server rewrites plain-text passwords so they do not appear literally, unless it was started with `--log-raw` (which also logs statements that fail to parse; without it, unparseable statements are not logged). Statements with a password hash are not rewritten. Protect and delete the file afterwards.
- On a busy server it costs I/O; the log tables use the CSV engine by default (MyISAM is the only alternative). Keep sessions short.
- There is no per-user filter (`sql_log_off` only exempts the session that sets
  it). For targeted capture use Performance Schema
  `events_statements_history_long` filtered by thread, or the slow log with
  `long_query_time = 0` and filter by user afterwards.
- For permanent auditing use an audit plugin, not the general log.

## Verify
`SHOW GLOBAL VARIABLES LIKE 'general_log%';` shows OFF after the capture, and
the captured file contains the statements from the reproduction.

## Checked
Date 2026-11-01. Documentation release: MySQL 8.4 Reference Manual, The General Query Log and Selecting Log Output Destinations.
Confirmed: runtime enable/disable via general_log and general_log_file, log_output destinations, sql_log_off scope, password rewriting and --log-raw, CSV/MyISAM log tables. Corrected the failed-statement and password claims. Removed unconfirmed claims: serialisation point and the named audit plugins.
Method: documentation only; no commands were run.
