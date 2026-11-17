---
id: computing-software.database-administration.sql-server.transaction-log-backups-and-the-log-chain
name: transaction-log-backups-and-the-log-chain
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sql-server-backup, log-chain, transaction-log-backup, tail-log-backup, copy-only, lsn, log-reuse-wait, msdb-backupset]
level: practitioner
status: docs-checked
description: "Schedule SQL Server log backups, keep the LSN log chain unbroken, find what broke it in msdb, and take tail-log and copy-only backups correctly."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/transaction-log-backups-sql-server
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/tail-log-backups-sql-server
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/copy-only-backups-sql-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transaction log backups and the log chain

**Goal:** in FULL / BULK_LOGGED recovery, an unbroken sequence of log backups so you
can restore to any moment, and a log file that does not grow forever.

## The chain
Each log backup covers LSNs `first_lsn` to `last_lsn` (the LSN of the next log record after the backup set), so the next one's `first_lsn`
should equal the previous `last_lsn`. The log chain is independent of data backups: a log backup taken after a later full
continues the same chain. What breaks it in practice:
- a log backup taken by someone else to a path you do not keep (third-party tool,
  a dev "just testing"), or deleted files.
After a break, plan a fresh full backup and confirm the new chain with the query below.

## Schedule
Microsoft says a log backup every 15 to 30 minutes might be enough, and more often if you must minimise work-loss exposure (the interval is your RPO).
At least one full backup must exist before any log backup.
```sql
BACKUP LOG appdb TO DISK = N'<BACKUP_PATH>\appdb_log_20261016_1015.trn'
  WITH CHECKSUM, COMPRESSION;
```
Frequent successful-backup messages fill the SQL Server error log; trace flag 3226 suppresses them if none of your scripts depend on them.

## Find gaps
```sql
SELECT database_name, type, backup_start_date, first_lsn, last_lsn, is_copy_only,
       mf.physical_device_name,
       LAG(last_lsn) OVER (PARTITION BY database_name ORDER BY backup_start_date) prev_last
FROM msdb.dbo.backupset bs JOIN msdb.dbo.backupmediafamily mf ON mf.media_set_id = bs.media_set_id
WHERE database_name = 'appdb' AND type = 'L'
ORDER BY backup_start_date DESC;      -- first_lsn <> prev_last means a gap
```
`physical_device_name` shows where a stray backup went.

## Copy-only
Ad hoc backups that must not disturb the sequence: `WITH COPY_ONLY`. A copy-only
full does not affect the differential base; a copy-only log does not affect the sequencing of regular log backups,
and the log is never truncated after a copy-only backup.

## Tail-log backup
Before restoring over a damaged or migrating database, back up the log not yet
backed up so nothing is lost:
```sql
BACKUP LOG appdb TO DISK = N'...\appdb_tail.trn' WITH NORECOVERY, NO_TRUNCATE, CHECKSUM;
```
`NORECOVERY` is needed for the tail-log backup of an online database; `NO_TRUNCATE` is for a database that is offline and fails to start
(effectively a copy-only log backup).

## Log not truncating
```sql
SELECT name, log_reuse_wait_desc FROM sys.databases;
```
`LOG_BACKUP` = a log backup is required before the log can be truncated; `ACTIVE_TRANSACTION` = open transaction;
`AVAILABILITY_REPLICA` = a secondary replica is still applying log records; `REPLICATION` =
transactions not yet delivered to the distribution database. Fix the cause; shrinking the log just makes it regrow.

## Verify
- [ ] Every FULL-recovery database has a log backup in the last interval (alert on it).
- [ ] No LSN gaps in the retention window; only one tool takes log backups.
- [ ] `log_reuse_wait_desc` is NOTHING or LOG_BACKUP between backups.

## Checked
2026-10-31. Confirmed against the Learn pages for transaction log backups, tail-log backups, copy-only backups, `backupset`, `sys.databases` and the transaction log architecture: log chain independent of data backups, full backup required first, `first_lsn`/`last_lsn` meaning, `is_copy_only`, copy-only behaviour, NORECOVERY/NO_TRUNCATE for tail-log backups, `log_reuse_wait_desc` values, trace flag 3226.
Changed: the 5-15 minute schedule (the page says 15 to 30 minutes might be enough). Removed as unconfirmed: error 4214, SIMPLE recovery and `NUL` as chain breakers, Ola Hallengren and dbatools commands, `DBCC OPENTRAN`, the VSS GUID remark.
Method: documentation only; no commands were run.
