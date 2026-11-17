---
id: computing-software.database-administration.sql-server.clustered-index-key-design-and-heaps
name: clustered-index-key-design-and-heaps
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, clustered-index, forwarded-records, heap, index-design, last-page-insert-contention, optimize-for-sequential-key]
level: advanced
status: docs-checked
description: "Choose SQL Server clustered index keys (narrow, unique, static, ever-increasing), recognise when a heap fits, and fix forwarded records and last-page insert contention."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-index-design-guide
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/heaps-tables-without-clustered-indexes
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/create-index-transact-sql
  - https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/performance/resolve-pagelatch-ex-contention
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-db-index-operational-stats-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clustered index key design and heaps

## The clustering key is copied everywhere
Every nonclustered index stores the clustering key as its row locator, so the key's width is paid
in every index. Good keys are:
- **Narrow**: `int`/`bigint` over a 3-column natural key or `uniqueidentifier` (16 bytes).
- **Unique**: otherwise a 4-byte internal uniquifier is added to the key (and so to every nonclustered index).
- **Immutable**: changing the key must also change every nonclustered index.
- **Not nullable, fixed width**: avoids a 3-4 byte NULL block and 2 extra bytes per variable-width value in every index.
- **Ever-increasing**: inserts go to the end; no mid-index page splits. random `uniqueidentifier` values are not ever-increasing and split pages mid-index (use `NEWSEQUENTIALID()` or a `bigint` identity/sequence clustering key and keep the GUID as a nonclustered unique key).
The primary key does not have to be the clustered index: `PRIMARY KEY NONCLUSTERED` plus a separate `CREATE CLUSTERED INDEX`.
Sometimes cluster on the main range-query column (e.g. `OrderDate, OrderId`) for reporting tables.

## Last-page insert contention
Many concurrent inserts on an identity key fight over the last page (`PAGELATCH_EX` waits on one page).
SQL Server 2019+: `CREATE INDEX ... WITH (OPTIMIZE_FOR_SEQUENTIAL_KEY = ON)` (or `ALTER INDEX ... SET`).
Alternatives (Microsoft's PAGELATCH_EX guide): a non-sequential leading key such as a hash modulo the CPU count, or memory-optimized tables for extreme rates.

## Heaps
A table without a clustered index. Fine for: staging tables loaded with `TABLOCK` and read once,
then truncated. Problems elsewhere:
- **Forwarded records**: an updated row that no longer fits moves and leaves a pointer; every
  scan follows the pointer (extra random IO).
- Deletes do not free pages without `TABLOCK` or a rebuild; scans read empty pages.
Find them:
```sql
SELECT OBJECT_NAME(ps.object_id) AS tbl, ps.forwarded_record_count, ps.page_count, ps.avg_page_space_used_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, 0, NULL, 'DETAILED') ps
WHERE ps.index_type_desc = 'HEAP' AND ps.forwarded_record_count > 0;

SELECT OBJECT_NAME(object_id), forwarded_fetch_count FROM sys.dm_db_index_operational_stats(DB_ID(), NULL, 0, NULL)
WHERE forwarded_fetch_count > 0 ORDER BY forwarded_fetch_count DESC;
```
Fix: add a suitable clustered index, or `ALTER TABLE dbo.t REBUILD;` (removes forwarding, but it
comes back; it also rebuilds all nonclustered indexes).

## Changing the clustered index
`CREATE CLUSTERED INDEX ... WITH (DROP_EXISTING = ON, ONLINE = ON)` rebuilds nonclustered
indexes only once, and only if the index definition (name, key and partition columns, uniqueness, sort order) changed; with `ONLINE = ON` they are rebuilt online too. Plan log space and run off-hours.

## Verify
No heaps with forwarded fetches in OLTP tables; clustering keys reviewed for width and uniqueness;
`PAGELATCH_EX` on hot insert tables addressed.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: SQL Server 2025 index design guide (desirable clustered key properties: narrow, unique with the 4-byte uniquifier otherwise, ever-increasing, immutable, not nullable, fixed width; uniqueidentifier is 16 bytes and not ever-increasing unless generated sequentially; memory-optimized tables for extreme throughput), CREATE INDEX (OPTIMIZE_FOR_SEQUENTIAL_KEY from SQL Server 2019, ALTER INDEX ... SET without rebuild, DROP_EXISTING behaviour for nonclustered indexes, ONLINE carries over), Resolve PAGELATCH_EX contention guide, Heaps page and sys.dm_db_index_physical_stats (forwarded_record_count for heaps in SAMPLED/DETAILED, ALTER TABLE REBUILD rebuilds the heap and its nonclustered indexes, TABLOCK delete deallocates pages), sys.dm_db_index_operational_stats (forwarded_fetch_count). Removed as unconfirmed: the claim that DROP_EXISTING avoids a double rebuild in all cases, the table-sized log space figure and the resumable suggestion.
Method: documentation only; no commands were run.
