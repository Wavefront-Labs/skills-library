---
id: computing-software.database-administration.redis.slowlog-analysis
name: slowlog-analysis
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, slowlog, performance, slow-commands, latency, big-keys, slowlog-log-slower-than]
level: practitioner
status: docs-checked
description: "Use the Redis SLOWLOG to find commands that block the main thread, tune slowlog-log-slower-than and slowlog-max-len, and fix the usual culprits."
sources:
  - https://redis.io/docs/latest/commands/slowlog-get/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency-monitor/
  - https://raw.githubusercontent.com/redis/redis/unstable/redis.conf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SLOWLOG

**Goal:** identify which commands take execution time on the main thread, since one slow command delays every client.

## Configure
```text
CONFIG SET slowlog-log-slower-than 10000   # microseconds (10 ms, the default); 0 logs every command; a negative value disables the slow log
CONFIG SET slowlog-max-len 1024            # entries kept in memory (default 128; the oldest is dropped)
```
Measures only command execution, not network, I/O or queueing time. `SLOWLOG RESET` reclaims the memory used by the log.

## Read
```text
SLOWLOG LEN
SLOWLOG GET 20
1) 1) (integer) 4512                 # id
   2) (integer) 1729070000           # unix time
   3) (integer) 84211                # duration in microseconds
   4) 1) "KEYS" 2) "session:*"       # command and arguments (truncated when long)
   5) "10.0.3.17:52344"              # client address and port
   6) "worker-7"                     # client name, if set with CLIENT SETNAME
SLOWLOG RESET
```
`SLOWLOG GET` returns the latest 10 entries by default; `-1` returns all. The entry id is unique and not reset until a server restart, so a script can use it to avoid processing an entry twice. Recent versions add a seventh element, the total argument count (8.10), and truncate long argument lists (`slowlog-entry-max-argc`, 32 by default in redis.conf; the SLOWLOG GET page calls it `slowlog-max-argc`).

## Usual culprits and fixes
| Command | Fix |
|---|---|
| `KEYS pattern` | `SCAN` with `MATCH`/`COUNT`; deny `KEYS` with an ACL rule |
| `HGETALL`/`SMEMBERS`/`LRANGE 0 -1`/`ZRANGE 0 -1` on big keys | HSCAN/SSCAN/paginated ranges; split big keys |
| `DEL` of a big key | `UNLINK` (background free); `lazyfree-lazy-*` settings |
| `SORT`, `SUNION`, `ZUNIONSTORE` on large sets | Precompute, smaller inputs |
| `EVAL`/`FCALL` long scripts | Shorter scripts; `busy-reply-threshold` (old name `lua-time-limit`) |
| `FLUSHALL` | `FLUSHALL ASYNC` |
| `INFO`/`CLIENT LIST` with thousands of clients | Poll less often |

Group by command over time to spot patterns: export `SLOWLOG GET` periodically from your monitoring system.

## Relation to latency
SLOWLOG excludes I/O, so it misses latency from fork (BGSAVE), AOF fsync, swapping or transparent huge pages. Use the latency monitor (`latency-monitor-threshold`, `LATENCY LATEST`, `LATENCY DOCTOR`) and `redis-cli --intrinsic-latency` for those.

## Verify
`CONFIG SET slowlog-log-slower-than 0`, run any command, and confirm it appears in `SLOWLOG GET 1` with its duration; then restore the threshold (and keep the log from growing: threshold 0 logs everything).

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): SLOWLOG GET, latency monitoring page, redis-cli
reference, plus `redis.conf` and `src/config.c` from the redis/redis repository. Confirmed: defaults (10000 us, 128), negative
disables and zero logs everything, entry fields and order, default count 10 and `-1`, unique id, `slowlog-entry-max-argc`
(the command page uses another name), `SLOWLOG RESET` reclaims memory, the latency tools. Fixed: the verification step used
`DEBUG SLEEP`, which is not documented (DEBUG is an internal command). Removed: "(4.0+)" on client fields, and the
Prometheus redis_exporter metric names (third party).
Method: documentation only; no commands were run.
