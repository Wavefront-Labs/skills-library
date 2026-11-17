---
id: computing-software.database-administration.sql-server.automatic-page-repair-in-availability-groups
name: automatic-page-repair-in-availability-groups
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, automatic-page-repair, availability-groups, database-mirroring, error-823, error-824, corruption, dm-hadr-auto-page-repair]
level: advanced
status: docs-checked
description: "Understand and monitor automatic page repair in SQL Server availability groups: which errors trigger it, how to check repairs, and what it does not fix."
sources:
  - https://learn.microsoft.com/en-us/sql/sql-server/failover-clusters/automatic-page-repair-availability-groups-database-mirroring
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-hadr-auto-page-repair-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-objects/sys-dm-hadr-auto-page-repair-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic page repair in availability groups

When a replica reads a page and hits certain corruption errors, it marks the page unreadable,
requests a fresh copy from a partner replica, and replaces it. No DBA action, but every repair is
evidence of failing storage that you must chase.

## What triggers it
- Error 823 (OS-level IO failure, CRC), 824 (logical: bad checksum, torn page, wrong page ID),
  and 829 (page marked restore pending).
- Primary: attempted only while the database is SYNCHRONIZED and the primary is still sending log to the secondary. It asks the secondaries, takes the first copy returned, and queries touching the page fail with error 829 until repaired.
- Secondary: redo suspends for the database until the page arrives from the primary.

## What it does not repair
File header page (page 0), boot page (page 9 in file 1), allocation pages (GAM, SGAM, PFS),
and pages in databases that are not in an AG or mirroring session.

## Monitor
```sql
-- on each replica
SELECT DB_NAME(database_id) AS db, file_id, page_id, error_type, page_status, modification_time
FROM sys.dm_hadr_auto_page_repair ORDER BY modification_time DESC;   -- up to 100 rows per database

SELECT DB_NAME(database_id), file_id, page_id, event_type, error_count, last_update_date
FROM msdb.dbo.suspect_pages;
```
`page_status` values: 2 queued for request from partner, 3 request sent to partner, 4 repaired, 5 not repaired in the last attempt (repair is retried).
Add an Agent alert on errors 823, 824 and 829 (the repair triggers) on every replica, and a job
that mails new rows in `sys.dm_hadr_auto_page_repair`.

## After a repair
1. Run `DBCC CHECKDB` on the affected database (on the primary, and on a secondary if that is where backups run).
2. Check storage: Windows System event log disk errors, SAN/HBA logs, firmware.
3. If repair keeps failing (`page_status` 5, or the secondary stays SUSPENDED because it never received the page), restore the page from backup (see page restore skill).
4. Repeated repairs on one replica: fail over away from it and replace its storage.

## Gotchas
- Clean old restored entries (event_type 4 on a secondary, 5 on a primary) out of `msdb.dbo.suspect_pages` periodically.
- Repair is asynchronous: applications should retry operations that fail with 823, 824 or 829.
- Unlike `DBCC CHECKDB ... REPAIR_ALLOW_DATA_LOSS`, automatic page repair preserves all data.

## Verify
Alerts for 823/824/825 exist on all replicas and fire to an operator; the monitoring query is part of the daily health check.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: automatic page repair article (errors 823 CRC, 824, 829; unrepairable page 0, page 9, GAM/SGAM/PFS; primary repair only when SYNCHRONIZED and still sending log; secondary SUSPENDED until the page arrives; suspect_pages event_type 4 and 5; retry guidance), sys.dm_hadr_auto_page_repair (columns, 100 rows per database, page_status 2 to 5). Wrong in the draft: page_status 3 and 5 meanings (5 means retry, not a manual-restore state), and 825 is not a repair trigger. Removed as unconfirmed: the 1000-row suspect_pages cap, DMV clearing on restart, replicated-log-corruption claim, CHECKDB-on-secondary claim and the Basic/distributed AG claim.
Method: documentation only; no commands were run.
