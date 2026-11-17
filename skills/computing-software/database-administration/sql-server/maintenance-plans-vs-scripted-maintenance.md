---
id: computing-software.database-administration.sql-server.maintenance-plans-vs-scripted-maintenance
name: maintenance-plans-vs-scripted-maintenance
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, maintenance-plans, ola-hallengren, maintenance-solution, sql-server-agent, index-maintenance, backup-jobs]
level: practitioner
status: docs-checked
description: "Decide between SQL Server maintenance plans and scripted maintenance (Ola Hallengren) and use the Maintenance Solution procedures for backup, CHECKDB and index jobs."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/maintenance-plans/maintenance-plans
  - https://ola.hallengren.com/
  - https://github.com/olahallengren/sql-server-maintenance-solution
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Maintenance plans vs scripted maintenance

## Maintenance plans
Built in SSMS and run by SQL Server Agent jobs; see the Microsoft maintenance plans page. Fine for a
single small server managed by a non-DBA. At scale they are hard to version-control or deploy to many servers,
so prefer scripted maintenance. Do not schedule a shrink-database task after an index rebuild.

## Scripted: Ola Hallengren Maintenance Solution
Install `MaintenanceSolution.sql` from the GitHub repository (it creates the `CommandLog` table and the
`DatabaseBackup`, `DatabaseIntegrityCheck` and `IndexOptimize` procedures).
```sql
EXEC dbo.DatabaseBackup @Databases = 'USER_DATABASES', @Directory = '<BACKUP_SHARE>',
  @BackupType = 'FULL', @Verify = 'Y', @Compress = 'Y', @CheckSum = 'Y', @CleanupTime = 168;
EXEC dbo.DatabaseBackup @Databases = 'USER_DATABASES', @Directory = '<BACKUP_SHARE>', @BackupType = 'LOG', @CleanupTime = 72;
EXEC dbo.DatabaseIntegrityCheck @Databases = 'USER_DATABASES', @CheckCommands = 'CHECKDB', @PhysicalOnly = 'N';
EXEC dbo.IndexOptimize @Databases = 'USER_DATABASES',
  @FragmentationLow = NULL,
  @FragmentationMedium = 'INDEX_REORGANIZE,INDEX_REBUILD_ONLINE,INDEX_REBUILD_OFFLINE',
  @FragmentationHigh = 'INDEX_REBUILD_ONLINE,INDEX_REBUILD_OFFLINE',
  @FragmentationLevel1 = 50, @FragmentationLevel2 = 80, @UpdateStatistics = 'ALL', @OnlyModifiedStatistics = 'Y';
```
`DatabaseBackup` also takes `@AvailabilityGroups` for availability group databases. The `CommandLog` table
logs the commands the procedures run.

## Schedule
Set log, full and differential backup frequency from your RPO/RTO, run `CHECKDB` regularly, and run `IndexOptimize`
on a schedule that fits your maintenance window. Also clean up old history.

## Migrating off plans
Script the plan's jobs, disable them, deploy Ola jobs with notifications to an operator, run both
backup sets in parallel for a cycle, then delete the plans.

## Verify
Every job has a notify-on-failure operator, and the jobs ran without errors for the last week.

## Checked
2026-11-01. Confirmed against ola.hallengren.com and the GitHub repository: the DatabaseBackup, DatabaseIntegrityCheck
and IndexOptimize procedures and the parameters used (@Databases, @BackupType, @Verify, @Compress, @CheckSum,
@CleanupTime, @CheckCommands, @PhysicalOnly, @Fragmentation* options, @FragmentationLevel1/2, @UpdateStatistics,
@OnlyModifiedStatistics, @AvailabilityGroups), MaintenanceSolution.sql and CommandLog.sql. Removed as unconfirmed:
maintenance-plan task behaviour claims, dbatools install command, @LogToTable, @MinNumberOfPages, @TimeLimit, the
CommandLog query, the schedule table, sp_delete_backuphistory and SSD advice.
Method: documentation only; no commands were run.
