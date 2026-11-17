---
id: computing-software.database-administration.sql-server.azure-sql-failover-groups-and-geo-replication
name: azure-sql-failover-groups-and-geo-replication
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, azure-sql, azure-sql-database, azure-sql-managed-instance, auto-failover-group, active-geo-replication, geo-secondary, failover-policy, grace-period, listener-endpoint, disaster-recovery]
level: advanced
status: docs-checked
description: "Protect Azure SQL Database and Managed Instance with active geo-replication or failover groups: listener endpoints, failover policy, planned vs forced failover."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/active-geo-replication-overview
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/failover-group-sql-db
  - https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/failover-group-sql-mi
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure SQL failover groups and active geo-replication

## Active geo-replication (Azure SQL Database only)
Per-database async replica on another logical server (up to 4
secondaries, readable). Failover is per database and the connection string changes
(you connect to the other server).
```bash
az sql db replica create -g rg -s prod-srv -n appdb --partner-server dr-srv --partner-resource-group rg-dr
az sql db replica set-primary -g rg-dr -s dr-srv -n appdb                     # planned, no data loss
az sql db replica set-primary -g rg-dr -s dr-srv -n appdb --allow-data-loss   # forced
```

## Failover groups (SQL Database and Managed Instance)
Group of databases (or all databases of an MI) with **stable listener endpoints**:
- read-write: `<fog-name>.database.windows.net` (MI: `<fog-name>.<dns-zone>.database.windows.net`)
- read-only: `<fog-name>.secondary.database.windows.net`
After failover the DNS names point to the new primary; apps need no change.
```bash
az sql failover-group create -g rg -s prod-srv -n fog-app --partner-server dr-srv \
  --add-db appdb ordersdb --failover-policy Automatic --grace-period 1   # hours
az sql failover-group set-primary -g rg-dr -s dr-srv -n fog-app                     # planned
az sql failover-group set-primary -g rg-dr -s dr-srv -n fog-app --allow-data-loss   # forced
```
MI: `az sql instance-failover-group create` with `--mi` / `--partner-mi`; MI pairs need VNet connectivity (global peering) and the
secondary MI created in the same DNS zone as the primary.

## Failover policy
- **Customer-managed (recommended by Microsoft)**: you decide when to fail over, after
  judging the outage. Automate with your own runbook.
- **Microsoft-managed (Automatic)** with a grace period (min 1 hour): Azure fails over
  only for wide regional outages after the grace period; data loss possible. Not a
  fast-failover mechanism for single-database issues.

## What replicates and what does not
- Data: async. Check lag: `SELECT partner_server, replication_state_desc, replication_lag_sec, last_replication FROM sys.dm_geo_replication_link_status;` (on primary).
- Not replicated: the secondary's PITR retention setting (default 7 days) is not part of
  the database; on Managed Instance, system databases such as master and msdb are not
  replicated, so create the same objects on the secondary. Keep logins, firewall rules and
  private endpoints in sync on both sides (for example in IaC).
- Size the secondary at the same service tier and compute; an undersized secondary
  throttles log replication and the primary (`HADR_THROTTLE_LOG_RATE_MISMATCHED_SLO`).

## Guaranteeing no loss for critical transactions
`EXEC sys.sp_wait_for_database_copy_sync @target_server = N'dr-srv', @target_database = N'appdb';`
after a commit blocks until it reached the secondary.

## Verify
- [ ] Apps use the failover group listener names, not server names.
- [ ] Logins/users work on the secondary (contained users or same SIDs).
- [ ] Planned failover drill done and timed; `replication_lag_sec` monitored.

## Checked
2026-10-28. Confirmed against the active-geo-replication, failover-group-sql-db and failover-group-sql-mi pages: up to four geo-secondaries, listener names <fog-name>.database.windows.net and <fog-name>.secondary.database.windows.net, grace period cannot be below one hour, Microsoft-managed failover only for extreme circumstances and customer-managed policy highly recommended, replication_lag_sec in sys.dm_geo_replication_link_status, HADR_THROTTLE_LOG_RATE_MISMATCHED_SLO for an undersized secondary, sys.sp_wait_for_database_copy_sync, MI secondaries in the same DNS zone, global VNet peering recommended for MI. The az commands passed check_commands.
Removed unconfirmed claims: "any region", the list of unreplicated server-level items (logins, firewall rules, Entra admin, elastic job agents), the same-SID login advice as a documented fact.
Method: documentation only; no commands were run.
