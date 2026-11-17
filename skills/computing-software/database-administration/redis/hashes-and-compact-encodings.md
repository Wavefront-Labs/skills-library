---
id: computing-software.database-administration.redis.hashes-and-compact-encodings
name: hashes-and-compact-encodings
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, hashes, listpack, ziplist, memory-optimization, object-encoding, hexpire, hscan]
level: practitioner
status: docs-checked
description: "Use Redis hashes for compact small objects: listpack vs hashtable thresholds, OBJECT ENCODING, bucketing many tiny keys, per-field TTL, and safe iteration."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/
  - https://redis.io/docs/latest/commands/object-encoding/
  - https://redis.io/docs/latest/commands/hexpire/
  - https://redis.io/docs/latest/commands/scan/
  - https://raw.githubusercontent.com/redis/redis/unstable/redis.conf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hashes and compact encodings (listpack)

**Goal:** store millions of small objects with the least memory, and know when Redis silently converts to the expensive encoding.

## Hash basics
```text
HSET user:1001 name "Ana" plan pro logins 0
HINCRBY user:1001 logins 1
HMGET user:1001 name plan
HGETALL user:1001              # O(n): avoid on big hashes, use HSCAN
HEXPIRE user:1001 3600 FIELDS 1 session   # 7.4+: per-field TTL
```
`HEXPIRE key seconds [NX | XX | GT | LT] FIELDS numfields field [field ...]` returns one status per field
(1 set, 0 condition not met, -2 no such field or key, 2 deleted because the TTL was 0).

## Encodings
Small aggregates are stored in a compact encoding and converted automatically when a limit is exceeded
(defaults from the memory optimization page and `redis.conf`):
| Type | Compact | Converts to | When over (defaults) |
|---|---|---|---|
| Hash | listpack | hashtable | `hash-max-listpack-entries 512` or a value longer than `hash-max-listpack-value 64` bytes |
| Sorted set | listpack | skiplist | `zset-max-listpack-entries 128` / `zset-max-listpack-value 64` |
| Set | intset (all integers) / listpack (7.2+) | hashtable | `set-max-intset-entries 512` / `set-max-listpack-entries 128`, `set-max-listpack-value 64` |
| List | listpack inside a quicklist | quicklist of nodes | per-node size set by `list-max-listpack-size` (default `-2`) |
Before 7.0 the directives were named `*-ziplist-*`; ziplist encodings applied up to 6.2.

```text
OBJECT ENCODING user:1001      # "listpack" or "hashtable"
MEMORY USAGE user:1001
```

## Bucketing trick
Many tiny keys cost far more than the same data in a few small hashes. The Redis memory documentation splits
`object:1234` into key `object:12` and field `34`, giving about 100 fields per hash, "an optimal compromise
between CPU and memory saved":
```text
# instead of SET obj:1234 v  ->  HSET obj:12 34 v     (bucket = id / 100, field = id % 100)
```
The same page reports roughly 5x less memory on average, up to 10x, for specially encoded types.

## Tuning
The limits are a CPU versus memory trade-off: compact encodings are linear-scan structures. If you raise
`hash-max-listpack-entries` far above the default, benchmark with `redis-benchmark` first, as the documentation
advises for larger values, and watch latency with `LATENCY` and `SLOWLOG`.

## Gotchas
- One value longer than `hash-max-listpack-value` converts the whole hash.
- Hash fields can now carry a TTL (`HEXPIRE`, 7.4+); the pre-7.4 rule that fields cannot expire no longer holds.
- `redis-cli --bigkeys` and `--memkeys` find the outliers; `HSCAN key cursor [MATCH pattern] [COUNT count] [NOVALUES]`
  iterates a large hash (`NOVALUES` since 7.4).

## Verify
`INFO memory` `used_memory` before/after loading a sample with the bucketed layout; `OBJECT ENCODING` shows listpack for buckets.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): memory optimization page, OBJECT
ENCODING, HEXPIRE, SCAN/HSCAN, redis-cli reference, plus `redis.conf` from the redis/redis repository. Confirmed:
defaults (hash 512/64, zset 128/64, set intset 512, set listpack 128/64, list -2), `listpack` names versus
`ziplist` before 7.0, `set` listpack since 7.2, the bucketing example and its 100 fields, HEXPIRE since 7.4.0 and
its grammar, HSCAN `NOVALUES` since 7.4, automatic conversion to the normal encoding. Fixed: the hash default is
`hash-max-listpack-entries 512`, not 128. Removed: "conversion is one way", "threshold changes only affect keys
written afterwards", the "~50+ bytes per key" overhead figure, and the "ziplist names still accepted as aliases"
claim (none is stated in the documentation), and "listpack list nodes of 8 KB" (only the `-2` default is documented).
Method: documentation only; no commands were run.
