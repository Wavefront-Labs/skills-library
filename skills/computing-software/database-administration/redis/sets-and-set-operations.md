---
id: computing-software.database-administration.redis.sets-and-set-operations
name: sets-and-set-operations
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, redis-sets, sinterstore, sadd, set-operations, redis-data-types]
level: practitioner
status: docs-checked
description: "Model membership, tagging and unique tracking with Redis sets: SADD/SISMEMBER, SINTER/SUNION/SDIFF and their STORE forms, SINTERCARD, and big-set cautions."
sources:
  - https://redis.io/docs/latest/develop/data-types/sets/
  - https://redis.io/docs/latest/commands/sinterstore/
  - https://redis.io/docs/latest/commands/sintercard/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sets and set operations

**Goal:** fast membership tests and set algebra (users who did A and B), using unordered unique collections.

## Basics
```text
SADD article:42:tags redis databases caching     # returns number added
SISMEMBER article:42:tags redis                  # O(1)
SMISMEMBER article:42:tags redis mysql           # many at once (6.2+)
SCARD article:42:tags
SREM article:42:tags caching
SRANDMEMBER pool 3   /   SPOP pool               # random pick / random pop
```

## Set algebra
```text
SINTER tag:redis tag:python                      # returns members
SINTERSTORE tmp:redis_python tag:redis tag:python  # writes result, returns size
EXPIRE tmp:redis_python 60
SUNIONSTORE / SDIFFSTORE  ...
SINTERCARD 2 tag:redis tag:python LIMIT 100      # count only, stops at LIMIT (7.0+)
```
Pattern: compute a filter result once into a temp key with a short TTL, then paginate it with `SSCAN` or move it into a sorted set for ordering.

## Complexity warnings
- `SINTER` is O(N*M) worst case (N smallest set size); `SUNION`/`SDIFF` O(total members). On million-member sets these block the server: check `SLOWLOG`.
- `SMEMBERS` returns all members in one reply; use `SSCAN key 0 COUNT 1000` for large sets.
- `SINTERCARD` exits early once the intersection reaches `LIMIT` (default 0 = unlimited).

## Alternatives
- Approximate unique counts: HyperLogLog.
- Ordered membership or scores: sorted sets.
- Very large membership filters with tolerance for false positives: Bloom filters.

## Verify
`SLOWLOG GET` shows no set operations over your latency budget.

## Checked
2026-10-31. Confirmed against the Redis sets data-type page and the SINTERSTORE and SINTERCARD
command pages: command forms, `SMISMEMBER` (6.2.0), `SINTERCARD` and `LIMIT` (7.0.0), the
complexity of `SINTER` (O(N*M)), `SUNION`/`SDIFF` (O(N) total members) and `SMEMBERS`/`SSCAN`.
Removed: cluster hash-slot rule, encoding thresholds, the HyperLogLog size, and the
MEMORY USAGE / OBJECT ENCODING check.
Method: documentation only; no commands were run.
