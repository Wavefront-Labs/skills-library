---
id: computing-software.cloud-infrastructure-engineering.azure.redis-cache-scaling-reboot-and-maintenance
name: redis-cache-scaling-reboot-and-maintenance
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-cache-for-redis, azure-managed-redis, redis-scaling, redis-reboot, redis-maintenance, scale-up, scale-out, shard-count, patch-schedule, maintenance-window, failover, connection-blips]
level: practitioner
status: docs-checked
description: "Scale Azure Cache for Redis up/out (tiers, shards, replicas), schedule patching, reboot nodes safely, and keep clients alive through the failovers these trigger."
sources: ["https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-how-to-scale", "https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-administration", "https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-failover", "https://learn.microsoft.com/en-us/cli/azure/redis"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Redis on Azure — scaling, reboot and maintenance

**Goal:** change cache size or throughput without an outage, and make planned maintenance
and reboots non-events for the applications.

Note: Microsoft has announced a retirement timeline for all Azure Cache for Redis SKUs and recommends moving to Azure Managed Redis; check the retirement FAQ before investing in a new Cache for Redis estate.

## 1. Decide what to scale
| Symptom (metric) | Action |
|---|---|
| `Used Memory %` high, evictions | scale **up** (bigger size) or **out** (more shards, Premium/Managed Redis) |
| High `Server Load` (Redis is single-threaded) | scale **out** with clustering (spreads keys and TLS work); scaling up also helps by freeing the main thread for background tasks |
| `Connected Clients` near limit | scale up (limit grows with size) — but first fix connection leaks |
| Network bandwidth near size limit | scale up/out |

## 2. Do it
```bash
az redis update -g rg-cache -n redis-prod --sku Premium --vm-size P2          # scale up / tier change Basic→Standard→Premium
az redis update -g rg-cache -n redis-prod --set shardCount=3                  # scale out (Premium clustering; enable clustering first, it cannot be undone)
# Azure Managed Redis uses `az redisenterprise` (see its CLI reference)
```
- Expect connection drops while scaling; test client reconnect behaviour first.
- Can't scale to a lower tier (Premium to Standard/Basic, Standard to Basic); Basic cannot go straight to Premium (Basic to Standard first, with no size change in the same step); you can't scale into C0 from a larger size.
- Scale out/in: Premium and Enterprise tiers can scale out, only Premium can scale in; enterprise tiers cannot scale down. On Premium, clustering must be enabled first before scaling in or out (enabling it cannot be undone), and clients must be cluster-aware (only database 0, multi-key commands need keys in one shard). Extra replicas per primary, zone redundancy and VNet injection cannot be added by scaling; create a new Premium cache.
- Scaling a Basic cache to a different size shuts it down and loses its data; Standard/Premium stay available but connection blips occur. Scaling down can evict keys if data exceeds the new size.
- Cluster scaling runs MIGRATE, which is expensive; time depends on the number of keys and value sizes.

## 3. Maintenance and reboot
```bash
az redis patch-schedule create -g rg-cache -n redis-prod --schedule-entries '[{"dayOfWeek":"Sunday","startHourUtc":2,"maintenanceWindow":"PT5H"}]'   # Basic/Standard/Premium only; no scheduled updates for Enterprise tiers
az redis force-reboot -g rg-cache -n redis-prod --reboot-type PrimaryNode       # PrimaryNode | SecondaryNode | AllNodes (; --shard-id for clusters)
```
- Patch schedule keeps Redis server updates in your window (Azure host updates can still occur outside it).
- Reboot to test client resilience (do it in non-prod regularly) or to recover a stuck node.
  Any reboot can lose in-flight writes; rebooting both nodes (`AllNodes`) raises the odds of data loss, so treat it as destructive for non-persisted caches.
- Subscribe to the `AzureRedisEvents` pub/sub channel in clients (Basic/Standard/Premium only; notice comes about 15 minutes before maintenance) to drain before failover.
- Reboot is not available for Enterprise tiers.

## 4. Client resilience checklist
- Configure client connection retry and timeouts per your client library's guidance, and retry with backoff on connection exceptions and timeouts.
- Reuse one connection per process; reconnect logic that recreates it after prolonged failure.
- Keep timeouts generous and retry with backoff so a failover doesn't cascade into a retry storm.

## Gotchas
- Scaling during peak plus failovers = cold cache misses hammering the database; schedule off-peak.

## Verify
- [ ] Post-scale: `az redis show --query "{sku:sku.name,size:sku.capacity,shards:shardCount}"` shows the target; memory and server load back at healthy levels.
- [ ] Patch schedule present; a non-prod `force-reboot PrimaryNode` produces only short errors in app logs and full recovery.
- [ ] Alerts exist on Server Load, Used Memory %, and evictions.

## Checked
Date: 2026-10-31. Checked against Microsoft Learn: Scale an Azure Cache for Redis instance, Administration (reboot, scheduled updates), Failover and patching, and the `az redis` CLI reference.
- Confirmed: tier scale up/down/out/in matrix and restrictions (including C0 and Basic to Premium), clustering first, MIGRATE cost, scale-up helping server load, `az redis update --set shardCount`, `--vm-size`, `force-reboot` types and `--shard-id`, five-hour minimum maintenance window, scheduled updates only on Basic/Standard/Premium, Azure/host updates outside the window, `AzureRedisEvents` (Basic/Standard/Premium, 15 minutes), Enterprise reboot unavailable, retirement note.
- Removed as unconfirmed: `replicasPerPrimary` update command, claim that clustering is only set at creation (it can be enabled later), `abortConnect`/`connectRetry`/`connectTimeout` values, StackExchange.Redis maintenance-event claim.
Method: documentation only; no commands were run.
