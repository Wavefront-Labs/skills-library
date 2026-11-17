---
id: computing-software.database-administration.redis.caching-patterns-and-eviction
name: caching-patterns-and-eviction
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, keydb, memcached, cache, caching, cache-aside, lazy-loading, write-through, ttl, expire, maxmemory, maxmemory-policy, allkeys-lru, allkeys-lfu, volatile-lru, eviction, rdb, aof, appendfsync, persistence, scan, keys, bigkeys, memory-usage, unlink, cache-stampede, thundering-herd, hot-key, redis-cli]
level: practitioner
status: docs-checked
description: "Use Redis as a cache: cache-aside with TTL jitter, maxmemory and eviction policy, RDB vs AOF persistence, SCAN rather than KEYS, and stampede protection."
sources:
  - https://redis.io/docs/latest/develop/reference/eviction/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
  - https://redis.io/docs/latest/commands/scan/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Redis caching patterns and eviction — fast, bounded, and safe to lose

**Goal:** a Redis cache that stays inside its memory budget, evicts the right keys,
never blocks on a single command, and does not stampede the database when hot keys
expire.

## 1. Cache-aside (the default pattern)
```python
def get_user(uid):
    key = f"user:v3:{uid}"                 # version the key format
    val = r.get(key)
    if val is not None:
        return deserialize(val)
    row = db.fetch_user(uid)
    ttl = 3600 + random.randint(0, 300)   # jitter avoids synchronised expiry
    r.set(key, serialize(row), ex=ttl)
    return row

def update_user(uid, data):
    db.update_user(uid, data)
    r.delete(f"user:v3:{uid}")            # invalidate after the DB commit, don't set
```
- Delete on write, not set: concurrent writers setting the cache can leave an older
  value winning.
- Always set a TTL. A key without one is a permanent memory leak in a cache.
- Cache misses for non-existent rows too (a short-TTL sentinel), or a scan of random
  IDs bypasses the cache entirely.
- Write-through (update cache in the same code path as the DB) suits read-after-write
  needs but still needs a TTL as a safety net.

## 2. Stampede protection
When a hot key expires, hundreds of requests recompute it at once. Options:
- **Lock:** one caller wins a short-lived lock and recomputes; others serve
  stale or briefly wait and retry.
- **Early refresh:** store the computed-at time; refresh probabilistically as expiry
  approaches (XFetch-style), or have a background job refresh known-hot keys.
- **Request coalescing** in the app (single-flight) per process.

## 3. Memory limit and eviction
```
maxmemory 6gb                 # leave RAM free for replication and persistence buffers
maxmemory-policy allkeys-lfu  # or allkeys-lru for a pure cache
maxmemory-samples 10          # default 5 (documented); 10 approximates true LRU more closely at some CPU cost
```
| Policy | Use |
|---|---|
| `allkeys-lru` / `allkeys-lfu` | pure cache; LFU keeps steadily popular keys |
| `volatile-lru` / `volatile-ttl` | mixed: only keys with TTL evictable |
| `noeviction` | Redis used as a primary store or queue; commands that add data fail when full |
A cache left on `noeviction` returns errors on commands that cache new data once full
(reads still work). The `volatile-*` policies behave like `noeviction` when no key has a TTL.
`allkeys-lru` is the documented good default if you have no reason to prefer another policy.
Check `INFO stats` `evicted_keys` and `INFO memory` `used_memory`.

## 4. Persistence: decide whether you need it
- **None** (`save ""`, `appendonly no`): fine for a pure cache that can warm from the DB.
  Restart = cold cache; plan for the load.
- **RDB** snapshots (`save <SECONDS> <CHANGES>`): compact point-in-time files; changes since the last snapshot are lost.
- **AOF** (`appendonly yes`, `appendfsync everysec`): you may lose 1 second of data; since
  Redis 7.0.0 the AOF is multi-part (a base file plus incremental files and a manifest).
Both RDB snapshots and AOF rewrites `fork()`, which can pause serving on a big dataset.

## 5. Commands that hurt
- `KEYS *` is O(N) and blocks the single command thread. Use
  `SCAN 0 MATCH user:* COUNT 1000` and iterate until the cursor returns `0`.
- On big collections, paginate with `HSCAN`/`SSCAN` instead of reading everything at once.

## Verify
- [ ] `CONFIG GET maxmemory` is non-zero and the policy is an `allkeys-*` policy for a cache.
- [ ] `INFO keyspace` shows `expires` close to `keys`.
- [ ] Hit rate `keyspace_hits / (hits + misses)` is measured and acceptable.
- [ ] A restart or full flush in staging does not overload the database (stampede tested).

## Checked
2026-11-01. Confirmed against the Redis docs (eviction, persistence, SCAN): eviction policy list and behaviour
(noeviction errors on commands that cache new data while reads still work, volatile-* act like noeviction without
TTLs, allkeys-lru as good default, maxmemory-samples default 5 and 10), evicted_keys and used_memory, multi-part AOF
from 7.0.0, everysec losing up to 1 second, save "", fork() cost, SCAN cursor returning 0, HSCAN/SSCAN. Removed as
unconfirmed: the Valkey claim, SET NX PX lock syntax, Cluster hot-key advice, UNLINK/KEYS/ACL advice, big-key and
slowlog tooling, and the RDB data-loss estimate.
Method: documentation only; no commands were run.
