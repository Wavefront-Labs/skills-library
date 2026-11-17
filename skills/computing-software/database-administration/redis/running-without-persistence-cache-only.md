---
id: computing-software.database-administration.redis.running-without-persistence-cache-only
name: running-without-persistence-cache-only
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, no-persistence, cache-only, redis-persistence, maxmemory-policy, redis-caching]
level: practitioner
status: docs-checked
description: "Run Redis as a pure cache with persistence off safely: config, the replication-restart data-wipe trap, warm-up, eviction policy and what to monitor."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/replication/
  - https://redis.io/docs/latest/develop/reference/eviction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running without persistence (cache-only)

**Goal:** lowest latency and no fork/disk overhead when the data can be rebuilt from the source of truth.

## Config
```text
save ""                     # disable RDB snapshots
appendonly no               # disable AOF
maxmemory 12gb
maxmemory-policy allkeys-lru    # or allkeys-lfu for skewed hot sets
```
Confirm: `CONFIG GET save` returns empty, `INFO persistence` shows `rdb_bgsave_in_progress:0` and `aof_enabled:0`.

## The replication trap
A primary with persistence off that restarts (crash, systemd restart) comes back **empty**, and its replicas then sync from it and wipe their own copies. The replication docs explicitly warn about this. Mitigations:
- Disable automatic restart of the primary process, or
- Let Sentinel fail over first (restart delay longer than `down-after-milliseconds` + failover time), or
- Keep RDB on replicas only (replicas can persist while the primary does not) and promote one on primary loss.
Replication still uses an RDB transfer for full syncs; `repl-diskless-sync yes` avoids writing it to disk.

## Cold start and warm-up
An empty cache sends 100% of reads to the database (thundering herd). Plan for it:
- Request coalescing / single-flight in the app.
- Gradual traffic shift or pre-warm scripts for hot keys.
- Database capacity sized to survive a cold cache for minutes.

## Eviction
- Without persistence, `noeviction` is almost never right for a cache (writes fail when full). Use an `allkeys-*` policy, or `volatile-*` when only TTL'd keys are disposable.
- Watch `INFO stats` `evicted_keys` and the hit ratio `keyspace_hits / (hits + misses)`.

## When not to do this
Sessions, rate-limit counters or queues that the business cannot lose; use AOF `everysec` there or a separate persistent instance.

## Verify
Restart a replica in staging: it resyncs from the primary; restart the primary with auto-restart disabled and confirm failover instead of an empty-primary resync.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the replication and administration pages: a master with persistence off that restarts empty wipes its replicas, so disable automatic restart or enable persistence; Sentinel can miss a fast restart; replicas can persist while the master does not; with replication Redis does RDB saves even without persistence unless diskless replication is used. Confirmed from the eviction page and redis.conf: `noeviction` is the default policy, `allkeys-*` and `volatile-*` policies, `maxmemory-samples` example. INFO fields `aof_enabled`, `rdb_bgsave_in_progress`, `evicted_keys`, `keyspace_hits` family are documented.
Method: documentation only; no commands were run.
