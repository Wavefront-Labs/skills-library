---
id: computing-software.database-administration.sql-server.checktable-and-checkfilegroup-for-vldbs
name: checktable-and-checkfilegroup-for-vldbs
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, dbcc-checkdb, dbcc-checktable, checkfilegroup, checkalloc, checkcatalog, vldb, integrity-checks]
level: advanced
status: docs-checked
description: "Split integrity checks on very large SQL Server databases across nights with CHECKALLOC, CHECKCATALOG, CHECKTABLE and CHECKFILEGROUP while keeping full coverage."
sources:
  - https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checktable-transact-sql
  - https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkfilegroup-transact-sql
  - https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkalloc-transact-sql
  - https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-checkdb-transact-sql
  - https://ola.hallengren.com/sql-server-integrity-check.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CHECKTABLE / CHECKFILEGROUP for very large databases

When a full `DBCC CHECKDB` on a multi-TB database does not fit the maintenance window, split
it into its components. `CHECKDB` = `CHECKALLOC` + `CHECKTABLE` of every table/indexed view +
`CHECKCATALOG` (+ Service Broker and FILESTREAM checks).

## Pieces
```sql
DBCC CHECKALLOC (Sales) WITH NO_INFOMSGS;        -- allocation structures; relatively quick
DBCC CHECKCATALOG (Sales) WITH NO_INFOMSGS;      -- metadata consistency
DBCC CHECKTABLE ('dbo.Orders') WITH NO_INFOMSGS, ALL_ERRORMSGS;      -- one table and its indexes
DBCC CHECKTABLE ('dbo.Orders', NOINDEX);         -- skips the intensive checks on nonclustered indexes of user tables
DBCC CHECKFILEGROUP (N'FG_2026') WITH NO_INFOMSGS;   -- all objects in a filegroup (run in the db)
```
`CHECKTABLE` and `CHECKFILEGROUP` accept `PHYSICAL_ONLY` (physical structure and allocation checks only; much faster, skips logical and FILESTREAM checks); `CHECKALLOC` does not.
`TABLOCK` (all three accept it) skips the internal snapshot and takes locks instead, so concurrency drops.
`CHECKFILEGROUP` already includes `CHECKALLOC` of the filegroup and `CHECKTABLE` of every table and indexed view in it.

## Weekly rotation pattern
- Every night: `CHECKALLOC` and `CHECKCATALOG` (cheap).
- Every night: `CHECKTABLE` for 1/7th of the tables, chosen by size buckets so each night
  takes similar time.
- Weekly or monthly: full `CHECKDB` on a **restored copy** elsewhere (also tests backups).
Ola Hallengren's `DatabaseIntegrityCheck` automates this with
`@CheckCommands = 'CHECKALLOC,CHECKCATALOG,CHECKTABLE'`, `@TimeLimit` (seconds after which no further commands are started).

## Partitioned/filegroup designs
If old partitions sit on read-only filegroups, check them once after they become read-only
(and after restores) and check only the active filegroups nightly with `CHECKFILEGROUP`.

## Gotchas
- `CHECKTABLE` misses allocation and catalog problems; you still need the other two.
- Online checks use an internal database snapshot; if one cannot be created, `CHECKALLOC` and `CHECKFILEGROUP` acquire locks instead. Azure SQL Hyperscale does not support `CHECKDB` or `CHECKFILEGROUP` (use `CHECKTABLE ... WITH TABLOCK`).
- Track coverage: log which tables were checked when, and alert if any table goes more than
  two cycles unchecked.

## Verify
A coverage query over your log table shows every user table checked within the last 7 days
and `CHECKALLOC`/`CHECKCATALOG` nightly with zero errors.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: DBCC CHECKDB, CHECKTABLE, CHECKALLOC and CHECKFILEGROUP reference pages for SQL Server 2025 (CHECKDB covers allocation, tables and indexed views, catalog and Service Broker; CHECKFILEGROUP = CHECKALLOC of the filegroup plus CHECKTABLE of its tables and indexed views; CHECKTABLE syntax with NOINDEX, ALL_ERRORMSGS, NO_INFOMSGS, TABLOCK, PHYSICAL_ONLY, MAXDOP; CHECKALLOC accepts only ALL_ERRORMSGS, NO_INFOMSGS, TABLOCK, ESTIMATEONLY; TABLOCK uses locks instead of an internal snapshot; Hyperscale note), Ola Hallengren DatabaseIntegrityCheck (@CheckCommands values, @TimeLimit semantics, @PhysicalOnly). Wrong in the draft: PHYSICAL_ONLY is not accepted by CHECKALLOC (or CHECKCATALOG), and index_id 1 was presented as limiting CHECKTABLE to the clustered index. Removed as unconfirmed: the cross-filegroup partial-check claim, errors 1823/5128 and Ola's least-recently-checked resume behaviour (the Ola page does not document it).
Method: documentation only; no commands were run.
