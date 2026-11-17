---
id: computing-software.database-administration.mysql.processlist-thread-states-and-kill
name: processlist-thread-states-and-kill
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-optimization, show-processlist, thread-states, kill-query, performance-schema, incident-response]
level: practitioner
status: docs-checked
description: "Read SHOW PROCESSLIST and performance_schema.processlist during an incident: what thread states mean, finding the blocker, and KILL vs KILL QUERY."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/show-processlist.html
  - https://dev.mysql.com/doc/refman/8.4/en/general-thread-states.html
  - https://dev.mysql.com/doc/refman/8.4/en/kill.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SHOW PROCESSLIST, thread states and KILL

## Views
```sql
SHOW FULL PROCESSLIST;                                   -- needs PROCESS to see others
SELECT * FROM performance_schema.processlist WHERE command <> 'Sleep' ORDER BY time DESC;
SELECT * FROM sys.session\G   -- processlist plus transaction, lock and memory detail
```

## States worth recognising
| State | Meaning / action |
|---|---|
| `Sending data` (5.7) / `executing` (8.0) | doing work: reading rows; long times = slow query |
| `Waiting for table metadata lock` | blocked by a metadata lock; find the session holding the table (often an idle open transaction) |
| row lock waits | look in `sys.innodb_lock_waits` |
| `Creating sort index` / `Sorting result` | filesort; big ones spill to disk |
| `Copying to tmp table on disk` / `converting HEAP to ondisk` | internal temp table spilled |
| `Opening tables` / `Waiting for table flush` | table cache pressure, or a `FLUSH TABLES` waiting on a long query |
| `System lock`, `checking permissions` (long) | usually I/O or global contention |
| `Sleep` with large `Time` and an open transaction | idle in transaction: holds locks and history list |

## Find the blocker
```sql
SELECT * FROM sys.innodb_lock_waits\G               -- waiting_query, blocking_pid, sql_kill_blocking_query
SELECT * FROM sys.schema_table_lock_waits\G          -- metadata locks, with sql_kill_blocking_connection
SELECT trx_mysql_thread_id, trx_started, trx_rows_modified, trx_query
FROM information_schema.innodb_trx ORDER BY trx_started LIMIT 5;
```

## Killing
```sql
KILL QUERY 1234;      -- stop the statement, keep the connection (transaction stays open)
KILL 1234;            -- close the connection; its transaction rolls back
```
- Rolling back a big transaction takes time; the thread shows `Killed` / `rollback` state.
  Killing again does nothing; restarting mysqld only moves the rollback to crash recovery.
  Watch `trx_rows_modified` decrease in `innodb_trx`.
- `KILL` requires `CONNECTION_ADMIN` for other users' threads.

## Gotchas
- `Time` is seconds in the current state, not the whole transaction age; use
  the transaction start time in `information_schema.innodb_trx` for that.
- Replication threads appear as `system user`; stop replication instead of killing them.

## Verify
After killing the root blocker, `sys.innodb_lock_waits` and `schema_table_lock_waits` are
empty and the processlist returns to normal.

## Checked

2026-11-01. Confirmed against MySQL 8.4 manual pages show-processlist, general-thread-states, kill (CONNECTION_ADMIN rule), sys-session, sys-innodb-lock-waits, sys-schema-table-lock-waits, performance-schema-processlist-table. Removed unconfirmed claims (performance_schema_show_processlist, version gate, RDS procedures, one state row).

Method: documentation only; no commands were run.
