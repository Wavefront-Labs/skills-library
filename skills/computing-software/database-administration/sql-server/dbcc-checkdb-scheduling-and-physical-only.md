---
id: computing-software.database-administration.sql-server.dbcc-checkdb-scheduling-and-physical-only
name: dbcc-checkdb-scheduling-and-physical-only
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, dbcc-checkdb, physical-only, consistency-check, corruption-detection, ola-hallengren, offload-checkdb, data-purity]
level: practitioner
status: docs-checked
description: "Schedule DBCC CHECKDB on SQL Server so corruption is caught within backup retention: full vs PHYSICAL_ONLY, splitting large databases, and offloading to a restored copy."
sources:
  - https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkdb-transact-sql
  - https://ola.hallengren.com/sql-server-integrity-check.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduling DBCC CHECKDB

**Goal:** corruption is detected while you still have a clean backup to restore
from: check frequency must be shorter than backup retention.

## Commands
```sql
DBCC CHECKDB (appdb) WITH NO_INFOMSGS, ALL_ERRORMSGS;           -- full logical + physical
DBCC CHECKDB (appdb) WITH PHYSICAL_ONLY, NO_INFOMSGS;            -- page checksums, allocation; much faster
DBCC CHECKDB (appdb) WITH DATA_PURITY;                           -- for databases upgraded from earlier versions
```
CHECKDB runs on an internal database snapshot unless you specify TABLOCK.

## Strategy for large databases
- Frequent PHYSICAL_ONLY runs plus a periodic full CHECKDB (Microsoft recommends both), or
- Split: `DBCC CHECKALLOC` + `DBCC CHECKCATALOG` on a schedule, and `DBCC CHECKTABLE`
  on a subset of tables each night so every table is covered within your cycle.
- **Offload**: restore last night's full backup on another server and run full
  CHECKDB there. This also tests the backup. It does not check the production
  files' current state, so still run PHYSICAL_ONLY on production.


With Ola Hallengren's maintenance solution:
```sql
EXECUTE dbo.DatabaseIntegrityCheck @Databases = 'USER_DATABASES', @CheckCommands = 'CHECKDB',
  @PhysicalOnly = 'Y', @LogToTable = 'Y';
```

## Make failures visible
- Run as an Agent job that **fails** on errors and alerts (Database Mail operator).
- Alert on `msdb.dbo.suspect_pages` rows.

## Gotchas
- `WITH TABLOCK` takes locks instead of using an internal snapshot (including a short exclusive
  lock on the database): faster under heavy load but less concurrency, and it skips
  CHECKCATALOG and Service Broker validation.
- Do not run REPAIR options as first response; see the repair skill.

## Verify
The last full CHECKDB of every database is more recent than your backup retention; job history shows success.

## Checked
2026-10-28. Confirmed against the DBCC CHECKDB reference and suspect_pages pages: PHYSICAL_ONLY gives a much shorter run-time and is recommended for frequent use with a periodic full run, DATA_PURITY for databases upgraded from earlier versions, internal database snapshot versus TABLOCK (faster under load, less concurrency, skips CHECKCATALOG and Service Broker validation), CHECKALLOC / CHECKCATALOG / CHECKTABLE commands, suspect_pages in msdb, and the Ola Hallengren DatabaseIntegrityCheck parameters PhysicalOnly and LogToTable.
Removed unconfirmed claims: the MAXDOP option version gate, I/O and tempdb load, the AG secondary corruption claim, error 823/824/825 alerts, dbi_dbccLastKnownGood, PAGE_VERIFY note, ReFS snapshot failures, fixed weekly/nightly cadences.
Method: documentation only; no commands were run.
