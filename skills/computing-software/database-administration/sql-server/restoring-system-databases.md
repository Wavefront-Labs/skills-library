---
id: computing-software.database-administration.sql-server.restoring-system-databases
name: restoring-system-databases
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, sql-server-backup, restore-master, msdb, model, single-user-mode, rebuild-system-databases]
level: advanced
status: docs-checked
description: "Back up and restore SQL Server master, msdb and model: single-user startup for master, rebuilding system databases, and what each restore brings back."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/restore-the-master-database-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/back-up-and-restore-of-system-databases-sql-server
  - https://learn.microsoft.com/en-us/sql/relational-databases/databases/rebuild-system-databases
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restoring system databases

## What to back up
Back up master, model and msdb with full backups (the recovery procedure restores the most recent full backups of all three). tempdb cannot be backed up: it is re-created every time the instance starts. msdb holds Agent jobs, alerts, operators, backup history and Database Mail settings.

## Restoring master
1. Start the instance in single-user mode with the `-mSQLCMD` startup parameter, which ensures only sqlcmd can connect (see the restore-master page for the exact startup steps).
2. Restore:
   ```bat
   sqlcmd -S . -E -Q "RESTORE DATABASE master FROM DISK = N'<BACKUP_DIR>\master.bak' WITH REPLACE"
   ```
   The instance **shuts down automatically** and terminates the sqlcmd process after a successful master restore.
3. Remove the single-user startup parameter, then start normally. Objects created after that master backup are not in it.

## When master is too damaged to start
Rebuild system databases from setup media, then restore your backups:
```bat
setup.exe /QUIET /ACTION=REBUILDDATABASE /INSTANCENAME=MSSQLSERVER ^
  /SQLSYSADMINACCOUNTS="CORP\dba-team" /SAPWD="..." /SQLCOLLATION=SQL_Latin1_General_CP1_CI_AS
```
Record collation and patch level beforehand. A recovery instance should be the same version, edition and patch level as the original (see the back up and restore of system databases page); check with `SELECT @@VERSION`.

## Restoring msdb / model
```sql
RESTORE DATABASE msdb  FROM DISK = N'<BACKUP_DIR>\msdb.bak'  WITH REPLACE;
RESTORE DATABASE model FROM DISK = N'<BACKUP_DIR>\model.bak' WITH REPLACE;
```
The same version and patch level guidance applies.

## Gotchas
- Keep copies of system DB backups **off** the server; a lost host with backups on its own
  disk cannot be rebuilt.
- Document service accounts, startup parameters, trace flags and paths; rebuild needs them.

## Verify
After restore and restart: `SELECT name, create_date FROM sys.databases;` lists expected
databases, logins exist (`sys.server_principals`), Agent jobs run.

## Checked

2026-10-28. Confirmed against Microsoft Learn (restore the master database, back up and restore of system databases, rebuild system databases): restore master in single-user mode with -mSQLCMD so only sqlcmd connects, RESTORE DATABASE master ... WITH REPLACE in sqlcmd, instance shuts down after the restore and the single-user parameter must be removed before restart, restore the most recent full backups of master, model and msdb, tempdb cannot be backed up, recovery instance should match version, edition and patch level, REBUILDDATABASE setup action. Removed unconfirmed: net start /m syntax, the per-database contents table, master SIMPLE recovery claim, re-attach advice, Agent-must-be-stopped note, AG and contained-AG remark, file-move procedure.

Method: documentation only; no commands were run.
