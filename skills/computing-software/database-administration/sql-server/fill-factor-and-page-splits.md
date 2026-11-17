---
id: computing-software.database-administration.sql-server.fill-factor-and-page-splits
name: fill-factor-and-page-splits
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, index-fragmentation, fill-factor, page-splits, index-design]
level: practitioner
status: docs-checked
description: "Leave SQL Server fill factor at the default and lower it only for indexes with measured mid-index page splits, rebuilding with a value in the 70-95 range."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/specify-fill-factor-for-an-index
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/reorganize-and-rebuild-indexes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fill factor and page splits

## What fill factor does
When an index is created or rebuilt, the fill factor (1 to 100, server-wide default 0, which behaves the same as 100)
sets the percentage of each **leaf-level** page filled with data. `FILLFACTOR = 80` leaves 20% of each leaf page empty,
reserved on every page rather than at the end of the index.

A page split happens when a row is added to a full index page: the Database Engine moves roughly half the rows to a
new page. Mid-index it is a resource-intensive operation and can fragment the index, which reduces read-ahead
effectiveness in large scans. The cost of a lower fill factor: more storage, memory and disk I/O to read and cache the
same data (a fill factor of 50 doubles the I/O and memory needed).

## Microsoft's guidance
- Most workloads perform best at the default (100).
- Microsoft does not recommend values other than 100 or 0, except for indexes with a high number of page splits, for
  example frequently modified indexes whose leading column holds nonsequential GUID values.
- If page splits hurt, rebuild with a new or existing fill factor in the 70-95 range; do not reduce it unnecessarily.
- A lower fill factor only helps when new rows land throughout the index. For an ever-increasing key such as an
  `IDENTITY` column, rows are added at the end and the empty space may never be filled.
- In many workloads, higher page density helps performance more than reducing fragmentation.

## Apply per index
```sql
ALTER INDEX IX_Employee_OrganizationLevel_OrganizationNode ON HumanResources.Employee
REBUILD WITH (FILLFACTOR = 80);
SELECT name, fill_factor FROM sys.indexes WHERE object_id = OBJECT_ID('HumanResources.Employee');
```
`CREATE INDEX ... WITH (DROP_EXISTING = ON, FILLFACTOR = 80)` also works. A rebuild or reorganize compacts pages to the
index's fill factor, so the setting persists with the index. Requires ALTER permission on the table.

## Measure
`sys.dm_db_index_physical_stats` returns `avg_fragmentation_in_percent` (logical fragmentation) and
`avg_page_space_used_in_percent` (page density). Low density means more pages to read and cache and can change query
plan choice, so judge both numbers, not fragmentation alone.

## Verify
After rebuilding, density is close to the chosen fill factor and the page splits you were chasing no longer occur
mid-index, without a large drop in `avg_page_space_used_in_percent` on the rest of the table's indexes.

## Checked
Date: 2026-11-09. Confirmed against the Learn pages "Specify fill factor for an index" and "Optimize index
maintenance to improve query performance and reduce resource consumption": fill factor range and default, leaf-level
meaning, page-split behaviour, 70-95 range, GUID example, identity example, 50 doubles I/O, DMV columns. Removed
(not stated on the cited pages): per-key-pattern value table, `PAD_INDEX` note, `sp_configure` advice, perfmon counter
and the Extended Events bad-split session, SSD remark.
Method: documentation only; no commands were run.
