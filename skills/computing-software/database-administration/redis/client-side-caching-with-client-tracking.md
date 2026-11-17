---
id: computing-software.database-administration.redis.client-side-caching-with-client-tracking
name: client-side-caching-with-client-tracking
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, client-side-caching, client-tracking, invalidation, resp3, bcast, optin, tracking-table]
level: practitioner
status: docs-checked
description: "Use Redis server-assisted client-side caching (CLIENT TRACKING): default vs BCAST vs OPTIN/OPTOUT modes, RESP3 invalidation pushes, and the correctness traps."
sources:
  - https://redis.io/docs/latest/develop/clients/client-side-caching
  - https://redis.io/docs/latest/develop/reference/client-side-caching/
  - https://redis.io/docs/latest/commands/client-tracking/
  - https://redis.io/docs/latest/commands/client-caching/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client-side caching (CLIENT TRACKING)

**Goal:** keep hot keys in application memory and have Redis tell the client when they change, cutting round trips for read-heavy workloads. Tracking was added in Redis 6.0.

## Modes
| Mode | How | Server memory |
|---|---|---|
| Default | Server remembers which keys each client read (in an invalidation table keyed by client ID) and invalidates those | Table bounded by `tracking-table-max-keys` (default 1,000,000) |
| BCAST | Client subscribes to key prefixes (`PREFIX`); any change to a matching key is broadcast. No prefix means every key | None for tracked keys (a prefix table instead), more invalidation traffic |
| OPTIN | Only track reads that directly follow `CLIENT CACHING YES` | Less |
| OPTOUT | Track all reads except those that directly follow `CLIENT CACHING NO` | Less |
Prefixes in BCAST mode must not overlap (for example `foo` and `foob`). `NOLOOP` suppresses invalidations for keys the same connection modified.

## Turning it on (RESP3)
```text
HELLO 3
CLIENT TRACKING on
GET user:42            # cache locally
# later another client: SET user:42 ...
# this connection receives a push: invalidate [user:42]
```
RESP2 needs a second connection that runs `CLIENT ID` then `SUBSCRIBE __redis__:invalidate`, and the data
connection uses `CLIENT TRACKING on REDIRECT <id>`. In RESP3 a redirect also works. A flush (`FLUSHALL`/`FLUSHDB`)
sends a null invalidation, so clients must drop their whole cache.

BCAST with prefixes:
```text
CLIENT TRACKING on BCAST PREFIX user: PREFIX product:
```

## Use a library
Writing this correctly is subtle; use built-in support. The Redis documentation lists these clients as
supporting client-side caching from these versions: redis-py 5.1.0, Jedis 5.2.0, node-redis 5.1.0, go-redis
9.22.0. Other clients may expose `CLIENT TRACKING` without supporting the caching features themselves. See each
client's "connect" page on redis.io for its configuration. Read-only commands use the cache, except
probabilistic and time series types, non-deterministic commands (`HRANDFIELD`, `HSCAN`, `ZRANDMEMBER`) and `FT.*`.

## Correctness caveats
- If any connection of a client drops, the client must flush its whole local cache (invalidations may have been missed). Also ping the invalidation channel periodically and flush if no reply arrives.
- Race with a separate invalidation connection: an invalidation can arrive before the reply that populated the cache. Libraries mark the entry as in progress and discard replies for entries that were invalidated meanwhile. A single RESP3 connection has no such race.
- When the invalidation table is full, the server evicts an entry and sends an invalidation as if the key had changed: correct, but noisier.
- Put a maximum TTL on every locally cached key and bound the local cache size.
- Keep fast-changing data (counters, scoreboards) on a separate connection without caching.

## Verify
`CLIENT INFO` shows `flags=t` (tracking; `B` marks broadcast mode); `INFO stats` `tracking_total_keys` and the app-side hit ratio confirm benefit; a write from another client removes the local entry in a test.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): client-side caching introduction
and reference, CLIENT TRACKING, CLIENT CACHING, CLIENT LIST, INFO, and `redis.conf`. Confirmed: modes and options,
OPTIN/OPTOUT semantics (`CLIENT CACHING YES`/`NO`), RESP2 redirect via `__redis__:invalidate`, the flush and race
guidance, `tracking-table-max-keys` default, the client version table, flag letters `t` and `B`, `tracking_total_keys`.
Fixed: removed Lettuce `ClientSideCaching` and the unversioned library class names (not in the documentation);
the documented minimum versions replace "redis-py 5.1+, Jedis 5, node-redis v5".
Method: documentation only; no commands were run.
