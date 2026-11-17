---
id: computing-software.database-administration.redis.sorted-sets-leaderboards-and-rate-limits
name: sorted-sets-leaderboards-and-rate-limits
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, sorted-set, zadd, zrange, leaderboard, rate-limiting, delayed-queue, listpack]
level: practitioner
status: docs-checked
description: "Model leaderboards, sliding-window rate limits and delayed queues with Redis sorted sets, using ZADD/ZRANGE (BYSCORE, REV, LIMIT) and knowing encoding and precision limits."
sources:
  - https://redis.io/docs/latest/commands/zadd/
  - https://redis.io/docs/latest/commands/zrange/
  - https://redis.io/docs/latest/develop/using-commands/multi-key-operations/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Sorted sets

**Goal:** ranked and time-ordered data with O(log N) updates, used in the three
patterns where sorted sets shine.

## Basics
Members are unique strings, each with a double-precision score; ordered by score, then lexicographically (byte order) for ties.
```text
ZADD key [NX | XX] [GT | LT] [CH] [INCR] score member [score member ...]     # O(log N) per item; GT/LT need 6.2+
ZRANGE key start stop [BYSCORE | BYLEX] [REV] [LIMIT offset count] [WITHSCORES]   # 6.2+; O(log N + M)
ZINCRBY, ZSCORE, ZRANK / ZREVRANK, ZREMRANGEBYSCORE, ZPOPMIN
```
Scores accept `+inf` and `-inf`. `LIMIT` needs `BYSCORE` or `BYLEX`.

## Leaderboard
```
ZINCRBY lb:2026-10 50 user:42
ZRANGE lb:2026-10 0 9 REV WITHSCORES         # top 10
ZREVRANK lb:2026-10 user:42                  # 0-based rank
ZRANGE lb:2026-10 +inf -inf BYSCORE REV LIMIT 0 10
```
With `BYSCORE` and `REV`, `start` is the highest score and `stop` the lowest. Ties: equal scores order lexically by
member (reverse order with `REV`). For "first to reach score wins", encode time in the score
(`score*1e10 + (MAX_TS - ts)`) while the result stays within the 2^53 range that doubles hold exactly.

## Sliding-window rate limit
Per client key, members are request ids, scores are timestamps (ms):
```
MULTI
ZREMRANGEBYSCORE rl:ip:1.2.3.4 0 <now-60000>
ZADD rl:ip:1.2.3.4 <now> <now>-<rand>
ZCARD rl:ip:1.2.3.4
PEXPIRE rl:ip:1.2.3.4 60000
EXEC
```
Reject if ZCARD > limit. Exact but costs memory per request; for high volume use
fixed-window counters (`INCR` + `EXPIRE`) or a Lua token bucket.

## Delayed queue
Score = due time; workers poll:
```
ZADD jobs:delayed <due_ts> <job_id>
ZRANGE jobs:delayed -inf <now> BYSCORE LIMIT 0 100
ZREM jobs:delayed <job_id>        # claim: only the worker whose ZREM returns 1 owns it
```

## Gotchas
- Small sorted sets use the compact listpack encoding; past `zset-max-listpack-entries` (default 128) or a member longer than
  `zset-max-listpack-value` (default 64 bytes) they become skiplist plus hash, which uses more memory (the Redis
  memory page says compact encodings use up to 10 times less, 5 times on average, for small aggregates).
- `ZRANGE 0 -1` on a million-member set returns it all in one call and blocks the server: page with `LIMIT` or by index ranges.
  A large `LIMIT` offset still traverses `offset` elements.
- Scores are doubles: integers beyond -(2^53) to +(2^53) lose precision, so large integer ids may be approximated.
- In Redis Cluster, multi-key commands such as `ZUNIONSTORE` and `ZINTERSTORE` need all keys in the same hash slot (`{tag}`).

## Verify
`OBJECT ENCODING lb:2026-10` (listpack/skiplist), `MEMORY USAGE lb:2026-10`, and
`ZCARD` growth bounded by your trimming.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): ZADD, ZRANGE, multi-key operations,
memory optimization, OBJECT ENCODING. Confirmed: ZADD grammar and GT/LT since 6.2.0, ZRANGE grammar with BYSCORE/BYLEX/REV/LIMIT
since 6.2.0 and the REV start/stop rule, tie ordering, 2^53 exact-integer range, listpack defaults 128/64, ZUNIONSTORE and
ZINTERSTORE single-slot rule, O(log N + M) and the LIMIT offset caveat. Removed: the per-command complexity column for
ZINCRBY/ZSCORE/ZRANK (not read in the pages checked).
Method: documentation only; no commands were run.
