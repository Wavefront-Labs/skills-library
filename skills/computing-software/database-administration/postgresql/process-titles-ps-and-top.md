---
id: computing-software.database-administration.postgresql.process-titles-ps-and-top
name: process-titles-ps-and-top
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-process-title, ps, top, update-process-title, cluster-name, os-monitoring]
level: practitioner
status: docs-checked
description: "Read PostgreSQL backend activity from the OS with ps and top: process title format, cluster_name, mapping a hot PID to its query, and update_process_title."
sources:
  - https://www.postgresql.org/docs/current/monitoring-ps.html
  - https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-CLUSTER-NAME
  - https://www.postgresql.org/docs/current/runtime-config-statistics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Process titles with ps and top

Each PostgreSQL process rewrites its command line to show what it is doing.

```bash
ps auxww | grep ^postgres
# postgres: checkpointer
# postgres: walwriter
# postgres: autovacuum launcher
# postgres: joe runbug 127.0.0.1 idle
# postgres: tgl regression [local] SELECT waiting
# postgres: tgl regression [local] idle in transaction
```
Format for client backends: `postgres: [cluster_name:] user database host activity`. Activity is `idle`, `idle in transaction` or a command type such as `SELECT`; `waiting` is appended when the process waits on a lock held by another session (check `pg_locks` to find the blocker). The exact ps invocation varies by platform.

## Settings
```ini
cluster_name = 'main'              # shown in every title when set; useful on hosts with several clusters
update_process_title = on          # if off, the title is set only when the process starts
```

## Map a hot OS process to SQL
```bash
top -c -u postgres                  # note the PID burning CPU
```
```sql
SELECT pid, usename, datname, state, wait_event_type, wait_event, now()-query_start AS runtime, query
FROM pg_stat_activity WHERE pid = 12345;
SELECT pg_cancel_backend(12345);    -- cancel the query
SELECT pg_terminate_backend(12345); -- end the session
```

## Useful OS views
```bash
pidstat -d -p $(pgrep -d, -u postgres) 5      # per-process disk I/O
cat /proc/<pid>/status | grep -E 'VmRSS|VmHWM' # memory of one backend
```

## Gotchas
- The title shows only the command type (SELECT/UPDATE), not the query text; join to pg_stat_activity for the query.

## Checked

2026-10-28. Confirmed against PostgreSQL current docs (version 18) section 27.1 Standard Unix Tools: ps sample output, title format `postgres: user database host activity`, idle / idle in transaction / command type / waiting meanings, cluster_name shown when set, update_process_title off means the title is set once at start. Removed unconfirmed: ps --sort flags, ports in titles, per-platform default of update_process_title, kill -9 recovery behaviour, PSS/smem advice, work_mem and pooler server_lifetime remarks, container remark.

Method: documentation only; no commands were run.
