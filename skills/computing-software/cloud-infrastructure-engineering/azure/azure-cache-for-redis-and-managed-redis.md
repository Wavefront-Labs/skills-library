---
id: computing-software.cloud-infrastructure-engineering.azure.azure-cache-for-redis-and-managed-redis
name: azure-cache-for-redis-and-managed-redis
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-cache-for-redis, azure-managed-redis, redis, caching, cache-aside, redis-enterprise, redis-clustering, zone-redundancy, active-geo-replication, redis-persistence, rdb, aof, private-endpoint, entra-authentication-redis, access-keys, maxmemory-policy, eviction, connection-multiplexing, stackexchange-redis, redis-metrics, server-load, cache-sizing, session-state, rate-limiting]
level: practitioner
status: gated
description: "Run Redis on Azure: Managed Redis vs Cache for Redis, sizing by memory and Server Load, clustering, persistence, geo-replication, Entra auth, eviction, resilient clients."
sources: ["https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-how-to-scale", "https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-administration", "https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-failover", "https://learn.microsoft.com/en-us/cli/azure/redis"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Redis on Azure — the cache that doesn't become the outage

**Goal:** a Redis tier sized for memory *and* throughput, reached privately with
Entra identities, with persistence/geo-replication only where the data deserves it,
and clients that survive the failovers Azure performs for maintenance.

Note: Microsoft has announced a retirement timeline for all Azure Cache for Redis SKUs and recommends moving to Azure Managed Redis (see the retirement FAQ linked from the scaling article).

## 1. Offering and tier
| Offering | Tiers | Pick for |
|---|---|---|
| **Azure Managed Redis** (Redis Enterprise-based, the current direction) | Memory Optimized, Balanced, Compute Optimized, Flash Optimized; see the Managed Redis overview for sizes and modules | new deployments: clustering, zone redundancy, active geo-replication, persistence, Entra auth, higher throughput per GB |
| Azure Cache for Redis **Basic/Standard/Premium** (OSS Redis 6) | Basic no SLA; Standard replicated; Premium: clustering, persistence, VNet injection (legacy), zones | existing estates; Basic for dev |
| Azure Cache for Redis Enterprise/Enterprise Flash | being superseded by Managed Redis | |
```bash
az redisenterprise create -g rg -n redis-orders-prod -l uksouth --sku Balanced_B10 --high-availability Enabled --zones 1 2 3 \
  --public-network-access Disabled --minimum-tls-version 1.2
az redisenterprise database create -g rg --cluster-name redis-orders-prod --clustering-policy OSSCluster --eviction-policy VolatileLRU --port 10000 \
  --persistence aof-enabled=true aof-frequency=1s   # or rdb-enabled with rdb-frequency
az redis create -g rg -n redis-sessions -l uksouth --sku Premium --vm-size P1 --zones 1 2 --minimum-tls-version 1.2 --redis-configuration '{"maxmemory-policy":"allkeys-lru"}' --enable-non-ssl-port false
```
- Size by **memory with headroom** (fragmentation + replication buffers need the rest) and **Server Load** (Redis is single-threaded per shard, so scale out with clustering for CPU-bound workloads; pick your own alert thresholds). A `Balanced_B10` (12 GB) differs from `ComputeOptimized_X10` by vCPU per GB.
- Clustering policy: **OSS cluster** (client-side slot routing, best throughput, most clients support it) vs **Enterprise cluster** (proxy, single endpoint, for clients without cluster support; multi-key ops across slots).
- Zone redundancy and HA (replica per shard) on for production; Basic has one node = data loss on restart.

## 2. Network and auth
- Private endpoint (`privatelink.redis.cache.windows.net` / `privatelink.<region>.redisenterprise.cache.azure.net`); `--public-network-access Disabled`. VNet injection (Premium) is legacy — prefer private endpoints.
- **Entra authentication**: enable on the cache (`az redis identity`/access policy assignment: `az redis access-policy-assignment create --access-policy-name "Data Contributor" --object-id <mi-oid> --object-id-alias app-orders`), then the client uses a token as password (`Microsoft.Azure.StackExchangeRedis` extension `ConfigurationOptions.ConfigureForAzureWithTokenCredentialAsync`, `redis-py-entraid`). Disable access keys (`--disable-access-key-authentication true`) once migrated; keys rotate with `az redis regenerate-keys` otherwise.
- TLS 1.2 only, non-SSL port off; port 6380 (Cache for Redis) / 10000 (Managed Redis).

## 3. Data model and eviction
- `maxmemory-policy`: **`allkeys-lru`** for pure caches, **`volatile-lru`/`volatile-ttl`** when some keys must never be evicted (then every cache key gets a TTL), `noeviction` for queues/state (and alert on memory). Always set TTLs; a cache without TTLs is a database with worse durability.
- Key hygiene: namespaced keys (`orders:tenant:123:cart`), hash tags `{tenant123}` to co-locate keys that must be in one slot for multi-key ops/transactions; avoid `KEYS *` (use `SCAN`), avoid giant values and hot keys (one very hot key pins one shard).
- Patterns: cache-aside with jittered TTL (avoid stampedes), distributed lock (`SET NX PX`, Redlock only across independent instances), rate limiting (`INCR` + `EXPIRE` or sliding window with sorted sets), pub/sub for invalidation, streams for lightweight queues (prefer Service Bus for durability).

## 4. Persistence and geo-replication
- **Persistence** (Premium/Managed Redis): RDB snapshots (configurable interval) or AOF to managed storage — makes a full restart recover warm; it is **not** a backup you can restore to a point in time on demand (export/import for that: `az redis export --prefix ... --container <sas-url>`).
- **Active geo-replication** (Managed Redis / Enterprise): multi-master CRDT across regions — reads/writes local, conflict-free types; app uses the regional endpoint; for session state/global counters in multi-region apps. Premium *passive* geo-replication is one-way, manual failover, no writes on the secondary.
- Maintenance (Basic/Standard/Premium; no scheduled updates for Enterprise tiers): Azure patches nodes with a failover — pin it to a **maintenance window** (minimum five hours) (`az redis patch-schedule create --schedule-entries '[{"dayOfWeek":"Sunday","startHourUtc":2,"maintenanceWindow":"PT5H"}]'`) and expect a brief reconnect.

## 5. Client resilience (most "Redis outages" are client misconfiguration)
- One multiplexed connection per process (StackExchange.Redis `ConnectionMultiplexer` singleton; Lettuce; redis-py `ConnectionPool`), `abortConnect=false`, `connectRetry=3`, `connectTimeout=15000`, `syncTimeout` ≥ 1 000 ms (not 100), `ssl=true`, `keepAlive=60` (gated: unconfirmed, source is paywalled or blocked).
- Handle `RedisTimeoutException`/`RedisConnectionException` with retry + circuit breaker; cache misses on error (fail open), never block the request path on cache failures.
- Avoid large pipelines/batches on a busy shard; large `MGET` calls and `SMEMBERS` on huge sets are the usual timeout culprits — paginate with `SSCAN`.
- Thread-pool starvation (.NET `min threads`) shows as timeouts with low Server Load; set `ThreadPool.SetMinThreads` or use async.
- Reconnect logic after a failover: force-reconnect after N consecutive errors (Microsoft's `ForceReconnect` sample) — the multiplexer sometimes holds a dead socket for the TCP keepalive window.

## 6. Monitor
Metrics: `usedmemorypercentage` and `serverLoad` (alert on thresholds you choose), `connectedclients` vs limit, `cachemisses`/`cachehits` ratio, `evictedkeys` (should be ~0 on volatile policies), `errors` by type (`Failover`, `Dataloss`, `UnresponsiveClients`), `operationsPerSecond`; per-shard dimension on clustered caches. Diagnostic setting `ConnectedClientList` for who's connected. `redis-cli --tls -h <host> -p 6380 -a <token>` + `INFO`, `SLOWLOG GET`, `MEMORY DOCTOR`, `CLIENT LIST` for live triage.

## Gotchas
- Standard/Premium failover = the client's DNS resolves the same name; the TCP connection drops — clients that never retry see an outage and blame Azure.
- Basic tier in production: a single node and patching = data loss and downtime; it has no SLA.
- Memory full with `noeviction` → writes fail with OOM; with `allkeys-lru` → your "persistent" session store silently evicts users.
- Scaling Cache for Redis Premium (size or shard count) is online but cluster scaling runs MIGRATE, takes time that depends on key count and value size, and increases server load — do it off-peak; Managed Redis scales more gracefully.
- Entra tokens expire; clients must re-authenticate (the Azure client extensions do it); custom clients that cache the token get `WRONGPASS` after it expires.
- Export requires a storage account with firewall exceptions for the cache's identity/IPs; import overwrites the cache entirely.

## Verify
- [ ] `az redis show`/`az redisenterprise show` → private only, TLS 1.2, zones, HA; access-key auth disabled and an app connects with a managed identity token.
- [ ] Load test: `serverLoad` and `usedmemorypercentage` within your targets, p99 latency within your SLO from the same region; no `evictedkeys` growth on volatile policy.
- [ ] Planned failover (`az redis force-reboot --reboot-type PrimaryNode`) → app error rate stays flat; clients reconnect within seconds (log shows `ForceReconnect` or automatic).
- [ ] Maintenance window set; `Failover` error metric alert configured; `SLOWLOG` shows no slow commands in steady state.

## Checked

Date: 2026-11-02. Confirmed on Azure Cache for Redis pages in sources (scale, administration, failover) and the az redis CLI reference, and by check_commands: scaling, failover and patching behaviour, az redis flags, hash-tag co-location of keys. Removed as not stated there: 100 KB value size, 50k req/s hot key figure, 1000-key MGET and 1M-member SMEMBERS thresholds. Left, marked gated: the StackExchange.Redis connection-string values.

Method: documentation only; no commands were run.
