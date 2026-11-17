---
id: computing-software.database-administration.sql-server.partition-switching-and-sliding-window
name: partition-switching-and-sliding-window
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, partition-switch, sliding-window, table-partitioning, partition-function, partition-scheme, truncate-partition, aligned-index]
level: advanced
status: docs-checked
description: "Partition large SQL Server tables by date, then load and archive with SWITCH, SPLIT and MERGE in a sliding window without long locks or data movement."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/partitions/partitioned-tables-and-indexes
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-partition-function-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partition switching and the sliding window

Partitioning has manageability and performance benefits: with aligned indexes whole partitions
can be switched in and out quickly.

## Setup (monthly, RANGE RIGHT)
```sql
CREATE PARTITION FUNCTION pf_month (date) AS RANGE RIGHT
  FOR VALUES ('2026-01-01','2026-02-01','2026-03-01', /* ... */ '2026-11-01');
CREATE PARTITION SCHEME ps_month AS PARTITION pf_month ALL TO ([PRIMARY]);
CREATE TABLE dbo.Sales (SaleDate date NOT NULL, SaleId bigint NOT NULL, Amount money,
  CONSTRAINT PK_Sales PRIMARY KEY CLUSTERED (SaleDate, SaleId)) ON ps_month (SaleDate);
```
RANGE RIGHT: each boundary is the first value of a partition (natural for dates). Keep an empty
partition at **both** ends so SPLIT/MERGE never move data.
All indexes should be **aligned** (on the same scheme, partition column in the key or included)
so switching works efficiently.

## Archive the oldest month
```sql
-- staging table matching the partitioned table (see the ALTER TABLE ... SWITCH reference for all requirements)
CREATE TABLE dbo.Sales_Out (... same ...) ON [PRIMARY];
ALTER TABLE dbo.Sales SWITCH PARTITION 2 TO dbo.Sales_Out;
-- export/archive dbo.Sales_Out, then drop or truncate it
ALTER PARTITION FUNCTION pf_month() MERGE RANGE ('2026-01-01');  -- remove the now-empty boundary
```
`TRUNCATE TABLE dbo.Sales WITH (PARTITIONS (2));` if no archive copy is needed.

## Load the new month
```sql
ALTER PARTITION SCHEME ps_month NEXT USED [PRIMARY];
ALTER PARTITION FUNCTION pf_month() SPLIT RANGE ('2026-12-01');   -- splits the empty end partition: instant
-- bulk load dbo.Sales_In; add the constraint(s) that ALTER TABLE ... SWITCH requires
ALTER TABLE dbo.Sales_In ADD CONSTRAINT ck_range CHECK (SaleDate >= '2026-11-01' AND SaleDate < '2026-12-01' AND SaleDate IS NOT NULL);
ALTER TABLE dbo.Sales_In SWITCH TO dbo.Sales PARTITION <n>;   -- partition number of the new month (see Inspect)
```

## Inspect
```sql
SELECT p.partition_number, prv.value AS lower_boundary, p.rows
FROM sys.partitions p
JOIN sys.indexes i ON i.object_id = p.object_id AND i.index_id = p.index_id
JOIN sys.partition_schemes ps ON ps.data_space_id = i.data_space_id
LEFT JOIN sys.partition_range_values prv ON prv.function_id = ps.function_id AND prv.boundary_id = p.partition_number - 1
WHERE p.object_id = OBJECT_ID('dbo.Sales') AND p.index_id = 1 ORDER BY p.partition_number;
```

## Gotchas
- Keep empty partitions at both ends so SPLIT and MERGE incur no data movement.
- With a columnstore index, only empty partitions can be split, and two nonempty partitions cannot be merged.
- Assign a NEXT USED filegroup before each SPLIT; after a split none is selected.
- Automate boundary creation ahead of time in an Agent job.

## Verify
After each cycle the row counts per partition match expectations and both end partitions are empty.

## Checked
2026-10-28. Confirmed against the partitioned tables and indexes, ALTER PARTITION FUNCTION, ALTER PARTITION SCHEME and TRUNCATE TABLE pages: manageability and performance benefits, aligned indexes (same partition scheme) allow fast switching, keep empty partitions at both ends so split and merge move no data, NEXT USED filegroup before a split, RANGE RIGHT, TRUNCATE TABLE WITH (PARTITIONS (...)), columnstore limits on split and merge, sys.partition_schemes and sys.partition_range_values.
Removed unconfirmed claims: "speeds queries only when they eliminate partitions", the SWITCH requirements list, schema-modification lock and WAIT_AT_LOW_PRIORITY on SWITCH, the 2016+ version gate, $PARTITION usage, hours-long split cost, uniqueness note, missing-boundary behaviour.
Method: documentation only; no commands were run.
