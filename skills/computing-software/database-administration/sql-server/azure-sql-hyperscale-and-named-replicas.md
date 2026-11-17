---
id: computing-software.database-administration.sql-server.azure-sql-hyperscale-and-named-replicas
name: azure-sql-hyperscale-and-named-replicas
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, azure-sql, hyperscale-named-replica, hyperscale, page-servers, ha-replicas, read-scale-out, snapshot-backups]
level: advanced
status: docs-checked
description: "Understand Azure SQL Hyperscale architecture (compute, page servers, log service), add HA and named replicas for read scale-out, and plan migration and reverse migration."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/hyperscale-architecture
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/service-tier-hyperscale-replicas
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/manage-hyperscale-database
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure SQL Hyperscale and named replicas

## Architecture
- **Compute** nodes (primary + replicas) hold only a cache (RBPEX on local SSD); no data files.
- **Page servers** each own a slice of data pages (up to 128 TB total), with their own cache.
- **Log service** receives log from the primary and feeds page servers and replicas.
- **Azure storage** holds the data files; backups are storage **snapshots** (instant backup and fast restore regardless of size).
Consequences: the log generation rate is capped (see the resource-limits page for your service objective),
and a cold RBPEX cache means queries read from page servers.

## Replica types
| Type | Purpose | Notes |
|---|---|---|
| HA replica (0-4) | failover target and read scale-out | same name; connect with `ApplicationIntent=ReadOnly` |
| Named replica (up to 30) | isolated read workloads | own database name, optionally on a different logical server in the same region, own logins on that server |
| Geo replica | DR in another region | same as active geo-replication |

## Add a named replica
```bash
az sql db replica create -g <rg> -s <primary-server> -n appdb \
  --partner-server <replica-server> --partner-database appdb-reporting \
  --secondary-type Named --service-objective HS_Gen5_4
```
The replica can be on a different logical server (same region) with its own logins:
give report users access only there.

## Lag and consistency
Replicas replay log from the log service, so reads may be slightly behind the primary.

## Migration
- Reverse migration to General Purpose exists for databases recently converted to Hyperscale; check the manage-hyperscale-database page for the current window and limits.
- Serverless compute is available for Hyperscale (service objectives named `HS_S_Gen5_<vCores>`).

## Gotchas
- Log rate cap governs bulk loads and index rebuilds: check `avg_log_write_percent` in `sys.dm_db_resource_stats`.

## Verify
`SELECT DATABASEPROPERTYEX('appdb','Updateability')` returns READ_ONLY when connected to the named replica, and the reporting workload no longer shows in the primary's Query Store.

## Checked
2026-10-28. Confirmed against the Hyperscale architecture, replicas and service-objective pages: compute nodes with RBPEX cache, page servers with RBPEX, log service, up to 128 TB, up to 4 HA replicas, up to 30 named replicas, named replicas may sit on a different logical server in the same region with their own logins, ApplicationIntent=ReadOnly routing to HA replicas, snapshot-based backup and fast restore, reverse migration to General Purpose exists, serverless Hyperscale exists, DATABASEPROPERTYEX Updateability. The az sql db replica create command passed check_commands.
Removed unconfirmed claims: the 150 MB/s figure, the 45-day reverse-migration window, the T-SQL ADD SECONDARY option names, the redo-lag DMV query, the landing zone, the online-migration T-SQL, "named replicas are not failover targets", version cleanup gotcha, contained-user detail.
Method: documentation only; no commands were run.
