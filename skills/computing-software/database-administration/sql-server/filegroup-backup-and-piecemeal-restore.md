---
id: computing-software.database-administration.sql-server.filegroup-backup-and-piecemeal-restore
name: filegroup-backup-and-piecemeal-restore
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, piecemeal-restore, filegroup-backup, partial-backup, read-only-filegroup, vldb, online-restore]
level: advanced
status: docs-checked
description: "Back up large SQL Server databases by filegroup, make archive filegroups read-only, and bring the database online in stages with a piecemeal restore."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/piecemeal-restores-sql-server
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/full-file-backups-sql-server
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/partial-backups-sql-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filegroup backups and piecemeal restore

For multi-terabyte databases: restore the PRIMARY and current-data filegroups first, let users
in, then restore history filegroups later (all editions support offline piecemeal restore;
Enterprise can also do it online).

## Design
- PRIMARY holds only system objects; current data in `FG_Current`; history partitions in
  `FG_2023`, `FG_2024` marked read-only once closed.
  ```sql
  ALTER DATABASE bigdb MODIFY FILEGROUP FG_2023 READ_ONLY;
  BACKUP DATABASE bigdb FILEGROUP = 'FG_2023' TO DISK = '<BACKUP_DIR>/bigdb_FG_2023.bak' WITH CHECKSUM, COMPRESSION;
  ```
  Log backups are not applied to a filegroup that has been read-only since before its backup.
- Partial backups back up the primary and all read-write filegroups (read-only ones optionally):
  ```sql
  BACKUP DATABASE bigdb READ_WRITE_FILEGROUPS TO DISK = '<BACKUP_DIR>/bigdb_rw.bak' WITH CHECKSUM, COMPRESSION;
  BACKUP DATABASE bigdb READ_WRITE_FILEGROUPS TO DISK = '<BACKUP_DIR>/bigdb_rw_diff.bak' WITH DIFFERENTIAL;
  ```
- Log backups as usual (FULL recovery): they are what make filegroups consistent with each other.

## Piecemeal restore (full recovery model)
```sql
-- stage 1: primary + current data
RESTORE DATABASE bigdb FILEGROUP = 'PRIMARY', FILEGROUP = 'FG_Current'
  FROM DISK = '<BACKUP_DIR>/bigdb_rw.bak' WITH PARTIAL, NORECOVERY;
RESTORE LOG bigdb FROM DISK = '<BACKUP_DIR>/bigdb_log1.trn' WITH NORECOVERY;
BACKUP LOG bigdb TO DISK = '<BACKUP_DIR>/bigdb_tail.trn' WITH NORECOVERY;  -- if the original still exists: tail first
RESTORE LOG bigdb FROM DISK = '<BACKUP_DIR>/bigdb_tail.trn' WITH RECOVERY;
-- database is online; unrestored filegroups such as FG_2023 stay offline and inaccessible

-- stage 2 (online in Enterprise): read-only filegroup needs no log replay
RESTORE DATABASE bigdb FILEGROUP = 'FG_2023' FROM DISK = '<BACKUP_DIR>/bigdb_FG_2023.bak' WITH RECOVERY;
```
Read-write filegroups restored later need the log chain from their backup to now applied
(`RESTORE LOG ... WITH RECOVERY` after the filegroup restore, and a fresh log backup taken).

## Check state
```sql
SELECT name, state_desc, is_read_only FROM bigdb.sys.database_files;
SELECT name, is_read_only FROM bigdb.sys.filegroups;
```

## Gotchas
- Queries must avoid offline filegroups: unrestored filegroups are not accessible.
- Practise the full sequence on a copy: getting the order wrong forces starting over.
- Under the simple recovery model the piecemeal sequence starts from a full or partial backup.

## Verify
Time each stage in a drill; record the time-to-online for the current data, the real RTO.

## Checked
2026-10-28. Confirmed against the Piecemeal Restores, Partial Backups, File Restores and BACKUP pages: READ_WRITE_FILEGROUPS makes a partial backup (primary plus read/write filegroups, optionally read-only ones), all editions support offline piecemeal restore and Enterprise also online, log backups are not applied to a filegroup that has been read-only since before its backup, read/write filegroups need an unbroken log chain, unrestored filegroups remain offline and inaccessible, piecemeal restore also works under the simple recovery model starting from a full or partial backup.
Removed unconfirmed claims: RECOVERY_PENDING state and errors 8653/679, the WITH PARTIAL gotcha, the simple-recovery sentence as written.
Method: documentation only; no commands were run.
