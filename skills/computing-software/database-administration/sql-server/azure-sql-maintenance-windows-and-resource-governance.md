---
id: computing-software.database-administration.sql-server.azure-sql-maintenance-windows-and-resource-governance
name: azure-sql-maintenance-windows-and-resource-governance
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, azure-sql, maintenance-window, log-rate-governance, resource-limits, worker-limits, advance-notifications, tempdb-limits]
level: advanced
status: docs-checked
description: "Configure Azure SQL maintenance windows and advance notifications, and work within resource governance limits: log rate, workers, sessions, tempdb and storage."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/maintenance-window
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/resource-limits-logical-server
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/resource-limits-vcore-single-databases
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure SQL maintenance windows and resource governance

## Maintenance window
Default: the system default window is 5pm to 8am. Choose instead:
- Weekday (10:00 PM to 6:00 AM local time, Mon-Thu) or Weekend (10:00 PM to 6:00 AM local time, Fri-Sun).
```bash
az sql db update -g <rg> -s <server> -n appdb --maint-config-id <config-id>   # id of the weekday or weekend configuration
az maintenance public-configuration list --query "[?contains(name,'WestEurope')].{name:name, window:maintenanceScope}" -o table
```
Advance notifications (up to 24 h ahead) are available for databases using a non-default window.
Not covered: urgent updates and hardware failures can still occur outside the window.
Applications still need retry logic.

## Governance: what limits you
Each service objective caps: CPU (vCores/DTUs), data IO, **log rate**, **workers** (concurrent
requests), **sessions**, tempdb size, max data size, and memory. Check live:
```sql
SELECT * FROM sys.dm_user_db_resource_governance WHERE database_id = DB_ID();
SELECT * FROM sys.dm_db_resource_stats ORDER BY end_time DESC;   -- utilisation vs those caps
```

## Log rate governance
Waits `LOG_RATE_GOVERNOR` (database cap) or `POOL_LOG_RATE_GOVERNOR` (elastic pool) during loads
and index maintenance. Fix: batch large modifications, load analytic data into a clustered
columnstore table, or scale up.
`INSTANCE_LOG_RATE_GOVERNOR` on Managed Instance is the instance-wide cap.

## Workers and sessions
Error 10928 "The request limit for the database is N and has been reached": too many concurrent
requests, often caused by blocking piling up requests. Fix blocking first, then reduce
concurrency or scale up. `max_worker_percent` in `sys.resource_stats` (query it in master) shows the trend.

## tempdb and storage
Per-objective tempdb max size; error 40544 when data hits max size: raise max size
(`ALTER DATABASE appdb MODIFY (MAXSIZE = 500 GB)`) within the tier's limit.

## Verify
Maintenance window set for production databases, Service Health alert routed to the team, and no
sustained 100% in any `sys.dm_db_resource_stats` column during business hours.

## Checked
2026-10-28. Confirmed against the maintenance-window and resource-limits-logical-server pages: system default window 5pm to 8am, Weekday (Mon-Thu) and Weekend (Fri-Sun) windows 10:00 PM to 6:00 AM local time, advance notifications up to 24 hours ahead for non-default windows, urgent updates and hardware failures can fall outside the window, LOG_RATE_GOVERNOR / POOL_LOG_RATE_GOVERNOR / INSTANCE_LOG_RATE_GOVERNOR wait types, error 10928, error 40544, sys.dm_user_db_resource_governance, max_worker_percent in sys.resource_stats, ALTER DATABASE ... MAXSIZE. The az commands passed check_commands.
Removed unconfirmed claims: the SQL_Default and SQL_WestEurope_DB_1 config names, the Managed Instance and elastic pool sentence, the gateway sentence, the sys.dm_user_db_resource_governance column list other than slo_name and the storage quota columns, TABLOCK/resumable-index/Hyperscale advice.
Method: documentation only; no commands were run.
