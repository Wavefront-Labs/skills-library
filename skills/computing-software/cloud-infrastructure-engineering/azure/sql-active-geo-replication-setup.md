---
id: computing-software.cloud-infrastructure-engineering.azure.sql-active-geo-replication-setup
name: sql-active-geo-replication-setup
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-sql, sql-ha, active-geo-replication, geo-replication-setup, geo-secondary, readable-secondary, set-primary, forced-failover, replication-lag, dm-geo-replication-link-status]
level: advanced
status: docs-checked
description: "Set up Azure SQL Database active geo-replication: create readable geo-secondaries, size and secure them, monitor lag, planned and forced failover, and when to use failover groups."
sources: ["https://learn.microsoft.com/en-us/azure/azure-sql/database/active-geo-replication-overview", "https://learn.microsoft.com/en-us/azure/azure-sql/database/active-geo-replication-configure-portal", "https://learn.microsoft.com/en-us/cli/azure/sql/db/replica", "https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-geo-replication-link-status-azure-sql-database"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active geo-replication for Azure SQL Database

**Goal:** a continuously replicated, readable copy of a database in another region (up to four
per primary) for DR or read offload, with failover you have rehearsed.

## 1. When geo-replication (vs failover group)
- Use **active geo-replication** for per-database control, multiple secondaries, or migrations between regions/servers.
- Use a **failover group** when apps need a stable listener name and group failover —
  failover groups are built on geo-replication but add DNS endpoints and automatic policy.

## 2. Create
```bash
az sql db replica create -g rg-uks -s sql-prod-uks -n orders \
  --partner-resource-group rg-ukw --partner-server sql-prod-ukw \
  --service-objective GP_Gen5_8 --backup-storage-redundancy Zone
az sql db replica list-links -g rg-uks -s sql-prod-uks -n orders -o table
```
- Partner server must exist first, with its own Entra admin, firewall or private endpoint rules and auditing configured.
- Size the secondary at least as large as the primary so it can keep up with the primary's log.
- After creation the secondary is seeded; `replication_state_desc` moves through `PENDING`, `SEEDING` and `CATCH_UP`.
- Logins are not copied with the database: create them on the partner server or use contained or Entra users.

## 3. Monitor
```sql
-- on the primary
SELECT partner_server, partner_database, replication_state_desc, role_desc, replication_lag_sec, last_replication
FROM sys.dm_geo_replication_link_status;
```
Alert when `replication_lag_sec` exceeds your RPO. Geo-replication is asynchronous; use `sp_wait_for_database_copy_sync` after critical transactions if you need them on the secondary before acking.

## 4. Failover
```bash
az sql db replica set-primary -g rg-ukw -s sql-prod-ukw -n orders                       # planned: syncs first, no data loss
az sql db replica set-primary -g rg-ukw -s sql-prod-ukw -n orders --allow-data-loss      # forced: primary unreachable
az sql db replica delete-link -g rg-uks -s sql-prod-uks -n orders --partner-server sql-prod-ukw   # break the link
```
Run on the **secondary's** server. Apps must switch connection strings (no listener) — store
the active server name in App Configuration or use a failover group.

## Gotchas
- Secondary is read-only; connect with `ApplicationIntent=ReadOnly` to its own server name.
- Hyperscale has its own geo-replica article with Hyperscale-specific behaviour; check it before using this skill's commands there.
- Elastic pools: a secondary can be placed in a pool on the partner server (`--elastic-pool`).

## Verify
- [ ] `list-links` shows the link healthy and `replication_lag_sec` within RPO under normal load.
- [ ] App identity can log in to the secondary (contained/Entra or same-SID login).
- [ ] A planned `set-primary` drill completes and the app reconnects after the connection-string switch; switched back afterwards.

## Checked
2026-10-27. Confirmed on Microsoft Learn: active-geo-replication-overview (up to four, asynchronous, user-controlled failover, `sp_wait_for_database_copy_sync`),
sys.dm_geo_replication_link_status (partner_server, partner_database, replication_state_desc PENDING/SEEDING/CATCH_UP/SUSPENDED, role_desc, replication_lag_sec, last_replication),
CLI reference for `az sql db replica` (create, list-links, set-primary, delete-link, --partner-server, --partner-resource-group, --service-objective, --backup-storage-redundancy, --allow-data-loss, --elastic-pool).
Removed: chained replicas, `--secondary-type Geo` in the example, TDE key and same-SID login guidance, log-throttle rationale, Azure Monitor metric name and 30 s alert figure,
scaling-order rule, standalone-RW claim, Hyperscale `--secondary-type` claim.

Method: documentation only; no commands were run.
