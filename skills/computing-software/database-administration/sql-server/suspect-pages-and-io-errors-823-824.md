---
id: computing-software.database-administration.sql-server.suspect-pages-and-io-errors-823-824
name: suspect-pages-and-io-errors-823-824
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, dbcc-checkdb, suspect-pages, error-823, error-824, error-825, page-verify-checksum, agent-alerts, auto-page-repair]
level: practitioner
status: docs-checked
description: "Detect SQL Server storage corruption early: page_verify CHECKSUM, Agent alerts for errors 823/824/825, the msdb suspect_pages table, and AG automatic page repair."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/manage-the-suspect-pages-table-sql-server
  - https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/database-file-operations/troubleshoot-msg-824-logical-consistency-error
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Suspect pages and I/O errors 823/824/825

**Goal:** the first damaged page pages a DBA, long before CHECKDB runs or a user
hits it.

## The errors
| Error | Meaning |
|---|---|
| 823 | The operating system reported a failure (for example a CRC error) reading the page |
| 824 | Read succeeded but the page failed a check: bad checksum, torn page, bad page id |
Failed pages are logged in `msdb.dbo.suspect_pages` (one row per page, up to 1,000 rows).

## Alerts
Create SQL Server Agent alerts for errors 823 and 824 with an operator notification so the first damaged page reaches a DBA (see the SQL Server Agent alert documentation).

## Check the table
```sql
SELECT * FROM msdb.dbo.suspect_pages;
```
event_type: 1 = 823 (OS CRC error) or 824 other than bad checksum or torn page (for example a bad page ID), 2 = bad checksum, 3 = torn page, 4 = restored, 5 = repaired, 7 = deallocated by DBCC. The table holds at most 1,000 rows, so delete resolved entries (restored, repaired, deallocated) once handled.


## Next steps when it fires
Run CHECKDB on the database, restore pages (page restore skill), and investigate
the storage path (event log, driver/firmware, SAN logs).

## Verify
The alerts exist and are enabled with a notification, and `suspect_pages` has no unresolved rows.

## Checked

2026-10-28. Confirmed against Microsoft Learn (Manage the suspect_pages table): one row per failed page up to 1,000 rows, event_type values 1, 2, 3, 4, 5 and 7, 823 caused by an OS CRC error and 824 bad checksum / torn page / bad page ID, rows deleted by restore and repair actions. Removed unconfirmed: error 825 description, PAGE_VERIFY statements and checksum-rewrite behaviour, sp_add_alert and severity 19-25 commands, Database Mail requirement, availability group automatic page repair and DMV, column list of suspect_pages.

Method: documentation only; no commands were run.
