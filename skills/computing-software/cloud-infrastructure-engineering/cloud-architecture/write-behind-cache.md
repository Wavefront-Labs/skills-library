---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.write-behind-cache
name: write-behind-cache
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-patterns, write-behind-cache, write-through-cache, caching-strategy, redis, durability]
level: practitioner
status: draft
description: "Choose and implement write-through or write-behind caching: consistency and durability trade-offs, coalescing writes, failure recovery, and when cache-aside is safer."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html", "https://redis.io/learn/howtos/solutions/caching-architecture/write-behind", "https://redis.io/learn/howtos/solutions/caching-architecture/write-through", "https://learn.microsoft.com/azure/architecture/patterns/cache-aside"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Write-through and write-behind caching

## Options
- **Write-through**: the write goes to the cache and synchronously to the database before
  acknowledging. Reads are always warm and consistent; writes pay both latencies.
- **Write-behind (write-back)**: the write is acknowledged once in the cache; a background
  process flushes to the database asynchronously, often batched. Very fast writes and write
  coalescing, at the cost of a durability window.
- **Cache-aside**: application writes the database and invalidates the cache. Simplest and the
  default when unsure.

## Steps
1. **Decide by data criticality.** Write-behind only for data where losing the last seconds is
   acceptable or the cache itself is durable (Redis AOF `appendfsync everysec` plus replicas,
   MemoryDB with multi-AZ transaction log). Financial or order data: write-through or
   database-first.
2. **Implement write-through** in a data-access layer or with tooling (Redis Gears/RedisGears
   write-through recipes, Hazelcast/Ignite MapStore, NCache). Order: database first, then cache,
   so a failed DB write never leaves phantom data in cache.
3. **Implement write-behind** with a durable queue between cache and DB: write to cache plus a
   stream (Redis Streams, Kafka) and have workers upsert to the DB in batches. Use idempotent
   upserts keyed by entity ID plus version to tolerate replays.
4. **Coalesce**: keep only the latest version per key within a flush interval to cut DB load
   for hot counters and session state.
5. **Recovery**: on cache node loss, replay the stream from the last committed offset; monitor
   flush lag and alert when it exceeds the acceptable loss window.
6. **Expiry**: never evict dirty entries before flush; use `noeviction` or separate dirty tracking.

## Gotchas
- Other services reading the database directly see stale data under write-behind.
- Write-through doubles write latency and fails if either store is down; define behaviour.
- Cache eviction policies such as `allkeys-lru` can drop unflushed writes.

## Verify
- [ ] Kill a cache primary during load: no acknowledged writes lost beyond the agreed window.
- [ ] Flush lag metric with alert threshold.
