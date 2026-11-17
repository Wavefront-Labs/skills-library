---
id: computing-software.database-administration.sql-server.covering-indexes-with-included-columns
name: covering-indexes-with-included-columns
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, included-columns, covering-index, key-lookup, nonclustered-index, index-design, index-consolidation]
level: practitioner
status: docs-checked
description: "Design SQL Server covering nonclustered indexes: key column order vs INCLUDE columns, removing key lookups, and consolidating overlapping indexes."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/create-indexes-with-included-columns
  - https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-index-design-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Covering indexes with included columns

## Key lookup -> covering index
A plan with an Index Seek plus Key Lookup (Clustered) for many rows means the index finds rows
but must fetch other columns from the base table one row at a time. Cover the query:
```sql
-- query
SELECT OrderDate, Status, TotalDue FROM dbo.Orders WHERE CustomerId = @c AND OrderDate >= @from ORDER BY OrderDate;

CREATE NONCLUSTERED INDEX IX_Orders_Customer_OrderDate
ON dbo.Orders (CustomerId, OrderDate)       -- seek + order
INCLUDE (Status, TotalDue)                  -- only carried at the leaf
WITH (ONLINE = ON, DATA_COMPRESSION = PAGE);   -- ONLINE = ON needs an edition that supports online index operations
```

## Key or INCLUDE?
- **Key columns**: used for seeks, ranges, ORDER BY/GROUP BY, and joins. Order matters: equality
  predicates first, then the range or sort column. Nonclustered key limit: 32 columns / 1,700 bytes (16 / 900 before SQL Server 2016).
- **INCLUDE**: only returned or filtered after the seek. Not ordered, not in upper levels (smaller
  B-tree), allowed for `nvarchar(max)` and other (max) types (only text, ntext and image are excluded), up to 1,023 included columns, and not counted toward key limits (but large types are copied to the leaf and can grow the index a lot).
- Columns in WHERE with low selectivity (`Status`) can go in INCLUDE: the residual predicate is applied at the leaf.

## Missing-index suggestions
DMV and plan suggestions list equality, inequality and included columns; treat them as hints, compare them with existing indexes and merge them by hand:
```sql
-- existing
CREATE INDEX IX_A ON dbo.Orders (CustomerId) INCLUDE (Status);
-- suggested
CREATE INDEX IX_B ON dbo.Orders (CustomerId, OrderDate) INCLUDE (TotalDue);
-- consolidate into one: (CustomerId, OrderDate) INCLUDE (Status, TotalDue), then drop IX_A
```
An index whose keys are a left-prefix of another index's keys is usually redundant (unless it is
unique and enforces a constraint, or much narrower for a hot query).

## Costs
Every index adds write cost and log on INSERT/UPDATE/DELETE, memory in the buffer pool, and
maintenance time. Check reads vs writes before adding more:
```sql
SELECT i.name, s.user_seeks, s.user_scans, s.user_lookups, s.user_updates
FROM sys.indexes i LEFT JOIN sys.dm_db_index_usage_stats s
  ON s.object_id = i.object_id AND s.index_id = i.index_id AND s.database_id = DB_ID()
WHERE i.object_id = OBJECT_ID('dbo.Orders');
```
Wide indexes with many included columns duplicate much of the table, so keep INCLUDE lists to what the query needs.

## Verify
Actual plan after the change shows a seek with no key lookup, and `SET STATISTICS IO ON` logical reads drop.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: Create Indexes with Included Columns page for SQL Server 2025 (nonclustered only, up to 1,023 included columns, included columns do not count toward the key limits, 32 key columns and 1,700 bytes from SQL Server 2016 versus 16 and 900 before, only text/ntext/image barred as included columns, large types increase leaf size), index design guide, sys.dm_db_index_usage_stats columns. Wrong in the draft: the key limit was given as 16 columns / 1700 bytes (mixed generations). Removed as unconfirmed: the 5-10 nonclustered indexes rule of thumb and the claim about missing-index DMV key ordering.
Method: documentation only; no commands were run.
