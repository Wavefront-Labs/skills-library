---
id: computing-software.database-administration.sql-server.backup-checksum-and-restore-verifyonly
name: backup-checksum-and-restore-verifyonly
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sql-server-backup, restore-verifyonly, backup-checksum, page-verify, backup-validation, test-dbalastbackup, restore-testing]
level: practitioner
status: docs-checked
description: "Use BACKUP WITH CHECKSUM, RESTORE VERIFYONLY and real test restores with CHECKDB to prove SQL Server backups are usable, and know what each proves."
sources:
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-verifyonly-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/enable-or-disable-backup-checksums-during-backup-or-restore-sql-server
  - https://dbatools.io/Test-DbaLastBackup.html
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/backup-checksum-default
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup CHECKSUM and RESTORE VERIFYONLY

**Goal:** know your backups restore, ranked by how much each check actually proves.

## Level 1: PAGE_VERIFY CHECKSUM on the database
```sql
SELECT name, page_verify_option_desc FROM sys.databases;   -- want CHECKSUM
ALTER DATABASE olddb SET PAGE_VERIFY CHECKSUM;            -- pages get checksums as they are rewritten
```
Older databases may still show `TORN_PAGE_DETECTION` or `NONE`.

## Level 2: BACKUP ... WITH CHECKSUM
Verifies each page's checksum while reading (fails the backup on a bad page, error 3043)
and writes a checksum over the whole backup stream.
```sql
BACKUP DATABASE appdb TO DISK = N'...' WITH CHECKSUM, COMPRESSION;
EXEC sp_configure 'backup checksum default', 1; RECONFIGURE;   -- instance default (not available in 2012 and earlier); NO_CHECKSUM overrides it
```
`CONTINUE_AFTER_ERROR` exists for salvaging a backup from a damaged database only.

## Level 3: RESTORE VERIFYONLY
Checks the backup set is complete and readable, re-validates checksums if they
exist, and checks header fields. Does **not** verify the data structure of the database.
```sql
RESTORE VERIFYONLY FROM DISK = N'...\appdb_full.bak' WITH CHECKSUM;
-- "The backup set on file 1 is valid."
```
Without a backup checksum, VERIFYONLY mostly confirms the file is readable. Run it on a
different server than the one that wrote it, against the copy in the backup store.

## Level 4: restore + DBCC CHECKDB (the only real proof)
```powershell
Test-DbaLastBackup -SqlInstance prod01 -Destination test01 -Database appdb `
  -MaxSize 500000 | Select Database, RestoreResult, DbccResult, BackupDates
```
dbatools finds the last full backup of each database, restores it to the destination under a new name, runs CHECKDB,
drops the copy, and reports (`-MaxSize` is in MB; `-VerifyOnly`, `-NoCheck` and `-NoDrop` change the steps). Schedule weekly for every database (rotate big ones), store
results in a table, and alert on failure. This also offloads CHECKDB from production
for databases where that is acceptable.

## Gotchas
- Checksums catch corruption that happened **before** backup (in the source pages)
  and in the backup file. They do not catch logically wrong data.
- A backup that VERIFYONLYs fine can still fail to restore for missing TDE certificates,
  missing credentials for URL, or not enough disk space at the destination.
- Encrypted backups (`WITH ENCRYPTION`) need the certificate on the verifying server.
- `msdb.dbo.backupset.has_backup_checksums` shows which backups had checksums.

## Verify
- [ ] All databases on `PAGE_VERIFY CHECKSUM`; `backup checksum default = 1`.
- [ ] Automated restore test + CHECKDB per database within the last cycle, results logged.
- [ ] Restore time measured and within RTO.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: BACKUP and RESTORE VERIFYONLY behaviour per the SQL Server 2025 documentation (page checksum failure stops the backup with error 3043, backup checksum default option with range 0/1 and NO_CHECKSUM override, option absent in 2012 and earlier, has_backup_checksums in msdb.dbo.backupset, VERIFYONLY does not verify database structure), dbatools Test-DbaLastBackup (restores last full backup under a new name, runs DBCC CHECKDB, drops, -MaxSize in MB, RestoreResult/DbccResult/BackupDates output). Removed as unconfirmed: the 2014 introduction claim and the SQL 2000 remark.
Method: documentation only; no commands were run.
