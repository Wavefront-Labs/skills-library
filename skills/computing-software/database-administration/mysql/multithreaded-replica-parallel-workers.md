---
id: computing-software.database-administration.mysql.multithreaded-replica-parallel-workers
name: multithreaded-replica-parallel-workers
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, replica-parallel-workers, multithreaded-replica, logical-clock, writeset, replica-preserve-commit-order, binlog-transaction-dependency-tracking, replication-lag]
level: practitioner
status: docs-checked
description: "Cut MySQL replica lag with multithreaded apply: replica_parallel_workers, LOGICAL_CLOCK, WRITESET dependency tracking, commit order and worker monitoring."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/replication-options-replica.html#sysvar_replica_parallel_workers
  - https://dev.mysql.com/doc/refman/8.4/en/replication-threads.html
  - https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_binlog_transaction_dependency_tracking
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multithreaded replicas

**Goal:** the replica applies in parallel what the source committed in parallel, so lag stops growing under write load.

## Settings
```ini
# replica
replica_parallel_workers = 8           # default 4; 0/1 = single-threaded (0 is deprecated)
replica_parallel_type = LOGICAL_CLOCK  # default (the variable is deprecated in 8.4; LOGICAL_CLOCK is the policy to keep)
replica_preserve_commit_order = ON     # default ON; commits in source order, keeps replica state consistent
# source (8.0 only; in 8.4 both variables are gone and dependency tracking is writeset-based)
binlog_transaction_dependency_tracking = WRITESET
transaction_write_set_extraction = XXHASH64
```
**WRITESET** marks transactions as independent when they touched different rows (by PK/unique key hashes), even if they were not concurrent on the source. With only COMMIT_ORDER, a source with low concurrency gives the replica nothing to parallelise.

## Check it is working
```sql
SELECT WORKER_ID, THREAD_ID, SERVICE_STATE, LAST_APPLIED_TRANSACTION, APPLYING_TRANSACTION
FROM performance_schema.replication_applier_status_by_worker;
```
If one worker does all the work, dependencies serialise transactions: tables without PKs, hot rows, or large transactions. sys schema / Performance Schema `events_transactions_summary_by_thread_by_event_name` help count per worker.

## What still serialises
- Tables without primary/unique keys (WRITESET cannot hash rows): add PKs (`sql_require_primary_key = ON`).
- DDL (runs alone).
- Huge transactions (one worker, and `replica_pending_jobs_size_max` limits event queue size).
- Foreign key cascades across workers are handled but reduce parallelism.

## Gotchas
- With `replica_preserve_commit_order = OFF`, the replica can expose states the source never had; reads may see gaps (and `Executed_Gtid_Set` has holes after a crash until `START REPLICA UNTIL SQL_AFTER_MTS_GAPS`).
- More workers than cores and I/O can handle helps nothing; benchmark 4/8/16.
- Seconds_Behind_Source can jump around with MTS; prefer heartbeat-based lag.

## Verify
Under a write benchmark on the source, replica lag stays flat and several workers show non-zero applied transactions.

## Checked

2026-10-31: confirmed on dev.mysql.com 8.4 pages: replica_parallel_workers default 4 (multithreading on by default; 0 deprecated), replica_parallel_type default LOGICAL_CLOCK with the variable deprecated, replica_preserve_commit_order default ON, replica_pending_jobs_size_max default 128MB (soft limit), coordinator/worker threads and per-channel threading (replication-options-replica, replication-threads), START REPLICA UNTIL SQL_AFTER_MTS_GAPS gap handling, replication_applier_status_by_worker monitoring, and the absence of binlog_transaction_dependency_tracking and transaction_write_set_extraction from the 8.4 binary log options (both removed; binlog_transaction_dependency_history_size remains). Removed the 8.0.27+ version notes.
Method: documentation only; no commands were run.
