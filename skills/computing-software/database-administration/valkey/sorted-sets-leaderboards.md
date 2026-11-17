---
id: computing-software.database-administration.valkey.sorted-sets-leaderboards
name: sorted-sets-leaderboards
category: computing-software
field: database-administration
product: valkey
tags: [sorted-sets, zadd, zrange, zrank, zincrby, leaderboard, zrangebylex, zrangebyscore]
level: practitioner
status: docs-checked
description: "Valkey sorted sets: ZADD, ZRANGE, ZRANK, ZINCRBY, score ranges, WITHSCORES, lexicographic ranges, leaderboards and rate limiter use, O(log N) costs."
sources:
  - https://valkey.io/topics/sorted-sets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A sorted set holds unique members, each with a floating-point score; order is by score, then lexicographically for equal scores. It is a hybrid of set and hash, kept ordered by the structure itself (B+ tree plus hash table), so inserts are O(log N) and reads of sorted output cost no extra sorting. Uses: leaderboards, sliding-window rate limiters.

Commands:
- `ZADD key score member [score member ...]`: variadic; on an existing member it updates the score and position; the reply counts only newly added members (0 when the member already existed).
- `ZRANGE key 0 -1 [WITHSCORES]` ascending; `ZREVRANGE` descending; 0 and -1 mean first to last element.
- `ZRANGEBYSCORE key -inf 10` returns scores up to 10 inclusive.
- `ZREM` removes members; `ZREMRANGEBYSCORE` removes by score range and returns the count.
- `ZRANK` and `ZREVRANK` give the position ascending or descending.
- `ZINCRBY key n member` adds to a score and returns the new score.

Leaderboard example: `ZADD` sets a racer score directly (100, then 150 ignoring the old value), `ZINCRBY` adds 50 to reach 200. Combine top-N `ZRANGE` with `ZREVRANK` to show "you are #4932".

Lexicographic ranges: if all members share one score (say 0), `ZRANGEBYLEX`, `ZREVRANGEBYLEX`, `ZREMRANGEBYLEX`, `ZLEXCOUNT` compare bytes with `memcmp` (no collation). Bounds are inclusive or exclusive by first character; `-` and `+` are the infinities. Prefixing a 16-byte big-endian number indexes 128-bit integers.

Cost: most operations O(log N); `ZRANGE` is O(log N + M) for M results, so avoid tens of thousands per call.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/sorted-sets/ (page text read in full): Score then lexicographic ordering, B+ tree plus hash table, ZADD variadic, ZRANGE/ZREVRANGE with 0 -1 and WITHSCORES, ZRANGEBYSCORE -inf 10 inclusive, ZREM/ZREMRANGEBYSCORE, ZRANK/ZREVRANK, lex commands with memcmp, 16-byte big-endian prefix, leaderboard ZADD/ZINCRBY example, O(log(n)) and O(log(n) + m).

Removed or changed: Wrong ZADD reply semantics: the page shows ZADD replying 0 when the member already exists and the count of new members otherwise.

Method: documentation only; no commands were run.
