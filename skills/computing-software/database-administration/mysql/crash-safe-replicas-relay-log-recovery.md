---
id: computing-software.database-administration.mysql.crash-safe-replicas-relay-log-recovery
name: crash-safe-replicas-relay-log-recovery
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, gtid, binlog, relay-log-recovery, crash-safe-replication, sync-relay-log, replica-configuration]
level: practitioner
status: docs-checked
description: "Configure MySQL replicas to survive crashes without duplicate or lost transactions: relay_log_recovery, sync_relay_log, GTID auto-positioning and GTID_ONLY."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/replication-solutions-unexpected-replica-halt.html
  - https://dev.mysql.com/doc/refman/8.4/en/replication-options-replica.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crash-safe replicas (relay_log_recovery)

## The problem
After an unexpected halt, the applier (SQL thread) must recover which transactions
were already executed. Its position lives in the applier metadata repository, an
InnoDB table `mysql.slave_relay_log_info` updated together with each DML
transaction and atomic DDL, so it matches what was applied. Non-atomic DDL and
engines without atomic DDL can leave it missing updates, and restoring is manual.

## Settings (MySQL 8.4 manual's most resilient combination)
```ini
[mysqld]
gtid_mode = ON
sync_relay_log = 1                 # slowest, safest: relay log synced after each received transaction
innodb_flush_log_at_trx_commit = 1 # the default
relay_log_recovery = ON            # default OFF, read-only at runtime
# relay_log_info_repository = TABLE is the default; the variable is deprecated, so omit it
```
Per channel (set it on each channel of a multi-source replica):
```sql
CHANGE REPLICATION SOURCE TO SOURCE_AUTO_POSITION = 1, GTID_ONLY = 1;
```
- `SOURCE_AUTO_POSITION = 1`: the replica compares GTIDs with the source and
  fetches exactly the missing transactions. Not used with file-position replication.
- `GTID_ONLY = 1`: recovery uses only GTIDs and file names/positions are no longer
  persisted; GTID auto-skip skips transactions already supplied.
- `relay_log_recovery`: starts a new relay log file and fetches from the applier
  position, ignoring existing relay log files. Use it after an unexpected halt; it
  is required for a crash-safe replica. Disabling `relay_log_purge` with it risks consistency.

Other storage-engine flush settings also matter; check your engines' crash-safe advice.

## Multithreaded replicas
With `replica_parallel_workers` above 0, `relay_log_recovery` fills gaps the same way
`START REPLICA UNTIL SQL_AFTER_MTS_GAPS` would. With GTIDs and
`SOURCE_AUTO_POSITION` on, old relay logs are not needed. `sync_relay_log = 1`
matters most here, since recovery fails if gaps cannot be filled from the relay log.

## Gotchas
- `relay_log_info_repository = FILE` gives no guarantee of recovery.
- With `sync_relay_log` greater than 1 or 0, committed transactions may be unsynced
  and recovery can fail by re-fetching them.

## Verify
In a test environment, `kill -9` mysqld on a busy replica, restart, and confirm
replication resumes with no errors and replicas and source still match (row counts or a checksum tool).

## Checked
2026-11-01. Confirmed against MySQL 8.4 "Handling an Unexpected Halt of a Replica" and the replica options page (relay_log_recovery default, dynamic scope, behaviour, relay_log_purge note). Removed: sync_binlog, log_replica_updates, delayed-replica, the relaxed-durability section, the version note on replica_preserve_commit_order, and named external checksum tool.
Method: documentation only; no commands were run.
