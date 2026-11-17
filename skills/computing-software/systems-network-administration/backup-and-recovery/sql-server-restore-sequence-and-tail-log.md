---
id: computing-software.systems-network-administration.backup-and-recovery.sql-server-restore-sequence-and-tail-log
name: sql-server-restore-sequence-and-tail-log
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [tail-log-backup, norecovery, point-in-time-recovery, sql-server-backup, transaction-log-backup, database-backup]
level: advanced
status: docs-checked
description: "Restore SQL Server to the point of failure or a point in time: tail-log backup, full/diff/log sequence WITH NORECOVERY, STOPAT, and finding the chain from msdb."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/tail-log-backups-sql-server
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/restore-a-sql-server-database-to-a-point-in-time-full-recovery-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server restore sequence and tail-log backups

Requires FULL (or BULK_LOGGED) recovery model with log backups.

## 1. Tail-log backup first (when the database still exists)
Captures log records not yet backed up, so you lose nothing:
```sql
BACKUP LOG sales TO DISK = N'\\backup\sql\sales_tail.trn' WITH NORECOVERY, NO_TRUNCATE, CHECKSUM;
```
`NORECOVERY` puts the DB in RESTORING (stops further changes). `NO_TRUNCATE` (or
`CONTINUE_AFTER_ERROR`) when data files are damaged but the log is readable.
Skipping this and restoring `WITH REPLACE` discards the tail.

## 2. Find the chain
```sql
SELECT bs.database_name, bs.type, bs.backup_start_date, bs.backup_finish_date,
       bs.first_lsn, bs.last_lsn, bs.database_backup_lsn, bmf.physical_device_name
FROM msdb.dbo.backupset bs JOIN msdb.dbo.backupmediafamily bmf ON bs.media_set_id = bmf.media_set_id
WHERE bs.database_name = 'sales' AND bs.backup_start_date > DATEADD(day,-3,GETDATE())
ORDER BY bs.backup_start_date;    -- type D=full, I=diff, L=log
```
Latest full → latest diff after it → all logs after the diff, unbroken by LSN.

## 3. Restore
```sql
RESTORE DATABASE sales FROM DISK = N'\\backup\sql\sales_full.bak' WITH NORECOVERY, REPLACE;
RESTORE DATABASE sales FROM DISK = N'\\backup\sql\sales_diff.bak' WITH NORECOVERY;
RESTORE LOG sales FROM DISK = N'\\backup\sql\sales_log_1000.trn' WITH NORECOVERY;
RESTORE LOG sales FROM DISK = N'\\backup\sql\sales_log_1015.trn' WITH NORECOVERY;
RESTORE LOG sales FROM DISK = N'\\backup\sql\sales_tail.trn'     WITH RECOVERY;
```
Point in time (e.g. before a bad DELETE at 10:07):
```sql
RESTORE LOG sales FROM DISK = N'\\backup\sql\sales_log_1015.trn' WITH STOPAT = '2026-10-18T10:06:30', RECOVERY;
```
Restore under a different database name when you only need to extract rows.

## Common failures
- Log restore refused because the log begins after the database's last restored LSN: a log backup is missing from the chain.
- Restore refused because the tail of the log has not been backed up: take the tail-log backup, or use REPLACE knowingly.
- Cannot open backup device: path or permissions of the SQL Server service account.
- Database stuck in Restoring: the final restore step needs `WITH RECOVERY`.

## Gotchas
- Copy-only backups don't break the chain; log backups taken by another tool may (check msdb
  for unexpected log backups).

## Checked
2026-11-01. Confirmed: tail-log backup with NORECOVERY/NO_TRUNCATE, NORECOVERY then STOPAT restore sequence, bulk-logged limits (Learn tail-log and point-in-time pages); msdb backupset and backupmediafamily tables (Learn system-table pages). Removed: dbatools commands, numeric error codes, AG advice, WITH MOVE wording.
Method: documentation only; no commands were run.

## Verify
Database ONLINE, `DBCC CHECKDB` clean, latest expected rows present (or bad change absent for
PITR), application validated.
