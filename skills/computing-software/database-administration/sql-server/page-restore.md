---
id: computing-software.database-administration.sql-server.page-restore
name: page-restore
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, dbcc-checkdb, page-restore, restore-page, corruption-repair, error-824, online-page-restore, tail-log-backup]
level: advanced
status: docs-checked
description: "Repair a few corrupt SQL Server pages without data loss by restoring just those pages from backups plus log backups, online in Enterprise edition."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/restore-pages-sql-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Page restore

**Goal:** fix a handful of damaged pages (error 824, CHECKDB errors) from good
backups with zero data loss, instead of restoring the whole multi-TB database.

## Prerequisites
- Full recovery model (best practice; bulk-logged has extra conditions and page restore generally does not work with it), and log backups since the full backup.
- The damaged pages are not the file boot page, the database boot page (1:9) or
  allocation pages (GAM, SGAM, PFS).
- Only read/write filegroups are supported. Enterprise edition supports online page restore.

## Identify pages
```sql
SELECT database_id, file_id, page_id, event_type, error_count, last_update_date FROM msdb.dbo.suspect_pages;
DBCC CHECKDB (appdb) WITH NO_INFOMSGS, ALL_ERRORMSGS;   -- lists (file:page) in errors
```

## Procedure
```sql
-- 1. Restore the pages from the latest full (or differential chain)
RESTORE DATABASE appdb PAGE = '1:57, 1:202, 1:916'
  FROM DISK = N'\\backup\appdb_full.bak' WITH NORECOVERY;
-- 2. Apply all subsequent log backups
RESTORE LOG appdb FROM DISK = N'\\backup\appdb_log_0100.trn' WITH NORECOVERY;
RESTORE LOG appdb FROM DISK = N'\\backup\appdb_log_0115.trn' WITH NORECOVERY;
-- 3. Take a NEW log backup (tail) to capture changes up to now
BACKUP LOG appdb TO DISK = N'\\backup\appdb_tail.trn';
-- 4. Restore that log backup and recover
RESTORE LOG appdb FROM DISK = N'\\backup\appdb_tail.trn' WITH RECOVERY;
```

## Then
- Run `DBCC CHECKDB` again to confirm clean.
- Find the root cause: Windows event log for I/O errors, storage firmware,
  `suspect_pages` entries on other databases. Corruption usually comes back if the storage is faulty.

## Gotchas

- Pages restored from the full backup must be brought current by log backups:
  without logs you cannot page-restore.

## Verify
`DBCC CHECKDB` reports 0 allocation and 0 consistency errors; queries touching
the affected objects succeed.

## Checked
2026-10-28. Confirmed against the Restore Pages, tail-log backup and suspect_pages pages: page restore applies to full or bulk-logged recovery (bulk-logged has extra conditions and generally does not work), read/write filegroups only, Enterprise edition supports online page restore, file boot page and database boot page 1:9 and GAM/SGAM/PFS allocation pages cannot be page-restored, suspect_pages table in msdb, the RESTORE PAGE then RESTORE LOG then tail-log backup sequence.
Removed unconfirmed claims: the 1000-page limit, the 1000-row limit of suspect_pages, Restore-DbaDbPage, ring-buffer advice, the automatic page repair gotcha for availability groups, "Standard: offline".
Method: documentation only; no commands were run.
