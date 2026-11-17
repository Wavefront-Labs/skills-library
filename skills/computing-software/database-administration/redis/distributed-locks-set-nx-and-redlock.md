---
id: computing-software.database-administration.redis.distributed-locks-set-nx-and-redlock
name: distributed-locks-set-nx-and-redlock
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, distributed-lock, set-nx, redlock, fencing-token, lua, mutual-exclusion]
level: advanced
status: docs-checked
description: "Implement Redis locks with SET NX PX and a compare-and-delete release, understand Redlock's assumptions, and add fencing tokens when correctness matters."
sources:
  - https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/
  - https://redis.io/docs/latest/commands/set/
  - https://redis.io/docs/latest/develop/using-commands/transactions/
  - https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed locks with Redis

**Goal:** a lock that is released only by its owner, expires if the owner dies,
and is used only where an occasional double-run is tolerable (or fenced).

## Acquire
```
SET lock:report:2026-10-16 <random-token> NX PX 30000
```
Returns OK if acquired, nil if held. `NX` = only if absent; `PX` = expiry in ms
so a crashed holder cannot block forever. The token must be unique across all clients and
all lock requests (the Redis page suggests 20 bytes from `/dev/urandom`).

Never `SETNX` then `EXPIRE` as two commands: a crash between them leaves a lock that never expires.

## Release: compare and delete atomically
Redis 8.4 and later:
```
DELEX lock:report:2026-10-16 IFEQ <token>
```
Older versions use a Lua script:
```lua
-- KEYS[1]=lock key, ARGV[1]=token
if redis.call("GET", KEYS[1]) == ARGV[1] then
  return redis.call("DEL", KEYS[1])
else
  return 0
end
```
`EVAL <script> 1 lock:report:2026-10-16 <token>` (or `EVALSHA` after `SCRIPT LOAD`). A plain `DEL` could delete a
lock that expired and was acquired by someone else. (`SET ... IFEQ` from 8.4 is the compare-and-set counterpart.)

## Renewal
For work that may exceed the TTL, extend periodically with a Lua script that extends the TTL only while the key
still holds your token. The Redis page suggests short validity times with extension, and limiting the number of
extensions. If renewal fails, stop the work.

## Redlock and its limits
Redlock acquires the lock on a majority of N independent Redis masters (the page uses N=5, so at least 3) within a
time budget smaller than the lock validity, then treats the validity as the initial TTL minus the time spent
acquiring. No replication between those masters. It assumes local clocks advance at about the same rate with small
drift. Redis does not use a monotonic clock for TTL expiry, so a wall-clock jump can let two clients hold a lock.
A long process pause (such as GC) beyond the validity can also leave two holders. If correctness (not just
efficiency) depends on exclusivity:
- use a **fencing token**: a monotonically increasing number issued with the lock
  (`INCR lock:report:fence`), passed to the protected resource, which rejects older tokens; or
- use a consensus system or the database's own locking instead of Redis.
The Redis page links Martin Kleppmann's analysis (listed in sources) and the author's reply.

## Gotchas
- Single-instance Redis with asynchronous replication: if the master crashes before the lock key reaches the
  replica and the replica is promoted, another client can acquire the same lock.
- Without persistence, a restarted Redlock instance can re-grant locks; the Redis page discusses delayed restarts
  and `fsync=always` (which costs performance).
- Choose TTL >> normal work time; log when work nears TTL.
- After a failed attempt, release (unlock) all instances and retry after a random delay.

## Verify
Concurrency test: N workers loop acquire/work/release; count overlapping critical
sections (should be zero absent pauses); kill a holder and confirm the lock frees after TTL.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): "Distributed Locks with Redis",
SET, Transactions. Confirmed: `SET resource random NX PX 30000`, random value requirement, unlock script, `DELEX`
introduced in 8.4, Redlock steps and N=5, clock-drift assumption, non-monotonic TTL clock, fencing-token advice,
replication race, persistence discussion, the Kleppmann link. Fixed: the page moved from
`/develop/use/patterns/distributed-locks/` (404) to `/develop/clients/patterns/distributed-locks/`; added the
8.4 `DELEX` release form. Removed: library-specific claims (Redisson watchdog, redis-py `Lock.extend`) and the
PostgreSQL advisory-lock and `SELECT ... FOR UPDATE` examples, none of which the Redis documentation covers.
Method: documentation only; no commands were run.
