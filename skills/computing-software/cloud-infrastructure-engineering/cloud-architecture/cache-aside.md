---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cache-aside
name: cache-aside
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-patterns, caching-strategy, cache-aside, lazy-loading, ttl, cache-down, azure-managed-redis, elasticache]
level: practitioner
status: docs-checked
description: "Implement cache-aside: load on miss, update the store then invalidate on write, TTL and eviction choices, staleness limits, and what happens when the cache is down."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/cache-aside", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cache-aside

The application owns the cache (Amazon ElastiCache calls this lazy loading): on read, check the cache; on a miss load from the data store and populate the cache; on write, update the data store then invalidate the cached item.

## Implementation
```text
get(k):  v = cache.get(k); if v: return v
         v = db.load(k); if v: cache.set(k, v, ttl); return v
put(k,v): db.write(k, v); cache.delete(k)
```
- **Update the store first, then delete the cache entry.** If you remove the cached item first, a client can fetch the item before the store is updated, miss, read the outdated item from the store and add it back, leaving stale data in the cache.
- **Delete rather than set on write**: the pattern invalidates on write and repopulates on the next read. Between the write and the next read a reader can see a miss or briefly stale data; the pattern does not guarantee consistency, because an external process can change the store at any time and the change shows only after the item reloads. If read-heavy paths need read-after-write freshness, consider write-through caching.
- **Give entries a TTL.** A TTL does not guarantee a value is not stale, but keeps data from getting too stale. Do not make it so short that premature expiry has the application continually reloading, nor so long that data goes stale; match it to access patterns. Caching works best for relatively static or frequently read data.
- **Avoid caching a null result** as the Azure example does (it skips caching when the store returns nothing).
- **Eviction**: caches have a limited size and evict when full; most use least-recently-used, some allow customising. Expensive-to-retrieve items can be configured individually.
- **Priming**: many solutions pre-populate the cache at startup; cache-aside still helps when entries expire or are evicted.
- **Local caches** are private to an instance, so copies diverge; consider a shared or distributed cache.

## Cache down
Lazy loading tolerates a node failing and being replaced by an empty node: the application keeps working with more latency, because each miss queries the database and refills the cache. Plan database capacity for a cold cache; Azure's guidance for reliability is that the workload can fall back to the origin data store if the cache malfunctions.

## When not to use
- Sensitive or security-related data, especially in a cache shared by several applications or users: fetch from the primary source.
- A static data set that fits in the cache (prime it at startup instead) or workloads where most requests miss, since the overhead then outweighs the benefit.
- Session state in a web farm: avoid client-server affinity dependencies.

## Verify
- [ ] Flush the cache in staging at peak replay: the database stays within capacity.
- [ ] Write then read returns the new value (within the stated staleness).
- [ ] Hit ratio and latency dashboards exist.

## Checked
2026-11-08. Confirmed on the Azure Cache-Aside pattern page (flow, update-then-invalidate ordering, lifetime, eviction, priming, consistency, local caching, when to use, reliability fallback) and the ElastiCache caching strategies page (lazy loading, node failure behaviour, cache-miss penalty, TTL semantics). Removed (not on these pages): TTL jitter formula, Redis `SET ... NX PX` lock keys, Lua versioned writes, singleflight, probabilistic refresh, negative-caching TTL, schema version in keys, 20-50 ms timeouts, memory-overhead sizing, `allkeys-lru` and `redis-cli --hotkeys`, and the Redis client-side-caching source (the page returned no text).
Method: documentation only; no commands were run.
