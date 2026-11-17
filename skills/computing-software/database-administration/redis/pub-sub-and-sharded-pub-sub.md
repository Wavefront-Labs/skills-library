---
id: computing-software.database-administration.redis.pub-sub-and-sharded-pub-sub
name: pub-sub-and-sharded-pub-sub
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, redis-data-types, pub-sub, publish, subscribe, psubscribe, sharded-pub-sub, ssubscribe, client-output-buffer-limit, keyspace-notifications]
level: practitioner
status: docs-checked
description: "Use Redis Pub/Sub for fire-and-forget fan-out: SUBSCRIBE/PSUBSCRIBE, sharded pub/sub in Cluster, output buffer limits, and when Streams is the right tool."
sources:
  - https://redis.io/docs/latest/develop/interact/pubsub/
  - https://redis.io/docs/latest/commands/ssubscribe/
  - https://redis.io/docs/latest/develop/use/keyspace-notifications/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pub/Sub

**Goal:** real-time fan-out (cache invalidation, live notifications) with no message storage, and no surprises when a subscriber is slow.

## Basics
```text
SUBSCRIBE chat:room:7
PSUBSCRIBE chat:room:*            # pattern
PUBLISH chat:room:7 "hello"      # returns number of receiving clients
PUBSUB CHANNELS chat:*
PUBSUB NUMSUB chat:room:7
```
A subscribed RESP2 connection can only (un)subscribe/ping; RESP3 allows normal commands on the same connection.

## Delivery semantics
At-most-once. If no one is subscribed, the message is dropped. If a subscriber disconnects (network blip, deploy), it misses everything sent meanwhile. Need durability or replay: use Streams.

## Slow subscribers
Messages queue in the subscriber's output buffer on the server:
```text
client-output-buffer-limit pubsub 32mb 8mb 60     # hard limit, soft limit for 60 s
```
These are the redis.conf defaults for subscriber clients. Watch `CLIENT LIST` for growing output buffers.

## Cluster: sharded pub/sub (7.0+)
Classic PUBLISH in Cluster is broadcast to every node (bus traffic grows with cluster size). Sharded:
```text
SSUBSCRIBE orders:{eu}
SPUBLISH orders:{eu} "..."
```
Channel hashes to a slot like a key; only that shard's nodes handle it. Use hash tags to co-locate.

## Keyspace notifications
`CONFIG SET notify-keyspace-events Ex` then `PSUBSCRIBE __keyevent@0__:expired` gets key expiry events. Same at-most-once semantics; expired events fire when Redis actually deletes the key (lazily or by the active cycle), not at the exact TTL instant.

## Gotchas
- A client subscribed to both a pattern and a matching channel can receive the same message twice (as `message` and `pmessage`).

## Verify
Two subscribers on a channel both receive a `PUBLISH`; `PUBLISH` returns 2; a disconnected subscriber does not get messages sent while it was away.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the Pub/Sub page: at-most-once delivery, RESP2 subscribed connections restricted to a small command set versus any command under RESP3, sharded Pub/Sub from 7.0 (SSUBSCRIBE, SPUBLISH, channel mapped to a slot), classic PUBLISH propagated to every cluster node, pattern subscriptions deliver `pmessage` and can duplicate. Confirmed `client-output-buffer-limit pubsub 32mb 8mb 60` default in redis.conf 8.2, SSUBSCRIBE since 7.0 (command definition), keyspace-notification behaviour. Removed unconfirmed: subscriptions on failover, per-pattern CPU cost, omem and OOM remarks.
Method: documentation only; no commands were run.
