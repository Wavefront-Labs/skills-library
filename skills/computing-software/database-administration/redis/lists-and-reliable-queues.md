---
id: computing-software.database-administration.redis.lists-and-reliable-queues
name: lists-and-reliable-queues
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, redis-data-types, redis-lists, blmove, reliable-queue, lpush, brpop]
level: practitioner
status: docs-checked
description: "Build Redis list queues that don't lose jobs: LPUSH/BRPOP basics, the LMOVE/BLMOVE processing-list pattern, recovery of stuck items, and when to use Streams instead."
sources:
  - https://redis.io/docs/latest/develop/data-types/lists/
  - https://redis.io/docs/latest/commands/blmove/
  - https://redis.io/docs/latest/commands/lmove/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lists and reliable queues

## Basic queue (at-most-once)
```
LPUSH jobs '{"id":1,"type":"email"}'
BRPOP jobs 5            # worker blocks up to 5 s; returns [key, value]
```
If the worker crashes after BRPOP but before finishing, the job is lost.

## Reliable queue with a processing list
Atomically move the job to a per-worker processing list, delete it only when done:
```
BLMOVE jobs jobs:processing:worker-7 RIGHT LEFT 5     # Redis 6.2+ (replaces BRPOPLPUSH)
# ... do the work ...
LREM jobs:processing:worker-7 1 '<the exact job payload>'
```
A reaper periodically scans processing lists of dead workers and pushes items back:
```
LMOVE jobs:processing:worker-7 jobs RIGHT LEFT        # repeat until empty
```
Track worker liveness with a heartbeat key (`SET worker:7:alive 1 EX 30`). Jobs need a unique
id inside the payload so `LREM` removes the right entry and handlers are idempotent
(a requeued job may run twice: at-least-once).

## Useful list commands
| Command | Use |
|---|---|
| `LLEN jobs` | queue depth (monitor it) |
| `LRANGE jobs 0 9` | peek |
| `LTRIM log 0 999` | capped list (keep newest 1000 after LPUSH) |
| `LPOS`, `LINSERT`, `LSET` | positional ops (O(N)) |
| `LMPOP` (7.0), and its blocking form `BLMPOP` | pop from the first non-empty of several lists (priority queues) |

## Priority queues
`BRPOP high normal low 5` checks keys in order, so `high` is drained first.

## When to use Streams instead
Need consumer groups, acknowledgements, pending-entry inspection (`XPENDING`), claiming stuck
messages (`XAUTOCLAIM`), replay, or multiple independent consumers of the same messages?
Redis Streams provide that natively; the list pattern above is simpler but manual.

## Gotchas
- Blocking commands hold a connection per waiting worker; size pools accordingly.
- In Redis Cluster, the source and destination of `LMOVE` must be in the same hash slot:
  use hash tags (`{jobs}` and `{jobs}:processing:7`).
- Large payloads in lists cost memory; store the payload elsewhere and queue ids.
- Persistence: with RDB-only snapshots, jobs enqueued since the last snapshot are lost on crash;
  use AOF `everysec` for queues.

## Verify
Kill a worker mid-job in a test: the job stays in its processing list, the reaper requeues it,
and another worker completes it; `LLEN` of processing lists returns to 0.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the command definitions in the redis/redis 8.2 repository: BLMOVE since 6.2 with arguments `source destination LEFT|RIGHT LEFT|RIGHT timeout`; LMPOP since 7.0 (`numkeys key... LEFT|RIGHT [COUNT]`); XAUTOCLAIM since 6.2. Confirmed from the BRPOP page that multiple keys are checked in the order given. The remaining patterns (processing list, reaper, hash tags for LMOVE in Cluster, AOF everysec for queues) follow from these documented behaviours and the persistence page.
Method: documentation only; no commands were run.
