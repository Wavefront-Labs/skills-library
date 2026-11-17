---
id: computing-software.database-administration.sql-server.columnstore-indexes
name: columnstore-indexes
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, columnstore-index, clustered-columnstore, nonclustered-columnstore, rowgroup, delta-store, tuple-mover, batch-mode, segment-elimination, real-time-operational-analytics, execution-plan]
level: advanced
status: docs-checked
description: "Choose and build SQL Server clustered or nonclustered columnstore indexes, load them into compressed rowgroups, and maintain rowgroup quality."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/columnstore-indexes-overview
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/columnstore-indexes-data-loading-guidance
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/columnstore-indexes-defragmentation
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/columnstore-indexes-design-guidance
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/columnstore-indexes-query-performance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Columnstore indexes

**Goal:** 10x compression and batch-mode scans for analytic queries over large tables.

## Which kind
- **Clustered columnstore (CCI)**: the table itself is columnar. Fact tables and
  large append-mostly history; Microsoft's design guidance wants at least about a million rows per partition.
- **Nonclustered columnstore (NCCI)** on a rowstore table: real-time operational
  analytics on an OLTP table. Filtered NCCI (`WHERE status = 'closed'`) keeps hot
  rows out of the columnstore.
```sql
CREATE CLUSTERED COLUMNSTORE INDEX cci_sales ON dbo.sales_fact
  WITH (MAXDOP = 1, DATA_COMPRESSION = COLUMNSTORE);   -- ORDER (sale_date) on 2022+
CREATE NONCLUSTERED COLUMNSTORE INDEX ncci_orders ON dbo.orders (order_date, customer_id, amount, status);
```
`MAXDOP = 1` on build gives a perfectly ordered index on the chosen column and so better segment elimination. `ORDER (...)` is available for clustered columnstore from SQL Server 2022 (nonclustered from 2025) and is best built with `MAXDOP = 1`.

## Rowgroups and the delta store
- Ideal rowgroup = 1,048,576 rows, compressed. Bulk inserts of >= 102,400 rows go
  straight to compressed rowgroups; smaller inserts and all updates land in the
  row-based **delta store**, which the tuple mover compresses when it reaches 1 M rows.
- Deletes only mark rows in the delete bitmap; updates = delete + insert into delta store.
- Load in batches of at least 102,400 rows (ideally 1,048,576) so rowgroups compress directly. From SQL Server 2019 a background merge task also helps the tuple mover.

## Health check
```sql
SELECT OBJECT_NAME(object_id) tbl, state_desc, COUNT(*) rowgroups,
       SUM(total_rows) rows, SUM(deleted_rows) deleted, AVG(total_rows) avg_rows,
       trim_reason_desc
FROM sys.dm_db_column_store_row_group_physical_stats
GROUP BY object_id, state_desc, trim_reason_desc;
```
Trouble signs: many small COMPRESSED rowgroups (`trim_reason_desc` = MEMORY_LIMITATION,
DICTIONARY_SIZE, BULKLOAD with small batches), many OPEN delta stores, deleted_rows around 10 % or more (REORGANIZE removes deleted rows from a rowgroup once 10 % or more are deleted).

## Maintenance
```sql
ALTER INDEX cci_sales ON dbo.sales_fact REORGANIZE;   -- merges small rowgroups, removes deleted rows (2016+), online
ALTER INDEX cci_sales ON dbo.sales_fact REORGANIZE WITH (COMPRESS_ALL_ROW_GROUPS = ON);  -- force-close delta stores
ALTER INDEX cci_sales ON dbo.sales_fact REBUILD PARTITION = 12;   -- last resort, per partition
```
Partition big CCIs by date so rebuilds and switching work per partition.

## Query side
- Look for **batch mode** on operators in the actual plan; see the Columnstore query performance page for segment elimination.
- Ordering the data (or `ORDER`) helps segment elimination, especially on string columns; it matters most on the filter column.
- Avoid heavy deletes and updates on a CCI (design guidance: keep them under about 10 % of rows).

## Verify
- [ ] Average rows per compressed rowgroup near 1 M; deleted rows under ~10 %.
- [ ] Analytic queries show batch mode and skipped segments in plans/stats.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: SQL Server 2025 index design guide and CREATE COLUMNSTORE INDEX page (102,400-row threshold for compressed rowgroups, 1,048,576-row delta rowgroups and OPEN/CLOSED/COMPRESSED transitions, ALTER INDEX REBUILD or REORGANIZE forces delta rowgroups in; ORDER clause from SQL Server 2022 for clustered and 2025 for nonclustered; filtered nonclustered columnstore from 2016; MAXDOP = 1 for best ordering; COMPRESSION_DELAY), columnstore design guidance and query performance (about a million rows per partition, under 10 % deletes or updates, MAXDOP = 1 build is perfectly ordered), REORGANIZE behaviour (2016: online, merges rowgroups, removes deleted rows at 10 %, COMPRESS_ALL_ROW_GROUPS), 2019 background merge, sys.dm_db_column_store_row_group_physical_stats (trim_reason_desc values, total_rows, deleted_rows). Removed as unconfirmed: the 10 M row guideline, nonclustered B-tree on CCI version note, TABLOCK parallel load advice, the Locally Aggregated Rows counter, STATISTICS IO field names and the string-predicate 2022 gate.
Method: documentation only; no commands were run.
