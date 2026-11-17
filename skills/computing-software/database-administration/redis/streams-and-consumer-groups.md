---
id: computing-software.database-administration.redis.streams-and-consumer-groups
name: streams-and-consumer-groups
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, redis-data-types, redis-streams, consumer-groups, xadd, xreadgroup, xack, xautoclaim, pending-entries-list, maxlen]
level: practitioner
status: docs-checked
description: "Build a durable work queue on Redis Streams: XADD with trimming, consumer groups, XREADGROUP/XACK, pending entries, XAUTOCLAIM for dead consumers."
sources:
  - https://redis.io/docs/latest/develop/data-types/streams/
  - https://redis.io/docs/latest/commands/xreadgroup/
  - https://redis.io/docs/latest/commands/xautoclaim/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streams and consumer groups

**Goal:** at-least-once processing with multiple workers, crash recovery, and bounded memory.

## Produce
```text
XADD orders MAXLEN ~ 1000000 * id 42 total 99.50     # ~ = approximate trim (efficient)
XADD orders MINID ~ 1729000000000 * ...               # trim by time-based ID
```
IDs are `<ms>-<seq>`; `*` auto-generates.

## Consumer group
```text
XGROUP CREATE orders billing $ MKSTREAM               # $ = only new entries; 0 = from the beginning
XREADGROUP GROUP billing worker-1 COUNT 10 BLOCK 5000 STREAMS orders >
# ... process ...
XACK orders billing 1729000000000-0
```
`>` gives never-delivered entries. Each delivered entry sits in the group's **Pending Entries List** (PEL) until XACKed.

## Recover from crashed consumers
```text
XPENDING orders billing                               # summary: count, min/max ID, per consumer
XPENDING orders billing IDLE 60000 - + 10             # entries idle > 60 s
XAUTOCLAIM orders billing worker-2 60000 0-0 COUNT 50 # take over stale entries (6.2+)
```
On startup each worker first re-reads its own PEL: `XREADGROUP GROUP billing worker-1 STREAMS orders 0`.

## Poison messages
The extended form of `XPENDING` shows a delivery count; after N deliveries, copy to a dead-letter stream and XACK.

## Monitoring
```text
XINFO STREAM orders            # length, first/last entry, groups
XINFO GROUPS orders            # pending, last-delivered-id, lag (7.0+)
XINFO CONSUMERS orders billing # idle time per consumer
```
Delete departed consumers with `XGROUP DELCONSUMER` (their pending entries become unclaimable: claim or acknowledge them first).

## Gotchas
- Without MAXLEN/MINID or XTRIM a stream grows forever; acking does not delete entries.
- Processing must be idempotent: a consumer that dies after the work but before XACK gets redelivered.
- In Cluster, a stream is one key on one shard: shard by multiple streams for throughput.

## Verify
Kill a worker mid-batch; within the claim interval another worker processes its entries and `XINFO GROUPS` pending returns to ~0.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the command definitions in redis/redis 8.2 and the redis/docs repository: XADD trimming with MAXLEN or MINID, `=` or `~` and LIMIT (MINID and LIMIT since 6.2); XGROUP CREATE with MKSTREAM and ENTRIESREAD; XAUTOCLAIM since 6.2 with `key group consumer min-idle-time start [COUNT] [JUSTID]`; XPENDING `[IDLE min-idle-time] start end count [consumer]` (IDLE since 6.2); XINFO GROUPS `lag` field since 7.0; XGROUP DELCONSUMER leaves pending messages unclaimable. Wording about delivery counts and idempotency follows from these commands.
Method: documentation only; no commands were run.
