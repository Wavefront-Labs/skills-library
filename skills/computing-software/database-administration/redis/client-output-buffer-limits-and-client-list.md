---
id: computing-software.database-administration.redis.client-output-buffer-limits-and-client-list
name: client-output-buffer-limits-and-client-list
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, client-list, client-output-buffer-limit, omem, pubsub, replica-buffer, client-kill, memory]
level: practitioner
status: docs-checked
description: "Find Redis clients that hog memory with CLIENT LIST (omem, qbuf, tot-mem), configure client-output-buffer-limit per class, and kill or cap offenders."
sources:
  - https://redis.io/docs/latest/commands/client-list/
  - https://redis.io/docs/latest/commands/client-kill/
  - https://redis.io/docs/latest/commands/client-no-evict/
  - https://redis.io/docs/latest/commands/client-no-touch/
  - https://redis.io/docs/latest/commands/info/
  - https://raw.githubusercontent.com/redis/redis/unstable/redis.conf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client output buffer limits and CLIENT LIST

## CLIENT LIST fields that matter
```
redis-cli CLIENT LIST
id=1287 addr=10.0.3.4:51234 laddr=... name=worker-3 age=8812 idle=0 flags=N db=0
  sub=0 psub=0 ssub=0 multi=-1 qbuf=0 qbuf-free=20474 argv-mem=0 obl=0 oll=0 omem=0
  tot-mem=22426 events=r cmd=get user=app lib-name=redis-py lib-ver=5.0.1
```
| Field | Meaning |
|---|---|
| `omem` | output buffer memory usage |
| `obl`, `oll` | output buffer length; output list length (replies are queued in the list when the buffer is full) |
| `qbuf`, `qbuf-free`, `argv-mem` | query buffer length and free space; incomplete arguments of the next command |
| `tot-mem` | total memory consumed by this client in its buffers |
| `idle` | idle time of the connection in seconds (leaked connections) |
| `flags` | `S` replica connection, `M` master, `P` Pub/Sub subscriber, `O` MONITOR, `x` in MULTI/EXEC, `b` blocking operation, `N` no special flag, `t` tracking (client-side caching) |
| `name` | set by apps with `CLIENT SETNAME`: do it, it makes this list useful |
`ssub` (shard channels) was added in 7.0.3 and `lib-name`/`lib-ver` are standard fields. New fields are added
over time, so parsers should skip unknown ones.
Overall: `INFO clients` (`connected_clients`, `blocked_clients`) and `INFO memory`
(`mem_clients_normal`, `mem_clients_slaves`, `mem_not_counted_for_evict`).

Find the worst offenders:
```bash
redis-cli CLIENT LIST | awk '{for(i=1;i<=NF;i++) if($i ~ /^omem=/){split($i,a,"="); print a[2], $0}}' | sort -nr | head
```

## Output buffer limits
```
client-output-buffer-limit normal  0 0 0          # default: unlimited for normal clients
client-output-buffer-limit replica 256mb 64mb 60  # hard limit, soft limit, soft seconds
client-output-buffer-limit pubsub  32mb 8mb 60
```
A client is disconnected immediately once the hard limit is reached, or if the soft limit is reached and
stays reached continuously for the given seconds. Zero disables a limit. Classes: `normal` (includes
MONITOR clients), `replica`, and `pubsub` (clients subscribed to at least one channel or pattern).
- **pubsub**: subscribers receive data in a push fashion; the default limit protects the server from slow ones.
- **replica**: during a full sync the master buffers writes for the replica. If writes during the RDB
  transfer exceed the limit, the replica is disconnected and has to start the sync again, which can loop.
  Raise it (for example `512mb 256mb 120`) on write-heavy masters. A replica limit lower than
  `repl-backlog-size` is ignored: the backlog size is used.
- **normal**: unlimited by default because normal clients get data only after a request; only
  asynchronous clients can request faster than they read. Consider something like
  `normal 256mb 128mb 60` for rogue clients, accepting that offenders are dropped.
- `maxmemory-clients` (default 0 = off) is a separate cap on the memory of all normal and pubsub clients:
  Redis drops the connections using the most memory first ("client eviction").
- `INFO memory` field `mem_not_counted_for_evict` reports transient replica and AOF buffers that are not
  counted for key eviction; they still use RAM.

## Act
```
CLIENT KILL ID 1287
CLIENT KILL ADDR 10.0.3.4:51234
CLIENT KILL USER batch_user
CLIENT NO-EVICT ON       # 7.0+: exempt this connection from client eviction
CLIENT NO-TOUCH ON       # 7.2+: this connection does not update key LRU/LFU stats
```
`CLIENT KILL` with filters returns the number of clients killed; filters combine with AND, and the calling
client is skipped unless `SKIPME NO`.
Idle leaks: `timeout 300` in the config closes clients idle for 300 s. It does not apply to replicas,
masters, blocked clients or Pub/Sub clients.

## Verify
`mem_clients_normal` returns to a small value, the offender (by name or addr) is fixed in the app, and the log
line `Client ... scheduled to be closed ASAP for overcoming of output buffer limits.` stops repeating.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): CLIENT LIST, CLIENT KILL,
CLIENT NO-EVICT, CLIENT NO-TOUCH, INFO, plus `redis.conf`, `src/networking.c` and `src/timeout.c` from the
redis/redis repository. Confirmed: field names and meanings, flag letters, `ssub` since 7.0.3, hard/soft limit
semantics and the three default limit lines, the replica limit versus `repl-backlog-size` rule,
`maxmemory-clients`, KILL filters, NO-EVICT (7.0.0) and NO-TOUCH (7.2.0), which clients `timeout` skips, the
log message text. Removed: the claim that `maxmemory` ignores replica and AOF buffers "in recent versions"
(replaced by the documented `mem_not_counted_for_evict` field), and the `x`/`b` flag descriptions were
corrected to the documented wording.
Method: documentation only; no commands were run.
