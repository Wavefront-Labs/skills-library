---
id: computing-software.systems-network-administration.backup-and-recovery.sql-server-full-differential-log-backups
name: sql-server-full-differential-log-backups
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [sql-server-backup, transaction-log-backup, recovery-model, differential-backup, restore-sequence, database-backup, stopat]
level: advanced
status: docs-checked
description: "Back up SQL Server with full, differential and log backups: recovery models, CHECKSUM, COMPRESSION and COPY_ONLY, STOPAT restore sequences and log chain hygiene."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/back-up-and-restore-of-sql-server-databases
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/backup-transact-sql
  - https://ola.hallengren.com/sql-server-backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server full, differential and log backups

**Goal:** restore any database to any point within retention, with RPO set by log backup frequency.

## Recovery models
- **FULL**: log records kept until backed up; point-in-time restore possible. Required for log backups.
- **SIMPLE**: log truncates automatically; restore only to full/differential points.
- **BULK_LOGGED**: temporary for bulk loads; point-in-time not possible within log backups containing bulk operations.
```sql
ALTER DATABASE Sales SET RECOVERY FULL;
```

## Backups
```sql
BACKUP DATABASE Sales TO DISK = N'\\bkp\sql\Sales_FULL_20261015.bak' WITH COMPRESSION, CHECKSUM, STATS = 10;
BACKUP DATABASE Sales TO DISK = N'\\bkp\sql\Sales_DIFF_20261016.bak' WITH DIFFERENTIAL, COMPRESSION, CHECKSUM;
BACKUP LOG Sales TO DISK = N'\\bkp\sql\Sales_LOG_20261016_1015.trn' WITH COMPRESSION, CHECKSUM;
BACKUP DATABASE Sales TO DISK = N'...adhoc.bak' WITH COPY_ONLY;   -- ad hoc, does not reset the differential base
```
Typical schedule: periodic full, more frequent differential, and log backups at an interval set by your RPO. Ola Hallengren's `DatabaseBackup` procedure handles this with cleanup and checks.

## Restore sequence (point in time)
```sql
RESTORE DATABASE Sales FROM DISK = N'...FULL.bak' WITH NORECOVERY, REPLACE;
RESTORE DATABASE Sales FROM DISK = N'...DIFF.bak' WITH NORECOVERY;
RESTORE LOG Sales FROM DISK = N'...LOG_1000.trn' WITH NORECOVERY;
RESTORE LOG Sales FROM DISK = N'...LOG_1015.trn' WITH STOPAT = '2026-10-16T10:12:00', RECOVERY;
```
Take a **tail-log backup** (`BACKUP LOG ... WITH NORECOVERY`) first if the database is still accessible, to avoid losing the last transactions.

## Hygiene
- One owner of log backups per database; another product's log backup breaks the chain for the first.
- `RESTORE VERIFYONLY` is not a substitute for real test restores; run them plus `DBCC CHECKDB` on the restored copy.
- Monitor `msdb.dbo.backupset` for databases with no recent log backup (log growth) or full backup.

## Checked
2026-11-01. Confirmed: BULK_LOGGED point-in-time limit, STOPAT/NORECOVERY restore sequence, COPY_ONLY not serving as a differential base and not truncating the log, tail-log backup with NORECOVERY on an online database, backupset history table (Learn BACKUP, tail-log and point-in-time restore pages). Removed: AG/log shipping claim, fixed schedule intervals, VERIFYONLY detail.
Method: documentation only; no commands were run.

## Verify
Monthly: restore a production database to a test instance at a chosen time with STOPAT, run DBCC CHECKDB, and record duration against RTO.
