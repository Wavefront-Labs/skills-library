---
id: computing-software.database-administration.sql-server.examining-pages-with-dbcc-page-and-dbcc-ind
name: examining-pages-with-dbcc-page-and-dbcc-ind
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, dbcc-page, dbcc-ind, dm-db-page-info, dm-db-database-page-allocations, corruption, page-internals]
level: sme
status: docs-checked
description: "Inspect SQL Server data pages with DBCC PAGE, sys.dm_db_page_info and DBCC IND / dm_db_database_page_allocations to map a corrupt page to its object and rows."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-db-page-info-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/pages-and-extents-architecture-guide
  - https://www.sqlskills.com/blogs/paul/inside-the-storage-engine-using-dbcc-page-and-dbcc-ind-to-find-out-if-page-splits-ever-roll-back/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Examining pages with DBCC PAGE and DBCC IND

Used when CHECKDB or error 824 names a page (`(1:153422)` = file 1, page 153422) and you need
to know which table, index and rows sit there before choosing repair, page restore or rebuild.

## Which object owns a page (supported, SQL Server 2019+)
```sql
SELECT * FROM sys.dm_db_page_info(DB_ID('appdb'), 1, 153422, 'DETAILED');
```
Returns the page header, including object ID, index ID and partition ID. It cannot show the page body.
If the page header itself is corrupt, this fails too; fall back to DBCC PAGE.

## DBCC PAGE (unsupported)
Still needed when you want the page contents rather than just the header. Use `DBCC TRACEON (3604)`
to send output to the client. The output format is not documented: do not build automation on it.

## Pages of an index
`sys.dm_db_database_page_allocations` (SQL Server 2012+) lists the pages of a table or index,
but it is not supported and is subject to change; use it on a restored copy and do not depend on it.

## Gotchas
- Run against a restored copy where possible; `DETAILED` scans on large tables are heavy.

## Verify
You can name the object and index for the corrupt page before choosing a fix.

## Checked
2026-10-28. Confirmed against the sys.dm_db_page_info and sys.dm_db_database_page_allocations pages: dm_db_page_info exists from SQL Server 2019, returns the page header (object ID, index ID, partition ID) and is a supported alternative to DBCC PAGE in many cases but not for page contents; DBCC PAGE is unsupported; sys.dm_db_database_page_allocations is available from SQL Server 2012 but is not supported and subject to change.
Removed unconfirmed claims: the dm_db_page_info column list, DBCC PAGE print options and header-field/page-type numbers, DBCC IND, fn_PhysLocFormatter, the index_id interpretation, and the buffer-pool gotcha.
Method: documentation only; no commands were run.
