---
id: computing-software.database-administration.mysql.undo-logs-and-history-list-length
name: undo-logs-and-history-list-length
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, innodb, history-list-length, undo-tablespace, purge-lag, long-running-transaction, innodb-undo-log-truncate, mvcc]
level: advanced
status: docs-checked
description: "Diagnose growing InnoDB history list length (purge lag) caused by long transactions, tune purge threads, and truncate bloated undo tablespaces in MySQL 8."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-purge-configuration.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-undo-tablespaces.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Undo logs and history list length

**Goal:** old row versions are purged promptly so queries stay fast and undo
tablespaces don't grow without bound.

## What HLL measures
Every change leaves an undo record for MVCC. Purge threads remove records no
transaction can still need. History list length (HLL) = number of unpurged
transactions' undo logs. Healthy: thousands. Problem: millions, growing.
```sql
SELECT count FROM information_schema.innodb_metrics WHERE name = 'trx_rseg_history_len';
SHOW ENGINE INNODB STATUS\G      -- "History list length 4123456" in TRANSACTIONS section
```
Symptoms of high HLL: queries slower over time (walking long version chains),
undo tablespaces growing, higher CPU.

## Cause #1: a long-running (or forgotten) transaction
Purge cannot pass the oldest open read view, even an idle one, even
`REPEATABLE READ` read-only:
```sql
SELECT trx_id, trx_mysql_thread_id, trx_started, TIMESTAMPDIFF(SECOND, trx_started, NOW()) AS age_s,
       trx_rows_modified, trx_query
FROM information_schema.innodb_trx ORDER BY trx_started LIMIT 5;
```
Kill or fix it (app not committing, a long consistent-snapshot backup, a stuck replica SQL thread). Set `wait_timeout` and app-side timeouts.

## Cause #2: purge can't keep up with heavy writes
```ini
innodb_purge_threads = 4                # restart needed; default 1 up to 16 logical processors, else 4; max 32
innodb_max_purge_lag = 1000000          # throttle DML when HLL exceeds this (0 = off, default)
innodb_max_purge_lag_delay = 300000     # upper limit of the imposed delay, microseconds (default 0)
```
Throttling DML protects read performance at the cost of write latency; use with care.

## Shrinking undo tablespaces
Undo lives in separate tablespaces (`innodb_undo_001`, `_002`; files `undo_001`, `undo_002`). With
`innodb_undo_log_truncate = ON` (default), a tablespace above
`innodb_max_undo_log_size` (1024 MiB default) is marked for truncation; at least two active undo tablespaces are required. Manual:
```sql
CREATE UNDO TABLESPACE undo_003 ADD DATAFILE 'undo_003.ibu';
ALTER UNDO TABLESPACE innodb_undo_001 SET INACTIVE;   -- truncated when empty, then
ALTER UNDO TABLESPACE innodb_undo_001 SET ACTIVE;
```
Truncating undo logs that reside in the system tablespace is not supported.

## Verify
HLL returns to its baseline after the long transaction ends; undo tablespace file
sizes (locations via `INFORMATION_SCHEMA.FILES`) shrink back after truncation.

## Checked

2026-11-01. Confirmed against MySQL 8.4 manual pages innodb-undo-tablespaces, innodb-parameters (purge/undo variable defaults and ranges), innodb-information-schema-metrics-table, information-schema-innodb-trx-table, innodb-standard-monitor. Corrected the innodb_purge_threads default; removed unconfirmed mysqldump and 5.7 claims.

Method: documentation only; no commands were run.
