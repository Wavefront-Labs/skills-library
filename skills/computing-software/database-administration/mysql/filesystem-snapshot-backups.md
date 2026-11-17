---
id: computing-software.database-administration.mysql.filesystem-snapshot-backups
name: filesystem-snapshot-backups
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, flush-tables-with-read-lock, lock-instance-for-backup, snapshot-backup, lvm-snapshot, physical-backup, mysql-backup]
level: practitioner
status: docs-checked
description: "Take consistent MySQL physical backups with LVM, ZFS or cloud disk snapshots using FLUSH TABLES WITH READ LOCK or LOCK INSTANCE FOR BACKUP, recording binlog position."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/backup-methods.html
  - https://dev.mysql.com/doc/refman/8.4/en/flush.html#flush-tables-with-read-lock
  - https://dev.mysql.com/doc/refman/8.4/en/lock-instance-for-backup.html
  - https://dev.mysql.com/doc/refman/8.4/en/performance-schema-log-status-table.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filesystem snapshot backups

A snapshot of the volume(s) holding datadir, redo, undo and binlogs gives a physical backup in seconds regardless of data size.

## If all files are on ONE volume with an atomic snapshot
Record the binlog position for replicas/PITR:
```sql
SELECT * FROM performance_schema.log_status\G   -- binlog file/pos, gtid_executed, relay log per channel, InnoDB LSN; needs BACKUP_ADMIN and SELECT
```
The table is populated with logging blocked only briefly; read it as close to the snapshot instant as possible (or take it under a lock, below).

## Multiple volumes or non-InnoDB tables: lock briefly
```sql
-- session kept open for the whole procedure
FLUSH TABLES WITH READ LOCK;       -- global read lock; MySQL's docs suggest it for ZFS/Veritas-style snapshots
SHOW BINARY LOG STATUS;            -- record file, position, Executed_Gtid_Set
-- shell: take the snapshot(s)
--   lvcreate -L 20G -s -n mysql_snap /dev/vg0/mysql
--   zfs snapshot tank/mysql@2026-10-18
UNLOCK TABLES;
```
- FTWRL is a global read lock, so keep it as short as possible; `lock_wait_timeout` bounds how long a `LOCK INSTANCE FOR BACKUP` waits to acquire its lock.
- `LOCK INSTANCE FOR BACKUP;` ... `UNLOCK INSTANCE;` (needs `BACKUP_ADMIN`) **permits DML** while blocking file create/rename/remove, `TRUNCATE TABLE`, `OPTIMIZE TABLE`, account management and `PURGE BINARY LOGS`. Because writes continue, read `performance_schema.log_status` for a consistent binlog, GTID and LSN set.

## Restore
1. Mount/clone the snapshot, copy files to the target datadir (`chown -R mysql:mysql`).
2. Start mysqld: crash recovery runs (check the error log).
3. For a replica: `CHANGE REPLICATION SOURCE TO ... SOURCE_AUTO_POSITION = 1` (GTID) or the recorded file/position; for PITR replay binlogs from the recorded position.

## Verify
- Snapshot restores start cleanly and `CHECK TABLE` on sample tables passes; schedule restore tests.
- Remove the LVM snapshot after copying it off.

## Gotchas
- A snapshot on the same disk array is not a backup; copy it elsewhere.
- Snapshots across several disks are only consistent if taken as one atomic set, or under a lock.

## Checked
2026-11-01. Confirmed against the MySQL 8.4 manual pages FLUSH Statement (global read lock, snapshot filesystems), LOCK INSTANCE FOR BACKUP (BACKUP_ADMIN, permits DML, blocked operations, lock_wait_timeout), The log_status Table (columns, privileges) and Replication problems (SHOW BINARY LOG STATUS). Removed: crash-safety and MyISAM claims, version note for SHOW MASTER STATUS, LVM degradation and processlist advice, container-size figures (not on those pages).
Method: documentation only; no commands were run.
