---
id: computing-software.database-administration.sql-server.restore-sequences-norecovery-and-stopat
name: restore-sequences-norecovery-and-stopat
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sql-server-backup, restore, norecovery, restore-stopat, stopatmark, point-in-time-restore, with-move, standby, restore-headeronly]
level: practitioner
status: docs-checked
description: "Restore a SQL Server database full, diff and log chain with NORECOVERY, stop at a point in time or mark, relocate files, and bring it online."
sources:
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/restore-statements-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/restore-a-sql-server-database-to-a-point-in-time-full-recovery-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restore sequences: NORECOVERY, STOPAT, RECOVERY

**Goal:** bring a database back to an exact moment (just before the bad `DELETE`)
with the minimum number of backups and no surprises.

## Order
1. Latest full before the target time - `WITH NORECOVERY`.
2. Latest differential after that full and before the target (optional) - `WITH NORECOVERY`.
3. Every log backup after the diff (or full), in order, up to the one containing the
   target time - `WITH NORECOVERY`, the last with `STOPAT`.
4. `RESTORE DATABASE ... WITH RECOVERY` to roll back uncommitted work and open it.
`RECOVERY` is the default: forgetting `NORECOVERY` on step 1 ends the sequence and
you start over.

## Inspect backups first
```sql
RESTORE HEADERONLY   FROM DISK = N'...\appdb_full.bak';  -- BackupType, FirstLSN, LastLSN, BackupStartDate
RESTORE FILELISTONLY FROM DISK = N'...\appdb_full.bak';  -- logical names for MOVE
```

## Point-in-time example, restored as a side-by-side copy
```sql
RESTORE DATABASE appdb_pit FROM DISK = N'...\appdb_full_0100.bak'
  WITH NORECOVERY, REPLACE,
       MOVE 'appdb'     TO '<DATA_DIR>\appdb_pit.mdf',
       MOVE 'appdb_log' TO '<LOG_DIR>\appdb_pit.ldf', STATS = 10;
RESTORE DATABASE appdb_pit FROM DISK = N'...\appdb_diff_1200.bak' WITH NORECOVERY;
RESTORE LOG appdb_pit FROM DISK = N'...\appdb_log_1215.trn' WITH NORECOVERY;
RESTORE LOG appdb_pit FROM DISK = N'...\appdb_log_1230.trn'
  WITH STOPAT = '2026-10-16T12:24:30', RECOVERY;
```
Restoring side by side and copying back the damaged rows is usually better than
overwriting production.

Named marks: `BEGIN TRAN deploy_42 WITH MARK 'before deploy'` then restore with
`STOPATMARK = 'deploy_42'` or `STOPBEFOREMARK`.

## Peeking while restoring
`WITH STANDBY = '<DATA_DIR>\undo_appdb_pit.tuf'` instead of `NORECOVERY` leaves the database
read-only between log restores, so you can check whether you have gone far enough
and continue restoring logs afterwards.

## Generate the script
Build the sequence from the `RESTORE HEADERONLY` output above, or use the SSMS point-in-time restore described on the Learn page.

## Gotchas
- `REPLACE` overwrites an existing database without tail-log protection: take a
  tail-log backup first if the current log matters.
- A log backup taken during bulk-logged operations cannot be used for STOPAT inside it.

## Verify
- [ ] `RESTORE HEADERONLY` LSNs confirm a continuous chain before you begin.
- [ ] Restored copy contains the rows just before the incident and none after.
- [ ] `DBCC CHECKDB` on the restored copy is clean.

## Checked
2026-10-31. Confirmed against the Learn pages for RESTORE statements and point-in-time restore: RECOVERY is the default and ends the sequence, NORECOVERY, STANDBY (read-only, undo file), STOPAT, STOPATMARK/STOPBEFOREMARK with a mark name, `BEGIN TRAN ... WITH MARK`, HEADERONLY and FILELISTONLY, MOVE, REPLACE losing the unbacked-up tail of the log, bulk-logged log backups blocking point-in-time inside them.
Removed as unconfirmed: the claim that STOPAT uses server local time, that STOPATMARK is inclusive, the instant-file-initialisation remark, the `sp_change_users_login` deprecation, and the dbatools and SSMS Timeline pointers.
Method: documentation only; no commands were run.
