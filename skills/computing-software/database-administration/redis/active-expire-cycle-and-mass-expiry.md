---
id: computing-software.database-administration.redis.active-expire-cycle-and-mass-expiry
name: active-expire-cycle-and-mass-expiry
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, active-expire, mass-expiry, ttl, redis-latency, hz]
level: practitioner
status: docs-checked
description: "Diagnose Redis latency spikes from many keys expiring at once, tune hz and active-expire-effort, and spread TTLs with jitter to avoid expiry storms."
sources:
  - https://redis.io/docs/latest/commands/expire/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency-monitor/
  - https://redis.io/docs/latest/commands/info/
  - https://raw.githubusercontent.com/redis/redis/unstable/redis.conf
  - https://raw.githubusercontent.com/redis/redis/unstable/src/expire.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active expire cycle and mass expiry

**Goal:** stop the pattern where a batch job sets millions of keys with the same TTL and, an hour later, Redis stalls while it deletes them.

## Mechanics
- Keys expire two ways: passively when a client touches an expired key, and actively, where Redis periodically tests random keys that have a TTL and deletes the expired ones.
- In the source (`expire.c`) the slow cycle samples 20 keys per database per loop (`ACTIVE_EXPIRE_CYCLE_KEYS_PER_LOOP`), repeats while more than 10% of the sample was expired (`ACTIVE_EXPIRE_CYCLE_ACCEPTABLE_STALE`), and is capped at 25% of CPU time (`ACTIVE_EXPIRE_CYCLE_SLOW_TIME_PERC`). A fast cycle is capped at 1000 microseconds. `active-expire-effort` raises these baselines.
- `hz` (default 10) is the frequency at which Redis checks for background tasks, which include purging expired keys that are never requested.
- When a large share of keys expires at once the cycle keeps hitting its time cap, expired keys pile up in memory, and the work competes with client commands.
- The latency monitor tracks this as the `expire-cycle` event:
```text
CONFIG SET latency-monitor-threshold 10
LATENCY LATEST
LATENCY HISTORY expire-cycle
```

## Fixes
1. **Jitter TTLs**: `EXPIRE key (3600 + random(0..600))`. Spreading a 1M key batch over 10 minutes removes the spike.
2. **Lazy free expired values**: `lazyfree-lazy-expire yes` (default `no`) so big values are freed off-thread.
3. **Tune effort**: `active-expire-effort` accepts 1 to 10 (default 1). Higher values do more expiry work per cycle (source: more keys per loop, longer fast and slow cycles, a lower stale threshold) at more CPU cost.
4. **hz**: `dynamic-hz yes` (default) lets Redis use an adaptive hz value at runtime; redis.conf recommends the default of 10 for most users.
5. Avoid huge single keys with TTLs: expiring a 1 GB sorted set is a big delete regardless of cycles.

## Observe
```text
INFO stats      # expired_keys, expired_stale_perc, expired_time_cap_reached_count, expire_cycle_cpu_milliseconds
INFO keyspace   # db0:keys=...,expires=...,avg_ttl=...
```
`expired_time_cap_reached_count` is the number of times active expiry cycles stopped early; a rising value means expired keys are accumulating faster than the cycle clears them.

## Verify
After adding jitter, `LATENCY HISTORY expire-cycle` shows no events above the threshold at the batch's expiry time and memory declines smoothly.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8), `redis.conf` and `src/expire.c`
from the redis/redis repository. Confirmed: the `expire-cycle` latency event and the LATENCY subcommands,
`latency-monitor-threshold` via CONFIG SET, INFO field names and meanings, defaults for `active-expire-effort`
(1, maximum 10), `lazyfree-lazy-expire` (no), `hz` (10) and `dynamic-hz` (yes), and the 20-key / 10% / 25% constants.
Removed: the claim that the fast cycle runs before every event-loop iteration and adds latency to every command, and
the suggested hz range of 20-50 (redis.conf only recommends the default).
Method: documentation only; no commands were run.
