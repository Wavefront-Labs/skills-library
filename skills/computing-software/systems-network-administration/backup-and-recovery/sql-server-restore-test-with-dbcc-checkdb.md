---
id: computing-software.systems-network-administration.backup-and-recovery.sql-server-restore-test-with-dbcc-checkdb
name: sql-server-restore-test-with-dbcc-checkdb
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [dbcc-checkdb-after-restore, restore-verifyonly, restore-test, database-backup, sql-server-backup, dbatools]
level: practitioner
status: docs-checked
description: "Prove SQL Server backups restore: RESTORE VERIFYONLY limits, scripted restore to a test instance, DBCC CHECKDB, automation with dbatools Test-DbaLastBackup, and timing."
sources:
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-verifyonly-transact-sql
  - https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkdb-transact-sql
  - https://docs.dbatools.io/Test-DbaLastBackup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server restore testing with DBCC CHECKDB

## VERIFYONLY isn't enough
```sql
RESTORE VERIFYONLY FROM DISK = N'\\backup\sql\sales_full.bak' WITH CHECKSUM;
```
Checks the backup set is complete and all volumes are readable, some page header fields, the
checksum (if present on the media) and free space on the destination. It does **not** verify
the structure of the data in the backup, so it cannot show the database is consistent. Only an
actual restore + CHECKDB proves that.

## Manual test restore
```sql
RESTORE DATABASE sales_restoretest FROM DISK = N'\\backup\sql\sales_full.bak'
  WITH MOVE 'sales' TO N'<DATA_DIR>\sales_rt.mdf', MOVE 'sales_log' TO N'<LOG_DIR>\sales_rt.ldf',
       NORECOVERY, STATS = 10;
RESTORE DATABASE sales_restoretest FROM DISK = N'\\backup\sql\sales_diff.bak' WITH NORECOVERY;
RESTORE LOG sales_restoretest FROM DISK = N'\\backup\sql\sales_log_0100.trn' WITH NORECOVERY;
RESTORE DATABASE sales_restoretest WITH RECOVERY;
DBCC CHECKDB (sales_restoretest) WITH NO_INFOMSGS, ALL_ERRORMSGS;
DROP DATABASE sales_restoretest;
```
Record elapsed restore time: that's your achieved RTO for this database size.

## Automate with dbatools
```powershell
Test-DbaLastBackup -SqlInstance sqlprod01 -Destination sqltest01 -Database sales, hr `
  -DataDirectory '<DATA_DIR>' -LogDirectory '<LOG_DIR>' |
  Select Database, RestoreResult, DbccResult, RestoreElapsed, DbccElapsed, BackupDates
```
It queries backup history for the last backups, restores them under a new name (default prefix
`dbatools-testrestore-`) on the destination, renames the internal files, runs CHECKDB and drops
the test database. `-IgnoreLogBackup` and `-IgnoreDiffBackup` skip those parts of the chain;
`-VerifyOnly` only runs RESTORE VERIFYONLY; `-Checksum` with it fails backups lacking checksums.
Schedule it (rotate through databases) and alert on failure.

## Considerations
- Large databases: Microsoft recommends `WITH PHYSICAL_ONLY` for frequent use on production
  systems (much shorter run-time) with a full DBCC CHECKDB run periodically. PHYSICAL_ONLY
  skips column-integrity and FILESTREAM checks.

## Verify
Regular report: each database restored and CHECKDB clean within the last N days, restore
times trending, failures ticketed.

## Checked
2026-11-08. Confirmed against the three cited pages (read in full): RESTORE VERIFYONLY checks, DBCC CHECKDB options (PHYSICAL_ONLY, NO_INFOMSGS, ALL_ERRORMSGS), Test-DbaLastBackup behaviour, parameters and output columns. Removed unsupported TDE-certificate and Developer-edition licensing claims; corrected the output column to BackupDates and the VERIFYONLY description. The restore T-SQL sequence is standard syntax not exercised here.
Method: documentation only; no commands were run.
