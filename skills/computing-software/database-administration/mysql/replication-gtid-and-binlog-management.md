---
id: computing-software.database-administration.mysql.replication-gtid-and-binlog-management
name: replication-gtid-and-binlog-management
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, replication, gtid, binlog, binary-log, replica, show-replica-status, errant-transaction, row-based-replication, semi-sync, pt-table-checksum]
level: advanced
status: docs-checked
description: "Set up GTID-based MySQL replication, read binlogs for root-cause and point-in-time recovery, and fix a broken replica without a full re-clone."
sources:
  - https://dev.mysql.com/doc/refman/8.0/en/replication-gtids.html
  - https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MySQL replication: GTIDs, binlogs, and fixing a broken replica

**Goal:** run GTID-based replication that survives failover without manual binlog
coordinate hunting, and know how to read the binlog when you need to answer "what
actually happened" or recover to a point in time.

## 1. GTID basics
Enable with `gtid_mode = ON`, `enforce_gtid_consistency = ON` (both sides),
`log_bin = ON`, `log_slave_updates = ON` on replicas that chain. Each transaction
gets a global `source_uuid:transaction_id`. A new replica just needs
`CHANGE REPLICATION SOURCE TO SOURCE_AUTO_POSITION = 1` — no more copying
`SHOW MASTER STATUS` file/position by hand, which was the classic source of
silent data loss when someone fat-fingered the position.

## 2. The "errant transaction" problem
GTIDs solve coordinate-hunting but introduce their own failure mode: an **errant
transaction** — one written directly on a replica (someone ran a stray `INSERT` on
what they thought was read-only) that never happened on the source. When that
replica is later promoted or a new replica tries to pull from it, replication halts
because the GTID set diverges and MySQL refuses to silently skip or duplicate.
Diagnose with:
```sql
SELECT GTID_SUBSET(@@GLOBAL.GTID_EXECUTED, '<source_gtid_set>');
-- or compare gtid_executed between source and replica directly
```
Fix: either inject an empty transaction with the same GTID on the source
(`SET GTID_NEXT='uuid:n'; BEGIN; COMMIT;`) so it's "satisfied" everywhere, or exclude
it and re-clone. Prevention: make replicas `read_only=ON` and `super_read_only=ON`
so even an admin's direct write is blocked unless explicitly overridden.

## 3. Reading the binlog
```bash
mysqlbinlog --base64-output=decode-rows -v binlog.000123 | less
# row events need the server's row-image setting to show old/new values:
# binlog_row_image = FULL
```
Row-based replication (the default, safest) logs before/after row images, not SQL
text — useful for "who deleted this row and when" forensics, but the output is
dense. Statement-based logging is more readable but unsafe for non-deterministic
statements (`NOW()`, `UUID()`, `LIMIT` without `ORDER BY`) — mixed mode
(`binlog_format=MIXED`) falls back to row format automatically for those.

## 4. Point-in-time recovery using binlogs
After restoring a full backup to its exact end position, replay subsequent binlog
events up to (but not including) a bad statement:
```bash
mysqlbinlog --start-position=<pos> --stop-datetime="2026-10-15 09:14:00" \
  binlog.000123 | mysql -u root -p
```
Requires binlogs retained far enough back (`binlog_expire_logs_seconds`) and the
exact position/time of the mistake — cross-reference with `mysqlbinlog` output
around the suspected time, or the audit log if enabled.

## 5. Common replica breakage and fixes
- **1062 duplicate key on replica apply**: usually a prior errant write or an
  incomplete previous recovery. Position-based skipping with `sql_replica_skip_counter`
  is deprecated and unreliable under GTID replication; diagnose the actual divergence
  rather than skip blindly — skipping can leave silent data drift.
- **Replica lag spike**: single-threaded apply thread is the classic cause pre-5.7
  parallel replication; check `replica_parallel_workers` /
  `replica_parallel_type=LOGICAL_CLOCK` are set, and that the lag isn't from a
  single huge transaction (bulk DELETE) that can't be parallelized.
- **Data drift without errors**: replication can apply cleanly while data silently
  diverges (e.g. non-deterministic trigger/UUID in statement mode). Run
  `pt-table-checksum` periodically and `pt-table-sync` to repair.

## Verify
- [ ] Both source and all replicas run with `gtid_mode=ON` and `enforce_gtid_consistency=ON`.
- [ ] Replicas are `read_only=ON`/`super_read_only=ON` to prevent errant transactions.
- [ ] `SHOW REPLICA STATUS` shows `Replica_IO_Running` and `Replica_SQL_Running` both `Yes` with acceptable `Seconds_Behind_Source`.
- [ ] Binlog retention covers your recovery window (`binlog_expire_logs_seconds`).
- [ ] A recent `pt-table-checksum` run shows no unexplained diffs.

## Checked

2026-10-31: confirmed mysqldump --set-gtid-purged semantics (SET @@GLOBAL.gtid_purged added to the dump, sql_log_bin=0 while reloading) on the mysqldump reference; mysqlbinlog options --base64-output=decode-rows (with --verbose for row events), --start-position, --stop-datetime, --include-gtids, --exclude-gtids, --skip-gtids; binlog_row_image default full and binlog_expire_logs_seconds default 2592000 on the 8.4 binary log options page; and single-invocation replay of multiple binlog files on the point-in-time recovery page. Reworded the skip-counter bullet to the documented deprecation instead of an unverified GTID behavior claim.
Method: documentation only; no commands were run.
