---
id: computing-software.database-administration.mysql.innodb-locking-and-deadlocks
name: innodb-locking-and-deadlocks
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, innodb, innodb-deadlock, innodb-lock-wait-timeout, gap-locks, next-key-locks, data-locks, innodb-print-all-deadlocks, lock-waits]
level: advanced
status: docs-checked
description: "Diagnose InnoDB lock waits and deadlocks: next-key and gap locks, performance_schema.data_locks and data_lock_waits, the deadlock report, and the fixes that remove them."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-deadlocks-handling.html
  - https://dev.mysql.com/doc/refman/8.4/en/performance-schema-data-locks-table.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InnoDB locking and deadlocks

**Goal:** explain why a statement waits or deadlocks and change the code or
index so it stops.

## Lock types you will see
- **Record lock** on an index entry; **gap lock** on the range between entries;
  **next-key lock** = record + preceding gap (default in REPEATABLE READ for
  locking reads, UPDATE and DELETE). Gap locks stop inserts into the range
  (phantom prevention), the source of most "why is my INSERT blocked?" cases.
- Locks are taken on **index entries scanned**, not rows returned: an UPDATE
  with no usable index locks every row it scans (effectively the table).
- READ COMMITTED disables most gap locking (only FK/duplicate checks use them).

## Who blocks whom (8.0)
```sql
SELECT * FROM sys.innodb_lock_waits\G     -- waiting_query, blocking_query, blocking_pid, sql_kill_blocking_query
SELECT * FROM performance_schema.data_locks WHERE object_name = 'orders';
```
Waits end with a lock wait timeout error after
`innodb_lock_wait_timeout` (50 s default; only the statement rolls back unless
`innodb_rollback_on_timeout` is enabled at startup).

## Deadlocks
InnoDB detects cycles and rolls back one of the transactions with a deadlock error (restart the transaction).
```sql
SHOW ENGINE INNODB STATUS\G      -- LATEST DETECTED DEADLOCK: both statements and locks
SET PERSIST innodb_print_all_deadlocks = ON;   -- log every deadlock to the error log
```
Common causes and fixes:
- Two transactions updating the same rows in different order → always touch rows in a consistent order (sort ids).
- Missing index makes UPDATE/DELETE scan and lock extra rows → add the index.
- `INSERT ... ON DUPLICATE KEY UPDATE` / insert-after-select patterns on the same gap → use READ COMMITTED, or unique constraints with retry.
- Large batch transactions → smaller batches.
Applications must retry on the deadlock error (and usually on lock wait timeouts).

## Gotchas
- Very high concurrency: deadlock detection itself costs CPU; the `innodb_deadlock_detect` variable can disable it, relying on a low `innodb_lock_wait_timeout`.
- Foreign key checks take shared locks on parent rows.

## Verify
No new deadlocks in the error log (with `innodb_print_all_deadlocks`),
and `Innodb_row_lock_waits` / `Innodb_row_lock_time_avg` status counters drop after the fix.

## Checked

2026-11-01. Confirmed against MySQL 8.4 manual pages innodb-locks-set, innodb-deadlocks, innodb-deadlock-detection, innodb-parameters (innodb_lock_wait_timeout, innodb_rollback_on_timeout, innodb_print_all_deadlocks), sys-innodb-lock-waits. Removed unconfirmed error numbers, column lists and the innodb_metrics counter.

Method: documentation only; no commands were run.
