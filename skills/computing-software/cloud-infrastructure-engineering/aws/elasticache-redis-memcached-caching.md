---
id: computing-software.cloud-infrastructure-engineering.aws.elasticache-redis-memcached-caching
name: elasticache-redis-memcached-caching
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elasticache, redis, valkey, memcached, caching-strategy, cache-aside, lazy-loading, write-through, ttl, cluster-mode, replication-group, read-replica, multi-az, automatic-failover, elasticache-serverless, global-datastore, redis-auth, rbac, in-transit-encryption, eviction-policy, maxmemory-policy, hot-key, big-key, session-store, rate-limiting, leaderboard, pub-sub]
level: practitioner
status: gated
description: "Use ElastiCache (Valkey/Redis OSS, Memcached): engine and topology choice, cache-aside vs write-through with TTL and stampede protection, cluster mode, failover, RBAC, eviction."
sources: ["https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Replication.Redis.Groups.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/BestPractices.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Clusters.RBAC.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/serverless-redis.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Redis-Global-Datastore.html", "https://valkey.io/topics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ElastiCache — Valkey/Redis and Memcached caching strategies

**Goal:** a cache that takes the read load off the database with a known hit rate, is
sized so eviction is a choice rather than an accident, survives a node failure without
the app noticing, and is not an unauthenticated open port in your VPC.

## 1. Engine and topology
| | Valkey / Redis OSS | Memcached |
|---|---|---|
| Data structures | Strings, hashes, lists, sets, sorted sets, streams, pub/sub, Lua, TTL per key | Strings only |
| Persistence / replication / failover | Yes (replicas, Multi-AZ auto-failover, snapshots) | None — node loss = cache loss |
| Scaling | Cluster mode (sharding by slot) | Add nodes; client-side hashing (Auto Discovery) |
| Pick | Almost always (Valkey is the default and ~20-33% cheaper than Redis OSS on ElastiCache) | Simplest possible volatile cache, multithreaded big nodes |
Topologies for Valkey/Redis:
- **Cluster mode disabled**: 1 primary + up to 5 replicas, one shard, data ≤ one node.
  Primary endpoint (writes) + reader endpoint (reads).
- **Cluster mode enabled**: up to 500 shards, each with replicas; keys hashed into
  16,384 slots; client must be cluster-aware (`redis-py-cluster`/`RedisCluster`,
  Lettuce, ioredis `Cluster`). Multi-key commands need the same slot — use hash tags
  `{user:123}:profile` / `{user:123}:cart`. Needed once one node's memory or throughput is not enough.
- **Serverless**: no nodes; pay per GB-hour stored + ECPU; scales instantly; single
  cluster endpoint; ideal for unknown or spiky load, pricier at steady high throughput.
```bash
aws elasticache create-replication-group --replication-group-id app-cache --replication-group-description "app" \
  --engine valkey --engine-version 8.0 --cache-node-type cache.r7g.large --num-node-groups 3 --replicas-per-node-group 1 \
  --cache-subnet-group-name private --security-group-ids sg-cache --multi-az-enabled --automatic-failover-enabled \
  --transit-encryption-enabled --at-rest-encryption-enabled --kms-key-id alias/cache \
  --user-group-ids app-users --snapshot-retention-limit 3 --snapshot-window 03:00-04:00 \
  --cache-parameter-group-name app-valkey8 --auto-minor-version-upgrade
```

## 2. Caching strategies
- **Cache-aside (lazy loading)**: app reads cache; miss → read DB → `SET key value EX ttl`.
  Simple; only requested data is cached; first read is slow; stale until TTL.
- **Write-through**: every DB write also writes the cache. Never stale for written
  keys, but caches data nobody reads and a write path that must handle cache failure.
- **Combine**: write-through for hot entities + cache-aside with TTL as the safety net.
- **TTL always** (`EX`/`PX`), even on write-through — otherwise the cache fills with
  dead keys. Add jitter (`ttl ± 10%`) so a cohort of keys does not expire together.
- **Stampede protection**: on a miss, `SET lock:key 1 NX EX 5` — only the winner
  rebuilds; others wait briefly and re-read, or serve stale (`stale-while-revalidate`
  by storing `expires_at` inside the value and refreshing early).
- Negative caching (`SET key "" EX 30` for "not found") stops hammering the DB for
  missing ids.
- Serialize compactly (msgpack/protobuf, or JSON + gzip for larger values); keep values
  small and avoid million-member collections — a **big key** blocks the single-threaded
  engine on read/delete (gated: unconfirmed, source is paywalled or blocked) (`UNLINK` instead of `DEL`, `SSCAN`/`HSCAN` instead of
  `SMEMBERS`/`HGETALL`).
- Other patterns: sessions (`HSET session:<id> … EX`), rate limiting (`INCR` + `EXPIRE`
  or sliding window with `ZADD`/`ZREMRANGEBYSCORE`), leaderboards (`ZADD`/`ZREVRANGE`),
  distributed locks (`SET NX PX` + check-and-delete via Lua), pub/sub for fan-out
  (fire-and-forget; use Streams for durable queues).

## 3. Memory and eviction
- Parameter group: `maxmemory-policy` — `allkeys-lru` for a pure cache,
  `volatile-lru`/`volatile-ttl` when some keys must never be evicted (sessions), `noeviction`
  for a datastore (writes then fail with OOM).
- `reserved-memory-percent` 25% (default) leaves room for replication/snapshot
  fork-copy-on-write; do not lower it on write-heavy nodes.
- Alarms: `DatabaseMemoryUsagePercentage` > 80, `Evictions` > 0 when policy says no
  eviction expected, `EngineCPUUtilization` > 65 (single-threaded: this is the real CPU),
  `CurrConnections` near the 65,000 limit, `ReplicationLag`, `CacheHitRate` < 0.8.
- Scale up (node type, online with failover) for memory; scale **out** (shards) for CPU/ops.
  `modify-replication-group-shard-configuration --node-group-count 6 --apply-immediately`
  reshards online.

## 4. Availability and failover
- Multi-AZ with automatic failover promotes a replica (DNS flip of the primary
  endpoint, cluster-mode clients get `MOVED` redirects). Client needs reconnect/retry
  logic and short DNS TTL; writes during failover fail — treat the cache as optional
  in the request path.
- Replicas are asynchronous; read-your-write from the reader endpoint is not guaranteed.
- Snapshots (RDB) daily to S3 + `copy-snapshot` for export; restore = new cluster.
  Persistence is for warm restart, not durability — never the system of record.
- **Global Datastore**: cross-region replica cluster (asynchronous replication), promote on regional
  failure; secondary is read-only.
- Maintenance window patches with failover; `auto-minor-version-upgrade` + a window at 3 am.

## 5. Security
- Enable in-transit (TLS) and at-rest encryption at creation. At-rest cannot be added
  later without a snapshot/restore; in-transit can be enabled online on recent engine
  versions via `modify-replication-group --transit-encryption-mode preferred` then `required`.
- **RBAC** (Redis 6+/Valkey): `create-user --user-name app --access-string "on ~app:* -@all +@read +@write +@hash -@dangerous" --authentication-mode Type=password,Passwords=<PASSWORD>`
  (or `Type=iam` for IAM auth tokens), grouped into a `user-group` attached to the
  replication group. The `default` user must be present in the group — give it `off`
  or a strong password. Legacy `--auth-token` is a single shared password; migrate.
- SG allows 6379 only from app SGs; no public endpoints exist, but a peered VPC is still a path.

## 6. Client hygiene
Connection pools (not a connection per request), pipelining for bulk ops, timeouts
(connect 1 s, command 200-500 ms) so a stalled cache does not take the app down,
circuit-breaker to bypass the cache under errors. `CLIENT LIST`/`INFO clients` to see
who is connected; `SLOWLOG GET 25` and `--bigkeys`/`MEMORY USAGE` to find culprits.
`KEYS *` is forbidden in production (blocks the node); `SCAN` with `COUNT`.

## Gotchas
- Memcached nodes are independent: scaling changes the hash ring and invalidates most keys; Auto Discovery clients handle membership but not the remap.
- `FLUSHALL` on a large dataset blocks for seconds; `FLUSHALL ASYNC` or rotate the cluster.
- Hot key on one shard caps throughput even with 20 shards; replicate hot reads
  client-side (local in-process cache for 1-5 s) or split the key.
- Lambda → ElastiCache needs VPC config; connection setup per cold start is the main latency.
- Engine version upgrades in cluster mode run rolling with brief `MOVED` storms; test clients.
- Unconfirmed: online in-transit-encryption enablement is version-dependent; check your engine version.

## Verify
- [ ] `CacheHitRate` ≥ 0.8 after warm-up and `Evictions` = 0 (or expected under `allkeys-lru`).
- [ ] `test-failover --node-group-id 0001` on the replication group: app keeps serving (cache bypass or reconnect) with no 5xx spike.
- [ ] `redis-cli --tls --user app --pass … --bigkeys` reports no key > 1 MB; `SLOWLOG` empty under load.
- [ ] Connecting without TLS or as `default` with no password fails.
- [ ] A DB outage drill: app degrades gracefully when cache is up and DB down (stale-serve) and when cache is down (DB direct with breaker).

## Checked

Date: 2026-11-02. Confirmed on ElastiCache User Guide pages in sources (What is ElastiCache, caching strategies, replication groups, best practices, RBAC, Global Datastore) and by check_commands (all aws elasticache flags exist): caching strategies, Multi-AZ replication groups, Global Datastore with a read-only secondary, RBAC. Removed as not stated there: 100 GB / 100k ops/s sharding threshold, 1 KB and 100 KB value sizes, ~1 minute failover time, 1 second Global Datastore lag. Left, marked gated: big-key blocking behaviour.

Method: documentation only; no commands were run.
