---
id: computing-software.database-administration.sql-server.row-and-page-data-compression
name: row-and-page-data-compression
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, index-fragmentation, data-compression, page-compression, row-compression, storage-savings]
level: practitioner
status: docs-checked
description: "Estimate and apply SQL Server ROW or PAGE compression per index or partition, choosing by update pattern and scan profile, and roll it out online."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/data-compression/data-compression
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-estimate-data-compression-savings-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/data-compression/enable-compression-on-a-table-or-index
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Row and page data compression

Row and page compression are not available in every edition (see Microsoft's editions and supported features pages).
Data is stored in fewer pages, so I/O-heavy workloads can improve, at the cost of extra CPU to compress and decompress. Microsoft notes
the details can change in service packs and releases and that enabling compression can change query plans.

| Type | Applies to |
|---|---|
| ROW | whole heap, clustered index, nonclustered index or indexed view, per partition |
| PAGE | the same objects; leaf pages get row and page compression, non-leaf pages do not get page compression |
| COLUMNSTORE / COLUMNSTORE_ARCHIVE | columnstore tables and indexes; archive adds the XPRESS algorithm and is slower to read |
Off-row data (for example an XML value over 8,060 bytes, or other large values stored separately) is **not** compressed by ROW/PAGE
(SQL Server 2022 adds separate XML compression for off-row XML). `COMPRESS()` (GZIP) output cannot be indexed. Not available for system tables;
incompatible with sparse columns; a table cannot be compressed if max row size plus compression overhead exceeds 8,060 bytes.

## Estimate first
```sql
EXEC sp_estimate_data_compression_savings
  @schema_name = 'dbo', @object_name = 'OrderLines',
  @index_id = NULL, @partition_number = NULL, @data_compression = 'PAGE';
```
It samples the object into an equivalent table in tempdb and compresses that; compare `size_with_current_compression_setting (KB)` and
`size_with_requested_compression_setting (KB)`. It takes an IS lock and needs SELECT plus VIEW DATABASE STATE and VIEW DEFINITION
(on the database and tempdb). `@data_compression` accepts NONE, ROW, PAGE, COLUMNSTORE, COLUMNSTORE_ARCHIVE; a result larger than current means do not compress.

## Which indexes
Choose per object (and per partition: partitions of one object may use different settings). Microsoft's trade-off is storage and I/O
against CPU, so measure on production-like load; `sp_estimate_data_compression_savings` gives the storage side.

## Apply
```sql
ALTER TABLE dbo.OrderLines REBUILD WITH (DATA_COMPRESSION = PAGE, ONLINE = ON);   -- heap or clustered
ALTER INDEX IX_OrderLines_Product ON dbo.OrderLines REBUILD WITH (DATA_COMPRESSION = PAGE, ONLINE = ON);
ALTER TABLE dbo.Sales REBUILD PARTITION = 3 WITH (DATA_COMPRESSION = PAGE);       -- one partition
```
Nonclustered indexes do **not** inherit the table's compression; set each explicitly (default NONE). Changing a heap's compression rebuilds
its nonclustered indexes; enabling it online on a heap is single-threaded. Disk space needs equal those of creating or rebuilding an index
(rebuild one partition at a time to reduce them); online index operations are fully logged, so allow for log growth and log backups.

## Gotchas
- New pages in a PAGE-compressed heap get page compression only from bulk import with bulk optimizations, `INSERT INTO ... WITH (TABLOCK)`
  into a table with no nonclustered index, or an `ALTER TABLE ... REBUILD` with PAGE; other DML pages stay uncompressed until a rebuild.
- Compression does not affect backup/restore or log shipping; exported data (bcp, native format) is uncompressed.
- Extra CPU is required; test with production-like load.

## Verify
```sql
SELECT OBJECT_NAME(p.object_id), i.name, p.partition_number, p.data_compression_desc, p.rows
FROM sys.partitions p JOIN sys.indexes i ON i.object_id = p.object_id AND i.index_id = p.index_id
WHERE p.object_id = OBJECT_ID('dbo.OrderLines');
```
and compare the `sp_estimate_data_compression_savings` estimate with the real size after the change.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for Data compression and sys.sp_estimate_data_compression_savings (2017-2025).
Confirmed: objects and partitions that can be compressed, off-row and system table limits, sparse column incompatibility, nonclustered index and heap behaviour, bulk-load PAGE rules, space and logging rules, estimator syntax, columns, permissions and 2022 XML option. Removed unconfirmed claims: all-editions-since-2016-SP1, buffer-pool memory saving, typical-saving percentages, 5-10x columnstore ratio, the index-operational-stats heuristic and `sp_spaceused`.
Method: documentation only; no commands were run.
