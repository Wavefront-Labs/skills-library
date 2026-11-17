---
id: computing-software.database-administration.sql-server.tempdb-configuration-and-contention
name: tempdb-configuration-and-contention
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, tempdb, pagelatch, pfs-contention, gam, sgam, memory-optimized-tempdb-metadata, version-store, sql-server-configuration]
level: advanced
status: docs-checked
description: "Lay out SQL Server tempdb data files, diagnose PAGELATCH allocation and metadata contention, and handle version store and spill growth."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/databases/tempdb-database
  - https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/performance/recommendations-reduce-allocation-contention
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tempdb configuration and contention

**Goal:** a tempdb that does not become the instance-wide bottleneck for temp
tables, sorts/hash spills, version store and online index builds.

## Layout
- Data files: as many as logical processors up to 8; above 8 start at 8 and add files in multiples of 4 only if
  allocation contention persists. Setup (2016+) adds the lower of logical processors or 8 (`/SQLTEMPDBFILECOUNT`).
- All data files **equal initial size and equal autogrowth** (the engine's proportional fill favours files with more free space,
  and Microsoft gives 64 MB as an example growth increment). Pre-size them so autogrowth is the exception.
- Fast I/O subsystem; separate disks per file are not required unless you see disk-level bottlenecks. tempdb is re-created at every start.
```sql
ALTER DATABASE tempdb MODIFY FILE (NAME = tempdev,  SIZE = 8GB, FILEGROWTH = 1GB);
ALTER DATABASE tempdb ADD FILE (NAME = temp2, FILENAME = '<TEMPDB_DIR>\temp2.ndf', SIZE = 8GB, FILEGROWTH = 1GB);
-- sizes above are examples; every data file must get the same size and growth. Moving files: see "Move system databases".
```
Defaults on a new install: 8 MB files growing by 64 MB; logical names `tempdev`, `temp#`, `templog`.
Trace flags 1117/1118 are not needed from SQL Server 2016 (all data files autogrow together; uniform extents only); do not add them.
With instant file initialization, log growth up to 64 MB is also instant on 2022+.

## Diagnose contention
```sql
SELECT r.session_id, r.wait_type, r.wait_resource, r.wait_time
FROM sys.dm_exec_requests r
WHERE r.wait_type LIKE 'PAGELATCH%' AND r.wait_resource LIKE '2:%';
```
`2:<file>:1` is the PFS page and `2:<file>:3` an SGAM page (a PFS page number is divisible by 8088; `2:1:2` is a GAM page)
-> `PAGELATCH_UP` on these is allocation contention: add equally sized files. Waits on system
object pages -> metadata contention. Microsoft's diagnostic joins `sys.dm_exec_requests` page_resource with `sys.dm_db_page_info`
(system table object ids 3, 9, 34, 40, 41, 54, 55, 60, 74, 75). On 2019+ and only when that contention clearly hurts (Microsoft warns of
current limitations, e.g. high `MEMORYCLERK_XTP` memory; consider a resource pool binding), enable
```sql
ALTER SERVER CONFIGURATION SET MEMORY_OPTIMIZED TEMPDB_METADATA = ON;  -- restart required; check SERVERPROPERTY('IsTempdbMetadataMemoryOptimized')
```
Not available in Azure SQL Database or Managed Instance. If the instance will not start afterwards, start with `-f` and turn it OFF.
Since 2016 temp tables and table variables are cached; SQL Server 2022 improved GAM/SGAM latch concurrency and 2019 made PFS updates concurrent.

## Space consumers
```sql
SELECT SUM(user_object_reserved_page_count)*8/1024 AS user_mb,
       SUM(internal_object_reserved_page_count)*8/1024 AS internal_mb,
       SUM(version_store_reserved_page_count)*8/1024 AS version_mb
FROM tempdb.sys.dm_db_file_space_usage;
SELECT session_id, user_objects_alloc_page_count, internal_objects_alloc_page_count
FROM sys.dm_db_session_space_usage ORDER BY internal_objects_alloc_page_count DESC;
```
The version store holds row versions for RCSI/snapshot isolation, online index operations, MARS and AFTER triggers
(per-database usage: `sys.dm_tran_version_store_space_usage`, 2017+). Internal objects cover sort and hash work tables and work files.
SQL Server 2025 adds accelerated database recovery in tempdb (a separate persistent version store) and tempdb space resource governance.

## Gotchas
- tempdb cannot be backed up or restored, set offline, or have its collation changed; it is re-created at each start.
- In Azure SQL Database each database has its own tempdb sized by service tier; Managed Instance lets you set file count, growth and max size.

## Verify
- [ ] Equal-size data files, count matched to cores, pre-sized.
- [ ] No sustained PAGELATCH waits on `2:*` resources under peak load.
- [ ] Alert on tempdb free space and on version store growth.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 tempdb Database page and the "Recommendations to reduce allocation contention" support article (2016-2025).
Confirmed: default file sizes and growth, file-count guidance and setup behaviour, equal-size rule, TF 1117/1118 no longer needed, PFS page rule and wait resources, memory-optimized tempdb metadata syntax/restart/limitations, `sys.dm_db_file_space_usage` and session/task space DMVs, version store contents. Removed unconfirmed claims: NVMe suitability, the 511232-page interval, temp-table caching defeat patterns, snapshot-transaction DMV, shrink behaviour.
Method: documentation only; no commands were run.
