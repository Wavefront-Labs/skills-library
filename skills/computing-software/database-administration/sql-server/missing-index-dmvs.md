---
id: computing-software.database-administration.sql-server.missing-index-dmvs
name: missing-index-dmvs
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, missing-index-dmv, sys-dm-db-missing-index-details, index-design, index-usage-stats, unused-indexes, sp-blitzindex, execution-plan]
level: practitioner
status: docs-checked
description: "Read SQL Server missing index DMVs critically, consolidate suggestions into a few good indexes, and remove unused indexes using index usage stats."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/tune-nonclustered-missing-index-suggestions
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-db-missing-index-details-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Missing index DMVs

**Goal:** turn the optimizer's index wishes into a small set of indexes that help,
without the "create every suggestion" index sprawl that slows writes.

## Query the suggestions
```sql
SELECT TOP 25
  ROUND(s.avg_total_user_cost * s.avg_user_impact * (s.user_seeks + s.user_scans), 0) AS score,
  d.statement AS table_name, d.equality_columns, d.inequality_columns, d.included_columns,
  s.user_seeks, s.user_scans, s.last_user_seek, s.avg_user_impact
FROM sys.dm_db_missing_index_groups g
JOIN sys.dm_db_missing_index_group_stats s ON s.group_handle = g.index_group_handle
JOIN sys.dm_db_missing_index_details d ON d.index_handle = g.index_handle
WHERE d.database_id = DB_ID()
ORDER BY score DESC;
```
`sys.dm_db_missing_index_group_stats_query` shows which queries asked for a suggestion.
Suggestions are cleared by restarts, failovers and taking a database offline, and when the table's metadata changes; at most 600 missing index groups are gathered.

## Read them critically
- The DMV output is a suggestion, not a finished index design: decide key order yourself.
- Prefer widening an existing index over adding a near-duplicate.
- Several suggestions on one table can often be combined into one index.
- Read the Tune nonclustered indexes with missing index suggestions page before creating them.

## Build
```sql
CREATE NONCLUSTERED INDEX ix_orders_customer_date
  ON dbo.orders (customer_id, order_date) INCLUDE (status, amount)
;
```
Check the actual plan of the triggering queries before and after (logical reads,
the seek replacing the scan).


## Verify
- [ ] Each new index maps to named queries whose reads dropped.
- [ ] No new index duplicates the leading keys of an existing one.

## Checked

2026-10-28. Confirmed against Microsoft Learn (Tune nonclustered indexes with missing index suggestions, sys.dm_db_missing_index_details): the improvement formula avg_total_user_cost * avg_user_impact * (user_seeks + user_scans), included_columns meaning, 600 missing index group cap, suggestions cleared by restart, failover, offline and table metadata changes, sys.dm_db_missing_index_group_stats_query exists. Removed unconfirmed: the 2019+ tag, key-order and filtered/columnstore claims, ONLINE and compression options, the unused-index query and thresholds, sp_BlitzIndex advice.

Method: documentation only; no commands were run.
