---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.distributed-cache
name: distributed-cache
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, caching-strategy, distributed-cache, redis, valkey, memcached, elasticache, azure-cache-for-redis, memorystore, eviction-policy]
level: practitioner
status: draft
description: "Design an in-memory distributed cache cluster: Redis/Valkey vs Memcached, cluster mode and sharding, HA and failover, eviction, sizing, and client behaviour."
sources: ["https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html", "https://learn.microsoft.com/azure/azure-cache-for-redis/cache-best-practices-development"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# In-memory distributed cache design

## Engine choice
- **Redis / Valkey**: data structures, replication, persistence options, pub/sub, Lua, cluster mode.
- **Memcached**: simple multithreaded key-value, no replication; client-side sharding.

## Design
1. **Topology**: cluster mode (hash slots 0-16383 across shards) for > one node's memory or
   throughput; replicas per shard across zones; automatic failover.
2. **Sizing**: dataset x overhead (~1.3-1.5x for Redis), plus headroom for replication buffers and
   forks (BGSAVE needs memory with persistence on); keep memory < ~75% used.
3. **Eviction**: `maxmemory-policy allkeys-lru` (or `allkeys-lfu`) for pure caches; `volatile-*`
   only if non-expiring keys must survive; `noeviction` makes writes fail when full.
4. **TTLs** on every cache key, with jitter to avoid synchronised expiry.
5. **Keys**: namespaced (`svc:v2:user:123`), version prefix to invalidate on schema change; avoid
   big keys (> 1 MB) and hot keys; in cluster mode use hash tags `{user123}` only when multi-key ops needed.
6. **Clients**: connection pooling, timeouts (tens of ms), cluster-aware clients, retry on MOVED/failover.
7. **Security**: TLS, AUTH/ACLs, private network only.

## Gotchas
- Treating the cache as a database (no persistence guarantees by default).
- `KEYS *` in production blocks the server; use `SCAN`.
- Failover drops in-flight writes; app must tolerate cache misses.

## Verify
- [ ] Failover test: app continues with elevated latency, no errors.
- [ ] Hit ratio, evictions and memory dashboards with alerts.
