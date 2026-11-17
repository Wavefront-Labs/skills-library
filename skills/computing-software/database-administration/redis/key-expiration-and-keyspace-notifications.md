---
id: computing-software.database-administration.redis.key-expiration-and-keyspace-notifications
name: key-expiration-and-keyspace-notifications
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, key-expiration, keyspace-notifications, ttl, expire, redis-data-types]
level: practitioner
status: docs-checked
description: "Set and manage Redis key TTLs (EXPIRE options, PERSIST, TTL/PTTL), understand lazy versus active expiry, and subscribe to expired-key events with keyspace notifications."
sources:
  - https://redis.io/docs/latest/commands/expire/
  - https://redis.io/docs/latest/develop/use/keyspace-notifications/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key expiration and keyspace notifications

## TTL commands
```text
EXPIRE cache:user:42 300          # seconds; PEXPIRE for ms; EXPIREAT/PEXPIREAT absolute
EXPIRE cache:user:42 600 GT       # 7.0+: NX | XX | GT | LT conditions
TTL cache:user:42                 # -1 no TTL, -2 key missing
PERSIST cache:user:42             # remove TTL
EXPIRETIME cache:user:42          # absolute unix time (7.0+)
```
- Overwriting with `SET` clears the TTL unless `KEEPTTL` is given; `INCR`, `LPUSH`, `HSET` keep it.
- `RENAME` keeps the TTL of the source.
- Hash fields can expire individually from 7.4 (`HEXPIRE`); before that, only whole keys.

## How expiry happens
- **Lazy:** a key is checked and deleted when accessed.
- **Active:** a background cycle runs 10 times a second, samples 20 keys with a TTL, deletes the expired ones and repeats while more than 25% of the sample was expired (`active-expire-effort` tunes it, range 1-10, default 1).
- Expired-but-unaccessed keys can occupy memory briefly; `INFO keyspace` `expires=` counts keys with TTL; `INFO stats` `expired_keys` counts deletions.
- Replicas do not expire keys themselves; they wait for the primary's `DEL`, though reads on a replica hide logically expired keys.

## Keyspace notifications
Off by default (cost CPU). Enable only the classes you need:
```text
CONFIG SET notify-keyspace-events Ex      # E = keyevent channel, x = expired events
SUBSCRIBE __keyevent@0__:expired
```
Flags: `K` keyspace, `E` keyevent, `g` generic, `$` string, `l` list, `s` set, `h` hash, `z` zset, `t` stream, `d` module, `x` expired, `e` evicted, `n` new key, `m` key miss. `A` is an alias for most classes (it excludes `m`, `n`, `o`, `c`); at least `K` or `E` must be set or nothing is delivered.

## Caveats
- Delivery is fire-and-forget Pub/Sub: a disconnected subscriber loses events. Not suitable as a reliable scheduler; use a sorted set of due times or Streams.
- `expired` fires when Redis actually deletes the key, which can lag the TTL under low access.
- In Cluster, each node only publishes its own keys: subscribe on every primary.

## Verify
`redis-cli --scan --pattern 'cache:*' | head | xargs -I{} redis-cli TTL {}` shows positive TTLs; `INFO keyspace` expires/keys ratio matches expectations.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed: EXPIRE NX/XX/GT/LT (7.0), PERSIST, TTL results, SET clears the TTL (KEEPTTL since 6.0), INCR/LPUSH/HSET keep it, RENAME transfers it; EXPIRETIME (7.0); HEXPIRE (7.4); lazy plus active expiry (10 cycles a second, 20 keys per loop, repeat above 25%); replicas wait for the primary's DEL while hiding logically expired keys on reads; keyspace notifications off by default, flag list and the A alias, fire-and-forget delivery, expired events can lag the TTL, each cluster node publishes events for its own keys. Removed the wrong repeat threshold of about 10%.
Method: documentation only; no commands were run.
