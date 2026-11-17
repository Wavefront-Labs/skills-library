---
id: computing-software.database-administration.redis.bitmaps-and-hyperloglog
name: bitmaps-and-hyperloglog
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, redis-data-types, bitmaps, hyperloglog, setbit, bitcount, pfadd, pfcount, unique-counting, daily-active-users]
level: practitioner
status: docs-checked
description: "Count daily active users and unique visitors in Redis with bitmaps (SETBIT/BITCOUNT/BITOP) and HyperLogLog (PFADD/PFCOUNT/PFMERGE) at tiny memory cost."
sources:
  - https://redis.io/docs/latest/develop/data-types/strings/bitmaps
  - https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/
  - https://redis.io/docs/latest/commands/bitfield/
  - https://redis.io/docs/latest/commands/bitop/
  - https://redis.io/docs/latest/commands/setbit/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bitmaps and HyperLogLog

**Goal:** exact or approximate unique counts over huge populations in kilobytes, not gigabytes.

## Bitmaps: exact, needs dense integer IDs
```text
SETBIT dau:2026-10-16 1001 1          # user 1001 active today
GETBIT dau:2026-10-16 1001
BITCOUNT dau:2026-10-16               # DAU
BITOP AND active-both dau:2026-10-15 dau:2026-10-16    # active both days (retention)
BITOP OR  wau dau:2026-10-10 ... dau:2026-10-16        # weekly actives
BITFIELD counters INCRBY u8 #3 1      # packed small counters (#3 = third u8 slot)
```
Bitmaps are not a separate type: they are bit operations on strings, so a bitmap is limited to 512 MB
(offsets 0 to 2^32-1). Memory is set by the highest bit offset: the Redis docs give 12 MB for 100 million
users, regardless of how many bits are set. Sparse or huge/random IDs (UUIDs) make bitmaps wasteful: map
them to dense integers or use HLL. `BITOP` also has `XOR`, `NOT` and, from Redis 8.2, `DIFF`, `DIFF1`,
`ANDOR` and `ONE`.

## HyperLogLog: approximate, any IDs
```text
PFADD uv:2026-10-16 "user-8f3a" "user-91bc"
PFCOUNT uv:2026-10-16                         # standard error 0.81%
PFCOUNT uv:2026-10-15 uv:2026-10-16           # union count on the fly
PFMERGE uv:2026-W42 uv:2026-10-10 ... uv:2026-10-16
```
At most 12 KB per key (a lot less while few elements have been seen). An HLL holds no elements: you cannot
list members or test membership. It is stored as a string, so `GET`/`SET` can serialize it. A merge result is an
approximation of the union; intersections need inclusion-exclusion over several estimates and get noisy.

## Choosing
| Need | Use |
|---|---|
| Exact counts, set operations, dense IDs | Bitmap |
| Unique counts of arbitrary strings, tiny memory | HyperLogLog |
| "Have we seen X?" with false positives OK | Bloom filter (`BF.ADD`; Redis 8 and Redis Stack) |
| Exact membership + count, modest size | Set (`SADD`/`SCARD`) |

## Gotchas
- Setting the last possible bit (`SETBIT key 4294967295 1`) on a missing or small string makes Redis allocate all
  the intermediate memory at once, which can block the server: validate offsets.
- `BITOP` is O(N) and potentially slow on long strings. Run it off-peak; the BITOP page suggests a writable
  replica for large metrics jobs, but the replication page warns against writable replicas, so weigh that.
  In Redis Cluster all keys of a `BITOP` must share a hash slot.
- Set TTLs on per-day keys (`EXPIRE dau:2026-10-16 7776000`, 90 days).
- Check privacy rules before storing personal identifiers (IP addresses, user IDs) even in an HLL.

## Verify
Compare `PFCOUNT` against an exact `SCARD` on a sample day: error within about 1%.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): HyperLogLog page, bitmaps
page, SETBIT, BITOP, BITFIELD, multi-key operations page, memory optimization page. Confirmed: 12 KB and
0.81% for HLL, offsets below 2^32 and the 512 MB limit, the full-allocation warning for the last bit, BITOP
operators (the 8.2 additions) and O(N) cost, BITFIELD `#` offset multiplier and `INCRBY u8` syntax, 12 MB for
100 million users, BITOP single-slot rule in cluster. Fixed: BITOP cannot run on an ordinary read-only
replica (it writes); the docs suggest a writable replica, which the replication page discourages.
Replaced a dead bitmaps URL (`/develop/data-types/bitmaps/` is 404; it is now under `/strings/`).
Method: documentation only; no commands were run.
