---
id: computing-software.database-administration.sql-server.azure-sql-purchasing-models-and-service-tiers
name: azure-sql-purchasing-models-and-service-tiers
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, azure-sql, azure-sql-database, azure-sql-managed-instance, vcore-dtu, service-tier, hyperscale, serverless, elastic-pool, business-critical]
level: practitioner
status: draft
description: "Choose an Azure SQL deployment and tier (SQL Database vs Managed Instance; DTU vs vCore; General Purpose, Business Critical, Hyperscale, serverless, elastic pools)."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/purchasing-models
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/service-tiers-sql-database-vcore
  - https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/sql-managed-instance-paas-overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Azure SQL deployment and service tiers

**Goal:** the right product and tier for the workload's features, latency and
cost, chosen with numbers rather than by default.

## Product
| Option | When |
|---|---|
| Azure SQL Database (single / elastic pool) | New cloud apps; database-scoped features; no cross-DB queries, no Agent (use elastic jobs) |
| Azure SQL Managed Instance | Lift-and-shift needing instance features: SQL Agent, cross-database queries, CLR, Service Broker, linked servers, native backup restore |
| SQL Server on Azure VM | Full control, OS access, unsupported features (SSRS/SSAS on box, specific versions) |

## Purchasing model
- **DTU** (Basic/Standard/Premium): bundled CPU+IO+memory units; simple, small DBs.
- **vCore**: choose cores, hardware generation, storage separately; Azure Hybrid
  Benefit (bring licenses) and reserved capacity apply. Default for anything serious.

## vCore tiers
| Tier | Storage / HA | Notes |
|---|---|---|
| General Purpose | Remote premium storage; HA by restarting compute elsewhere | Cheapest; IO latency ~5-10 ms; failover tens of seconds |
| Business Critical | Local SSD + 3 replicas (Always On) | Low latency, free readable secondary (`ApplicationIntent=ReadOnly`), In-Memory OLTP |
| Hyperscale | Distributed page servers, up to 128 TB | Fast scale, near-instant snapshot backups, named replicas; reverse migration limited |
**Serverless** (GP and Hyperscale): auto-scales vCores between min/max and can
auto-pause (GP) after idle delay: great for dev/intermittent use, cold-start
latency on resume. **Elastic pools**: many DBs sharing a vCore budget for
spiky multi-tenant SaaS.

## Sizing from data
Before migrating, capture CPU, IO (IOPS, MB/s, latency), memory and log
generation rate from the source (perfmon or the Data Migration Assistant SKU
recommender / Azure Migrate). Check the tier's limits: max log rate (MB/s) and
IOPS per vCore often cap General Purpose before CPU does.

## Gotchas
- Log rate governance (`LOG_RATE_GOVERNOR` waits) throttles bulk loads on lower tiers.
- tempdb size is tied to vCores.
- Changing tier is online but ends with a brief disconnect; apps need retry logic
  (transient errors 40613, 40501, 49918).

## Verify
```sql
SELECT DATABASEPROPERTYEX(DB_NAME(), 'Edition'), DATABASEPROPERTYEX(DB_NAME(), 'ServiceObjective');
SELECT TOP 20 * FROM sys.dm_db_resource_stats ORDER BY end_time DESC;   -- avg_cpu/io/log percent of tier limit
```
Sustained >80% of any limit = wrong tier or tuning needed.
