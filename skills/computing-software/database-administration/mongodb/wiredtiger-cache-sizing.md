---
id: computing-software.database-administration.mongodb.wiredtiger-cache-sizing
name: wiredtiger-cache-sizing
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-production-notes, mongodb-administration, wiredtiger-cache, wiredtiger, cache-eviction, working-set, containers-memory]
level: advanced
status: verified
description: "Size and monitor the MongoDB WiredTiger cache: default 50% of (RAM-1GB), container limits, dirty/eviction thresholds, and spotting a working set that no longer fits."
sources:
  - https://www.mongodb.com/docs/manual/core/wiredtiger/#memory-use
  - https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-storage.wiredTiger.engineConfig.cacheSizeGB
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WiredTiger cache sizing

**Goal:** the working set (indexes + hot documents) fits in cache, and the
cache does not starve the OS file cache or overrun a container limit.

## Defaults
WiredTiger cache = the larger of 50% of (RAM - 1 GB) and 256 MB (config docs; on a host reporting 32509 MB the server showed 15742 MB = 0.5 x (32509 - 1024)). The operating system uses free memory as the filesystem cache, which keeps the compressed data files in memory. Leaving the default is usually right on a dedicated host; `cacheSizeGB` accepts 256 MB to 10 TB.

## When to set it explicitly
```yaml
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 12
```
- **Containers / Kubernetes**: the docs say WiredTiger may not account for a container's memory limit in certain cases, so set `cacheSizeGB` (or `cacheSizePct`) below the RAM available to the container; check `db.hostInfo().system.memLimitMB` for what the server sees.
- Several mongod on one host: split RAM between them explicitly.

## Monitor
```javascript
const c = db.serverStatus().wiredTiger.cache;
({ maxGB: c["maximum bytes configured"]/2**30,
   usedGB: c["bytes currently in the cache"]/2**30,
   dirtyGB: c["tracked dirty bytes in the cache"]/2**30,
   readIntoCache: c["pages read into cache"],
   appThreadEvictAttempts: c["page evict attempts by application threads"],
   appThreadEvictMicros: c["application thread time evicting (usecs)"] })
```
WiredTiger defaults (tuning page): `eviction_target` 80% of the cache and `eviction_trigger` 95% (application threads start evicting), `eviction_dirty_target` 5% and `eviction_dirty_trigger` 20%. So healthy: used around 80% of max, dirty under 5%. Bad signs:
- used pinned at 95%+ and `page evict attempts by application threads` / `application thread time evicting (usecs)` rising: user
  operations doing eviction work, latency spikes.
- dirty > 20%: writes outpace checkpoint/eviction; slow storage.
- constant high `pages read into cache`: working set exceeds cache, disk reads per query.

## Fixes
Indexes that support the queries (fewer pages touched), drop unused indexes
(they occupy cache), more RAM, or shard.

## Gotchas
- Per the production notes, collection data in the WiredTiger cache is uncompressed, so on-disk sizes (compressed) underestimate the working set.
- `db.collection.stats().indexSizes` total vs cache size is a first sanity check.

## Verify
After changes, `serverStatus` cache metrics stay below eviction triggers under
peak load and p99 latency drops.

## Checked
- MongoDB 9.0.4 Community, mongosh 2.13.0 and Database Tools 100.19.1 (mongostat, mongotop) on Windows, run in a scratch folder. The monitoring snippet ran against a live node (maxGB 15.37, usedGB 0.03, dirty 0, pages read into cache 148). The original `pages evicted by application threads` key does not exist in 9.0.4 (it returned undefined); the keys `page evict attempts by application threads` and `application thread time evicting (usecs)` do, and the snippet was updated.
- A node started with `cacheSizeGB: 1` reported a 1 GB cache; the default on this host matched 0.5 x (RAM - 1 GB). `stats().indexSizes` is present.
- Docs fetched: configuration options (default formula, 256 MB lower bound, 10 TB upper bound), production notes (container guidance; cache data uncompressed), WiredTiger tune_cache page (eviction target/trigger/dirty defaults 80/95/5/20).
