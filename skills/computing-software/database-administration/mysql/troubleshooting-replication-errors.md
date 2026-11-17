---
id: computing-software.database-administration.mysql.troubleshooting-replication-errors
name: troubleshooting-replication-errors
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, gtid, binlog, replication-error-1062, error-1032, skip-transaction, replica-drift]
level: advanced
status: docs-checked
description: "Fix a stopped MySQL replica: read the applier worker error, decide between fixing data and skipping, and skip a GTID or non-GTID transaction correctly."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/replication-problems.html
  - https://dev.mysql.com/doc/refman/8.4/en/replication-administration-skip.html
  - https://dev.mysql.com/doc/refman/8.4/en/performance-schema-replication-applier-status-by-worker-table.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting replication errors

## Read the error
```sql
SHOW REPLICA STATUS\G     -- IO and SQL thread state and last errors
SELECT worker_id, last_error_number, last_error_message, last_error_timestamp,
       applying_transaction, last_applied_transaction
FROM performance_schema.replication_applier_status_by_worker WHERE last_error_number <> 0;
```
If the failing transaction errored in a worker thread, its GTID is in the `applying_transaction` column of `performance_schema.replication_applier_status_by_worker`; the worker row also holds the real error number and message.

## Common causes
- Duplicate-key or missing-row errors: the replica was written to directly, drifted, or a restore overlapped the binlog position.
- Missing table: DDL not applied on the replica (filters, manual change).
- Source no longer has the needed binlog: the replica is too far behind and must be rebuilt from a fresh snapshot (the docs' fallback is copying a new snapshot from the source).

## Decide: fix data or skip
Skipping is only safe when you know the transaction's effect is already present (or
irrelevant). Otherwise the replica drifts further and later errors follow. For 1032/1062,
inspect the row on both sides first. Inspect the failing transaction itself with `SHOW RELAYLOG EVENTS` on the replica or `SHOW BINLOG EVENTS` on the source, searching for the GTID.

Fix data approach (preferred for single rows): on the replica, make the row match the source, then `START REPLICA;`.

## Skipping a transaction with GTID
With GTIDs, commit an empty transaction with the failing GTID (not suitable on a channel using
`ASSIGN_GTIDS_TO_ANONYMOUS_TRANSACTIONS`):
```sql
STOP REPLICA;
SET GTID_NEXT = '<server_uuid>:<N>';   -- applying_transaction from the worker table
BEGIN; COMMIT;
SET GTID_NEXT = 'AUTOMATIC';
START REPLICA;
```
On a multi-source replica, name the channel in `START REPLICA`. The empty transaction enters this replica's binary log; `FLUSH LOGS` then `PURGE BINARY LOGS TO '<file>'` removes it while the GTID stays recorded.

Without GTIDs (`gtid_mode` OFF, OFF_PERMISSIVE or ON_PERMISSIVE), `SET GLOBAL sql_replica_skip_counter = N` skips events, not whole transactions; alternatively move the source log position with `CHANGE REPLICATION SOURCE TO`.

## Prevent
- Never modify data on the replica outside the replication threads (the manual says a proper snapshot and no outside writes mean this should not happen).
- Do not blanket-skip errors; it hides drift.

## Verify
Both replication threads run, the lag falls, no new worker errors, and the affected table matches the source.

## Checked
2026-11-01. Confirmed against the MySQL 8.4 manual pages Skipping Transactions (GTID empty-transaction method, ASSIGN_GTIDS_TO_ANONYMOUS_TRANSACTIONS limit, non-GTID skip counter, purging), Troubleshooting Replication and the replication_applier_status_by_worker table (columns). Removed: error-number table, 13114/1236 strings, replica_transaction_retries, sql_log_bin, super_read_only, gtid_purged/xtrabackup and pt-table-checksum advice, SHOW REPLICA STATUS field names (not on those pages).
Method: documentation only; no commands were run.
