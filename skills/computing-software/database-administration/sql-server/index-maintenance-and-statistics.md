---
id: computing-software.database-administration.sql-server.index-maintenance-and-statistics
name: index-maintenance-and-statistics
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, index-fragmentation, rebuild, reorganize, update-statistics, sys-dm-db-index-physical-stats, fillfactor]
level: advanced
status: docs-checked
description: "Decide whether SQL Server index maintenance is worth its cost, choose reorganize vs rebuild, and try statistics updates before rebuilding."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/reorganize-and-rebuild-indexes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server index maintenance and statistics

**Goal:** stop running blanket "rebuild everything" jobs; maintain only the indexes where measured data shows a benefit,
and use statistics updates where that is what actually helped.

## 1. Measure fragmentation and page density
For rowstore indexes `sys.dm_db_index_physical_stats()` returns `avg_fragmentation_in_percent` (logical fragmentation,
out-of-order pages) and `avg_page_space_used_in_percent` (page density); for partitioned indexes it reports per
partition. Low page density means more pages to read and cache and can change plan choice. In many workloads raising
page density helps more than reducing fragmentation.

Microsoft's current guidance is that maintenance decisions should consider the workload and the resource cost of the
maintenance, and should not rest on fixed fragmentation or page-density thresholds alone. Rebuilding or reorganizing
small rowstore indexes usually does not reduce fragmentation.

## 2. Reorganize vs rebuild
- **Reorganize** is less resource intensive and is the preferred method unless there is a reason to rebuild. It is
  always online, defragments only the leaf level of rowstore indexes, compacts pages to the index's fill factor, does
  not update statistics, and progress is kept if it is cancelled.
- **Rebuild** drops and re-creates the index, removes fragmentation at all levels and compacts pages to the specified
  or current fill factor. It can be offline (usually faster, holds object-level locks and blocks queries) or, depending
  on index type and version, online (a short lock at the end; modifications update an extra copy of the index, a minor
  slowdown) and possibly resumable. It needs space for two copies of the index while it runs. A higher `MAXDOP` can
  shorten it at the cost of CPU.
- Rebuild updates the index's statistics with the equivalent of `FULLSCAN`, except for partitioned or resumable
  rebuilds, which use the default sampling ratio.
- An index cannot be reorganized or rebuilt if its filegroup is offline or read-only.
- Columnstore: since SQL Server 2016 `REORGANIZE` does the essentials of a rebuild online, and since SQL Server 2019 a
  background merge task also compresses small delta row groups, so rebuilds are rarely needed.

## 3. Rebuild often "helps" by refreshing statistics
Improvement after a rebuild is often due to the full-scan statistics update and the plan recompile, not to less
fragmentation. Updating statistics costs far less (often minutes, where a rebuild can take hours). Try that first, and
raise the sample with `WITH SAMPLE ... PERCENT` or `WITH FULLSCAN` for statistics that need it (uncommon).
```sql
UPDATE STATISTICS <table_name> WITH FULLSCAN;
```

## 4. Microsoft's recommended strategy
1. Do not assume maintenance noticeably improves your workload; measure before and after (Query Store A/B testing).
2. If rebuilding helps, test replacing it with statistics updates.
3. Monitor fragmentation and page density over time against query performance; maintain only the indexes behind
   degraded queries, as needed rather than on a fixed schedule.
4. Run needed maintenance at low-usage times and retest periodically.

## 5. Azure SQL Database and Managed Instance
Resource governance bounds apply to maintenance too; a rebuild can slow other workloads (for example log I/O at 100%
slows bulk loads), elastic pool neighbours are affected, and geo-replica or read-scale replicas can lag or be
reseeded. On Managed Instance a restricted resource governor workload group can limit the impact. For most Azure SQL
storage, sequential and random I/O perform alike, which reduces the impact of fragmentation.

## Verify
- [ ] Jobs target specific indexes with measured benefit, not every index on a schedule.
- [ ] A regressed query was checked for stale statistics before assuming an index problem.
- [ ] Online or resumable rebuild availability was confirmed for your version before scheduling in business hours.

## Checked
Date: 2026-11-09. Confirmed against the Learn page "Optimize index maintenance to improve query performance and reduce
resource consumption": DMV columns, no-fixed-threshold guidance, reorganize and rebuild behaviour, statistics side
effects, columnstore notes, strategy list, Azure considerations. Removed (not stated on that page): Ola Hallengren
references, 5-30% and 1000-page thresholds, Standard-edition online rebuild claim, auto-update statistics thresholds,
trace flag 2371, `AUTO_UPDATE_STATISTICS_ASYNC` advice, `STATS_DATE` and `dm_db_stats_properties` query, ascending-key
discussion.
Method: documentation only; no commands were run.
