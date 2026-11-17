---
id: computing-software.database-administration.sql-server.repair-allow-data-loss-and-emergency-mode
name: repair-allow-data-loss-and-emergency-mode
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, dbcc-checkdb, repair-allow-data-loss, emergency-mode, suspect-database, corruption-last-resort, repair-rebuild]
level: sme
status: docs-checked
description: "Decide when DBCC CHECKDB REPAIR_ALLOW_DATA_LOSS or EMERGENCY mode is the last resort for a corrupt or SUSPECT SQL Server database, and how to run it with eyes open."
sources:
  - https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkdb-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/databases/database-states
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REPAIR_ALLOW_DATA_LOSS and EMERGENCY mode

**Goal:** when no clean backup exists, salvage the most data possible, knowing
exactly what repair throws away.

## Order of preference
1. Restore (page restore, file restore, full + logs) from good backups.
2. Fail over to a healthy AG replica / log-shipping secondary.
3. If the errors are confined to nonclustered indexes, rebuilding those indexes may be enough; check the CHECKDB output first.
4. Only then: REPAIR_ALLOW_DATA_LOSS.
`CHECKDB` names the repair option to use at the end of its error list; that is the tool's
estimate, not a recommendation. Microsoft calls REPAIR_ALLOW_DATA_LOSS an emergency last resort,
and it can lose more data than restoring the last known good backup.

## Running repair
```sql
-- first make physical copies of all data, log and other database files (Microsoft requires this before repair)
ALTER DATABASE appdb SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
BEGIN TRANSACTION;   -- optional: repair can run under a user transaction so you can roll back (not in EMERGENCY mode)
DBCC CHECKDB (appdb, REPAIR_ALLOW_DATA_LOSS) WITH NO_INFOMSGS, ALL_ERRORMSGS;
-- inspect, then COMMIT or ROLLBACK
COMMIT;
ALTER DATABASE appdb SET MULTI_USER;
```
Repair deallocates corrupt pages: **rows on them are gone**, and it does not
respect foreign keys or business rules (orphaned children). Run `DBCC CHECKCONSTRAINTS`
afterwards and reconcile data with the application owners.

## SUSPECT / RECOVERY_PENDING databases
If crash recovery itself failed (log corruption), the database is SUSPECT:
```sql
ALTER DATABASE appdb SET EMERGENCY;      -- single-user, READ_ONLY, sysadmin access only
-- try to copy data out first (SELECT INTO another database / bcp)
ALTER DATABASE appdb SET SINGLE_USER;
DBCC CHECKDB (appdb, REPAIR_ALLOW_DATA_LOSS);   -- in EMERGENCY, rebuilds the log if recovery failed because of log corruption
ALTER DATABASE appdb SET MULTI_USER;
```
Rebuilding the log can lose transactional consistency and leaves no full ACID guarantee: treat
the result as suspect data, run `DBCC CHECKCONSTRAINTS` and back up immediately. The log size is
left at its default and must be resized by hand.

## Gotchas
- After any repair, take a new full backup immediately.
- Root cause (storage, drivers, memory) must be found, or it happens again.

## Checked
2026-11-01. Confirmed on the DBCC CHECKDB and database states Learn pages: last-resort wording, single-user requirement, copy files before repair, EMERGENCY behaviour, transaction rollback limits, log rebuild consequences, CHECKCONSTRAINTS, back up after repair. Removed: index_id rule, 'rare in practice' claim, output-line quote.
Method: documentation only; no commands were run.

## Verify
A second `DBCC CHECKDB` returns clean; affected tables' row counts compared to
expectations; data loss documented for the business.
