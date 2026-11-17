---
id: computing-software.cloud-infrastructure-engineering.azure.sql-failover-groups-and-geo-replication
name: sql-failover-groups-and-geo-replication
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-sql, sql-ha, failover-groups, auto-failover-groups, active-geo-replication, geo-replication, read-scale-out, listener-endpoint, read-write-listener, read-only-listener, grace-period, planned-failover, forced-failover, managed-instance-link, distributed-availability-group, hyperscale-geo-replica, named-replicas, zone-redundant, dr-drill, rpo, rto]
level: advanced
status: docs-checked
description: "Make Azure SQL survive a region: geo-replication vs auto-failover groups, listener endpoints, planned vs forced failover, grace periods, read scale-out and drills proving RTO/RPO."
sources: ["https://learn.microsoft.com/azure/azure-sql/database/active-geo-replication-overview", "https://learn.microsoft.com/azure/azure-sql/database/auto-failover-group-sql-db", "https://learn.microsoft.com/azure/azure-sql/database/auto-failover-group-configure-sql-db", "https://learn.microsoft.com/cli/azure/sql/failover-group"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL failover groups and geo-replication — a listener the app never has to change

**Goal:** the database tier fails over to the paired region with a stable connection
string, within the RPO/RTO the tier register promises, by a command you have run in
a drill — and reads scale out to replicas without touching the primary.

## 1. Options
| Mechanism | Scope | Endpoint | Failover |
|---|---|---|---|
| **Active geo-replication** (SQL DB only) | per database, up to 4 readable secondaries in any region | each secondary has its own server name — app must switch | manual (`az sql db replica set-primary`) |
| **Auto-failover group** (SQL DB + MI) | group of DBs on a server pair (MI: whole instance) | **listener** `<fog>.database.windows.net` (RW) and `<fog>.secondary.database.windows.net` (RO) via DNS CNAME | manual planned/forced, or **automatic** with a grace period |
| Zone redundancy | within region | same server | automatic |
Use failover groups for DR; add geo-replicas for extra read regions; zone redundancy regardless.

## 2. Build a failover group
```bash
az sql server create -g rg-dr -n sql-prod-ukw -l ukwest --enable-ad-only-auth --external-admin-principal-type Group --external-admin-name sg-sql-admins --external-admin-sid <oid>   # same admin/logins/firewall/private endpoint as primary
az sql failover-group create -g rg -s sql-prod-uks -n fog-orders --partner-server sql-prod-ukw --partner-resource-group rg-dr \
  --add-db orders --failover-policy Automatic --grace-period 1 --secondary-type Geo        # grace period in hours (minimum 1); Manual to keep the decision human
az sql failover-group show -g rg -s sql-prod-uks -n fog-orders --query "{role:replicationRole,state:replicationState}"
```
- Size the secondary at least as large as the primary so it can keep up.
- **Standby secondary** (`--secondary-type Standby`) is a passive replica for disaster recovery only; `Geo` secondaries are readable.
- Connection strings: `Server=tcp:fog-orders.database.windows.net,1433;` for writes; `fog-orders.secondary.database.windows.net` + `ApplicationIntent=ReadOnly` for read scale. The listener DNS record flips at failover with a 30-second TTL, so clients must not cache DNS longer.
- Server-level settings are not part of the group: replicate firewall/VNet rules, private endpoints (and their DNS records), Entra admin, logins, auditing and encryption key access to the partner server yourself.
- MI failover groups have their own skill (`sql-managed-instance-failover-groups`).

## 3. Failover semantics
- **Planned** (`az sql failover-group set-primary -g rg-dr -s sql-prod-ukw -n fog-orders`): waits for full sync — **no data loss**. Use for drills and migrations.
- **Forced** (`--allow-data-loss`): immediate, may lose unreplicated transactions (replication is asynchronous). Use when the primary region is gone.
- **Automatic policy**: triggers only after Microsoft detects the primary *unavailable* for the grace period (can't be set below one hour) — it is slow by design; a tight RTO needs your own detection and a forced failover decision.
- After failover the roles swap; **re-point nothing** if you used the listener; check replication resumes; fail back with another planned failover.
- Geo-replication link lag: `sys.dm_geo_replication_link_status` (`replication_lag_sec`, `last_replication`) on the primary; alert when lag exceeds your RPO.

## 4. Read scale-out
- Connections with `ApplicationIntent=ReadOnly` can be routed to a read replica where the database supports read scale-out (`az sql db create --read-scale Enabled`; Hyperscale uses `--ha-replicas`).
- Geo-secondaries also serve reads (cross-region latency; replication is asynchronous so data lags the primary).

## 5. Drill checklist (quarterly)
1. Announce; confirm lag ≈ 0.
2. Planned failover to secondary; measure time until app writes succeed through the listener.
3. Verify: app health, `replicationRole` = Primary on the new side, logs flowing to the DR region's Log Analytics, backups continuing (automated backups follow the primary).
4. Run in DR ≥ 1 h (finds the missing firewall rule, the private DNS record, the missing login).
5. Planned failback; record RTO/RPO; file the missed items.

## Gotchas
- Private endpoints: the listener CNAME resolves to the *current primary's* server — your private DNS zone needs A records for **both** servers or the secondary is unreachable after failover.
- Server-level firewall rules and Entra admin are not replicated — the #1 cause of "failover worked, app can't connect".
- Automatic failover waits at least one hour (the minimum grace period) before it can trigger — write that into the tier register, not just "automatic".

## Verify
- [ ] `az sql failover-group show` on both servers: roles Primary/Secondary, replication healthy; `sys.dm_geo_replication_link_status.replication_lag_sec` within RPO.
- [ ] `nslookup fog-orders.database.windows.net` → primary server; after a planned failover it resolves to the partner within the 30-second TTL.
- [ ] Drill log: planned failover + 1 h in DR + failback completed with app checks green; firewall/private DNS/logins verified on the secondary.
- [ ] Alert rule on replication lag and on *geo-replication link broken* exists and tested.

## Checked
2026-10-27. Confirmed on Microsoft Learn: auto-failover-group-sql-db (listener and `.secondary` endpoints, 30-second TTL, grace period not below one hour, ApplicationIntent),
active-geo-replication-overview (up to four, asynchronous), sys.dm_geo_replication_link_status columns, CLI reference for `az sql failover-group` (--add-db, --failover-policy, --grace-period,
--secondary-type Geo/Standby, --partner-server, --partner-resource-group, --allow-data-loss, set-primary), `az sql server` (Entra-only admin flags), `az sql db` (--read-scale, --ha-replicas).
Removed: MI link and Hyperscale table rows, RPO of 5 s, seconds-to-a-minute and under-60-s figures, licence-free standby claim, Java DNS cache property, TDE and SID guidance, named-replica
commands, tempdb statement, group-name uniqueness, tier-downgrade, MI subnet and elastic-pool gotchas, replicationState values.

Method: documentation only; no commands were run.
