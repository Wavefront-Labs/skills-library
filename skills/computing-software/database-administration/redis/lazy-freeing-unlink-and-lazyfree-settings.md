---
id: computing-software.database-administration.redis.lazy-freeing-unlink-and-lazyfree-settings
name: lazy-freeing-unlink-and-lazyfree-settings
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, unlink, lazyfree, flushall-async, big-keys, latency, memory]
level: practitioner
status: docs-checked
description: "Avoid Redis stalls when deleting big keys: UNLINK, FLUSHALL ASYNC, and the lazyfree-* settings that make evictions, expiry and DEL free memory in a background thread."
sources:
  - https://redis.io/docs/latest/commands/unlink/
  - https://redis.io/docs/latest/commands/flushall/
  - https://redis.io/docs/latest/commands/info/
  - https://redis.io/docs/latest/develop/tools/cli/
  - https://raw.githubusercontent.com/redis/redis/unstable/redis.conf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy freeing (UNLINK / lazyfree-*)

**Goal:** freeing a hash with 5M fields with `DEL` takes seconds on the main thread and stalls every client. Free memory in a background thread instead.

## Commands
```text
UNLINK big:hash big:set          # removes keys from the keyspace now, reclaims memory in another thread
FLUSHDB ASYNC / FLUSHALL ASYNC   # ASYNC since 4.0, SYNC option since 6.2
```
`UNLINK` is like `DEL` but does the actual memory reclaiming in a different thread, so it is not blocking.
Its cost for the caller is O(1) per key regardless of size. An asynchronous `FLUSHALL` only deletes keys that
existed when it was invoked.

## Make implicit deletes lazy (redis.conf, all default `no`, all settable with CONFIG SET)
```text
lazyfree-lazy-eviction yes        # maxmemory evictions
lazyfree-lazy-expire yes          # TTL expiry
lazyfree-lazy-server-del yes      # implicit deletes, e.g. a command that stores data over an existing big key (RENAME target)
replica-lazy-flush yes            # replica flushing its dataset before loading a full resync
lazyfree-lazy-user-del yes        # make plain DEL behave like UNLINK
lazyfree-lazy-user-flush yes      # FLUSHALL/FLUSHDB default to ASYNC (6.2+)
```
Check the effective values on your server: `CONFIG GET lazyfree*`.

## Trade-offs
- Memory is reclaimed after the command returns, so `used_memory` lags behind the delete.
- `INFO memory` `lazyfree_pending_objects` shows objects waiting to be freed and `lazyfreed_objects` the count
  already freed in the background (both are in the memory section, not stats).

## Finding big keys first
```bash
redis-cli --bigkeys          # keys with many elements per type (SCAN-based)
redis-cli --memkeys          # keys using the most memory
```
Fix the data model (shard big hashes by suffix) instead of only hiding the delete cost.

## Verify
`LATENCY HISTORY command` or `SLOWLOG` no longer shows multi-second `DEL`/`EXPIRE` events after switching; `lazyfree_pending_objects` returns to 0.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): UNLINK, FLUSHALL, INFO (memory
section), redis-cli reference, plus `redis.conf` and `src/config.c` from the redis/redis repository. Confirmed:
UNLINK semantics and complexity, `FLUSHALL [ASYNC | SYNC]` with ASYNC since 4.0.0 and SYNC since 6.2.0,
`lazyfree-lazy-user-flush` since 6.2, all lazyfree defaults `no` and settable at runtime, the four documented
trigger categories, INFO field names. Fixed: `lazyfreed_objects` is reported in `INFO memory`, not `INFO stats`.
Removed: "small values are freed inline", "Valkey 8 turns several on", the "6.0+" tag on `lazyfree-lazy-user-del`,
and "lazy eviction can briefly overshoot maxmemory" (none is stated in the sources read).
Method: documentation only; no commands were run.
