---
id: computing-software.database-administration.sql-server.azure-sql-monitoring-resource-stats-and-database-watcher
name: azure-sql-monitoring-resource-stats-and-database-watcher
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, azure-sql, dm-db-resource-stats, database-watcher, resource-stats, query-performance-insight, azure-monitor, monitoring]
level: practitioner
status: docs-checked
description: "Monitor Azure SQL Database and Managed Instance with sys.dm_db_resource_stats, sys.resource_stats and database watcher, and know each source's grain and retention."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/monitoring-with-dmvs
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-db-resource-stats-azure-sql-database
  - https://learn.microsoft.com/en-us/azure/azure-sql/database-watcher-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure SQL monitoring

## Am I hitting a limit? (recent, 15-second grain)
```sql
SELECT end_time, avg_cpu_percent, avg_data_io_percent, avg_log_write_percent,
       avg_memory_usage_percent, max_worker_percent, max_session_percent, avg_instance_cpu_percent
FROM sys.dm_db_resource_stats ORDER BY end_time DESC;
```
One row per 15 seconds, kept for about an hour. Percentages are of the database's service-tier
limits, so a column near 100 means that resource is the constraint.
If the database failed over in the last 60 minutes, the view only returns data since the failover.

Longer history (5-minute grain, about 14 days) from `master`:
`SELECT * FROM sys.resource_stats WHERE database_name = 'appdb' ORDER BY start_time DESC;`

## Other scopes
- Managed Instance does not support `sys.dm_db_resource_stats`; use `sys.server_resource_stats`.
- Elastic pools: `sys.dm_elastic_pool_resource_stats` (recent, query it from any database in the
  pool) and `sys.elastic_pool_resource_stats` (in `master`, last 14 days).

## Database watcher
A managed monitoring solution for Azure SQL Database and Azure SQL Managed Instance. It collects
data from more than 70 catalog views and DMVs into Azure Data Explorer or Real-Time Analytics
in Microsoft Fabric, where you query it with KQL or T-SQL. Workflow: create a watcher resource,
pick the data store and the SQL targets (databases, elastic pools, managed instances), grant the
watcher access to the targets, start it. Dashboards are Azure Workbooks; retention is set on the
data store. Each high-availability replica counts as its own target, and there is a per-watcher
target limit documented on the overview page. Alerts are not available when the data store is
Real-Time Analytics or a free Azure Data Explorer cluster.

## Gotchas
- `sys.dm_db_resource_stats` only holds about an hour; keep longer history in the watcher's store.
- Cost of the watcher's data store and alerts: see the vendor's pricing pages.

## Verify
Someone watches CPU, log write, worker and storage headroom, and the retention you need
(beyond 14 days) is stored somewhere.

## Checked
2026-11-01. Confirmed against the Learn pages `monitoring-with-dmvs`, `sys-dm-db-resource-stats-azure-sql-database`
and `database-watcher-overview`: 15-second grain and one-hour retention, failover note, `sys.resource_stats`
5-minute grain and 14 days, `sys.server_resource_stats` for Managed Instance, elastic pool views, watcher data stores,
70+ views, workflow, Azure Workbooks dashboards, alert limitation. Removed as unconfirmed: error 10928 detail, Query Store
and Query Performance Insight section, Azure Monitor metric names and the alert command, diagnostic log categories,
SQL Insights succession, watcher permission names, serverless pause behaviour.
Method: documentation only; no commands were run.
