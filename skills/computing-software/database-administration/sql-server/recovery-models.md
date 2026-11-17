---
id: computing-software.database-administration.sql-server.recovery-models
name: recovery-models
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sql-server-backup, recovery-model, full-recovery, simple-recovery, bulk-logged, log-reuse-wait, transaction-log-growth]
level: practitioner
status: docs-checked
description: "Choose SQL Server recovery models (FULL, BULK_LOGGED, SIMPLE) from RPO needs, and fix runaway transaction log growth by reading log_reuse_wait_desc."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/recovery-models-sql-server
  - https://learn.microsoft.com/en-us/sql/relational-databases/logs/the-transaction-log-sql-server
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-databases-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovery models

**Goal:** the recovery model matches the RPO, and the transaction log never
fills the disk.

## The three models
| Model | Log backups | Point-in-time restore | Log truncation |
|---|---|---|---|
| FULL | required | yes | after a log backup (the log grows until one is taken) |
| BULK_LOGGED | required | no: recover to the end of any backup | after a log backup; log backups can be large because minimally logged operations are captured |
| SIMPLE | not supported | no (only to the end of a backup) | automatic; log space is reclaimed for you |
SQL Server Enterprise and Standard editions default to FULL, Express to SIMPLE; you can switch at any time.
SIMPLE cannot be used with log shipping, Always On availability groups, database mirroring, media recovery without data loss or point-in-time restore.

```sql
SELECT name, recovery_model_desc, log_reuse_wait_desc FROM sys.databases;
ALTER DATABASE appdb SET RECOVERY FULL;
BACKUP DATABASE appdb TO DISK = N'...';    -- a log chain starts with a full backup; the first log backup needs one
```

## The classic failure: log grows forever
FULL (or BULK_LOGGED) recovery without log backups: the log is not truncated and grows until
the disk is full (error 9002). Diagnose:
```sql
SELECT name, log_reuse_wait_desc FROM sys.databases WHERE name = 'appdb';
DBCC SQLPERF(LOGSPACE);
```
| log_reuse_wait_desc | Meaning / fix |
|---|---|
| LOG_BACKUP | Take log backups (Microsoft: every 15-30 minutes might be enough; more often if your work-loss tolerance requires) |
| ACTIVE_TRANSACTION | A long open transaction holds the log: find and end it |
| AVAILABILITY_REPLICA | An AG secondary is still applying this database's log |
| REPLICATION | Transactional replication has not delivered log records yet |
| ACTIVE_BACKUP_OR_RESTORE | A backup or restore is running |
Other documented values: NOTHING, CHECKPOINT, DATABASE_MIRRORING, DATABASE_SNAPSHOT_CREATION, LOG_SCAN, OLDEST_PAGE, XTP_CHECKPOINT, SLOG_SCAN (ADR).
After fixing the cause, shrink only if the log is far beyond its normal working
size: `DBCC SHRINKFILE (appdb_log, 8192);` (MB). Never shrink as routine.

## BULK_LOGGED use
BULK_LOGGED reduces log space with minimal logging of bulk operations. Log backups are larger because the
minimally logged operations are captured in them, and point-in-time recovery is not supported.

## Gotchas
- A new log chain starts after switching from SIMPLE to FULL or BULK_LOGGED; the chain starts with a full backup.
- Size and autogrowth of the log: see the file-autogrowth-and-vlf-counts skill.

## Verify
`log_reuse_wait_desc` normally NOTHING or LOG_BACKUP between backups;
the msdb backup history (`msdb.dbo.backupset`) shows log backups at the expected interval.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for Recovery Models, sys.databases and the Transaction Log Architecture guide.
Confirmed: model behaviours and the edition defaults, SIMPLE exclusions, error 9002, log chain start rule, 15-30 minute log backup guidance, `log_reuse_wait_desc` values and meanings. Removed unconfirmed claims: model-database inheritance, "pseudo-simple", differential backup requirement after a switch, DBCC OPENTRAN and the 5-15 minute interval.
Method: documentation only; no commands were run.
