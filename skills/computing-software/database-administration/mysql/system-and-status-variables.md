---
id: computing-software.database-administration.mysql.system-and-status-variables
name: system-and-status-variables
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, system-variables-mysql, show-global-status, show-variables, performance-schema, global-vs-session, dynamic-variables, mysql-monitoring]
level: practitioner
status: docs-checked
description: "Read and change MySQL system variables (global vs session, dynamic vs read-only) and turn SHOW GLOBAL STATUS counters into rates that diagnose load."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/using-system-variables.html
  - https://dev.mysql.com/doc/refman/8.4/en/server-status-variables.html
  - https://dev.mysql.com/doc/refman/8.4/en/performance-schema-system-variable-tables.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System variables and status variables

## System variables (configuration)
```sql
SHOW GLOBAL VARIABLES LIKE 'innodb_buffer_pool_size';
SELECT @@GLOBAL.sort_buffer_size, @@SESSION.sort_buffer_size;
SET GLOBAL max_connections = 800;            -- dynamic: new value now, lost on restart
SET PERSIST max_connections = 800;           -- also written to mysqld-auto.cnf
SET PERSIST_ONLY innodb_log_buffer_size = 64*1024*1024;   -- read-only var: applied at next restart
SET SESSION sql_mode = 'STRICT_TRANS_TABLES';
```
- Scope: some variables are global-only, some session-only, most both. A session copy is initialised from the global at connect time, so `SET GLOBAL` does not affect existing sessions.
- Read-only variables (e.g. `innodb_log_file_size` in old versions, `innodb_buffer_pool_instances`) error with `Variable ... is a read only variable`.

Where a value came from:
```sql
SELECT VARIABLE_NAME, VARIABLE_SOURCE, VARIABLE_PATH, SET_TIME, SET_USER
FROM performance_schema.variables_info WHERE VARIABLE_NAME = 'max_connections';
-- VARIABLE_SOURCE: COMPILED, GLOBAL (my.cnf), PERSISTED, DYNAMIC, COMMAND_LINE ...
```

## Status variables (counters)
Most are cumulative since startup (`Uptime`). A raw value means little; compute rates between two samples.
```bash
mysqladmin -r -i 10 extended-status | grep -E 'Questions|Com_select|Com_insert|Threads_running|Innodb_rows_read'
```
`-r` shows the difference between samples.

## Counters worth knowing
| Status | Look for |
|---|---|
| `Threads_running` | sustained > CPU cores = contention or slow queries |
| `Threads_connected` / `Max_used_connections` | near `max_connections` |
| `Questions`, `Com_*` | QPS and mix |
| `Innodb_buffer_pool_reads` vs `..._read_requests` | disk reads per logical read (miss ratio) |
| `Created_tmp_disk_tables` / `Created_tmp_tables` | temp tables spilling to disk |
| `Select_full_join`, `Select_scan` | joins without indexes, full scans |
| `Opened_tables` rate | table cache too small |
| `Aborted_clients` / `Aborted_connects` | app not closing / auth failures |
| `Innodb_row_lock_waits`, `..._time_avg` | row lock contention |
| `Slow_queries` | rate against long_query_time |

```sql
SELECT * FROM performance_schema.global_status WHERE VARIABLE_NAME IN ('Threads_running','Questions','Uptime');
SELECT * FROM sys.metrics WHERE Variable_name LIKE 'innodb_buffer_pool%';
```

## Gotchas
- `SHOW STATUS` without GLOBAL shows **session** counters (mostly tiny); always say GLOBAL for server-wide numbers.
- `FLUSH STATUS` resets session counters and some global ones; avoid in monitoring setups that compute deltas.
- MariaDB has different names for some variables; check before copying settings.

## Checked

2026-10-31: confirmed SET GLOBAL/SET PERSIST/SET PERSIST_ONLY syntax and the mysqld-auto.cnf persisted-variables file, session variables initialized from globals at connect time, and performance_schema variables_info (VARIABLE_SOURCE values COMPILED, GLOBAL, PERSISTED, DYNAMIC, COMMAND_LINE, EXPLICIT, EXTRA, LOGIN, SERVER, USER; VARIABLE_PATH, SET_TIME, SET_USER, SET_HOST), global_variables/session_variables/persisted_variables, and performance_schema.global_status on dev.mysql.com 8.4 pages. No claims removed.
Method: documentation only; no commands were run.
