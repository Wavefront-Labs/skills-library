---
id: computing-software.database-administration.redis.latency-monitor-and-latency-doctor
name: latency-monitor-and-latency-doctor
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, redis-latency, redis-memory-optimization, latency-monitor, latency-doctor, intrinsic-latency, fork-latency, transparent-huge-pages, latency-spikes]
level: advanced
status: docs-checked
description: "Find the cause of Redis latency spikes with the latency monitor, LATENCY DOCTOR and --intrinsic-latency: slow commands, fork, AOF fsync, THP, swapping, or the network."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency-monitor/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing Redis latency

**Goal:** turn "Redis is sometimes slow" into one named cause.

## 1. Rule out the host
On the Redis host (not via network), run for a minute:
```bash
redis-cli --intrinsic-latency 60
```
This measures the latency floor of the host (it does not connect to Redis and saturates one
core). The docs show 115 microseconds on an entry-level physical server and 9.7 ms on a busy
VM, up to 40 ms on some VMs: Redis cannot do better than this baseline.

## 2. Client-side view
```bash
redis-cli -h <host> --latency-history           # min/avg/max over time
```
Spikes here but not in server metrics = network or client (connection pool
exhaustion, GC pauses).

## 3. Enable the latency monitor
```
CONFIG SET latency-monitor-threshold 10     # ms; record events slower than this (0 = off, default)
LATENCY LATEST                              # event, last timestamp, last ms, max ms
LATENCY HISTORY command
LATENCY DOCTOR                              # human-readable analysis and advice
LATENCY RESET
```
Event names and their usual fixes:
| Event | Cause | Fix |
|---|---|---|
| `command` / `fast-command` | Slow O(N) commands (KEYS, big ZRANGE/SMEMBERS/HGETALL, Lua) | SLOWLOG to find them; SCAN, pagination |
| `fork` | BGSAVE / AOF rewrite fork copies page tables (docs examples: about 9-13 ms per GB on physical hosts and VMware, far more on some Xen VMs) | Smaller instances, disable THP, persistence on replica only |
| `aof-fsync-always`, `aof-write-pending-fsync` | Disk can't keep up with fsync | `appendfsync everysec`, faster disk, `no-appendfsync-on-rewrite yes` |
| `expire-cycle` | Mass expiry of keys with the same TTL | Add jitter to TTLs |
| `eviction-cycle`, `eviction-del` | maxmemory eviction of big keys | `lazyfree-lazy-eviction yes`, smaller values |

## 4. Kernel checks
- Transparent huge pages: `cat /sys/kernel/mm/transparent_hugepage/enabled` should
  show `never`; with THP enabled a fork can cause copy-on-write of almost the whole
  process memory, with large latency and memory cost.
- Swapping: check the `Swap:` fields in `/proc/<pid>/smaps` (and `vmstat 1`, columns si/so);
  swapped Redis pages cause latency. Set `maxmemory` with headroom.

## Gotchas
- The monitor costs almost nothing; leave a threshold set in production.
- One slow command blocks all clients: Redis executes commands on one main thread.

## Verify
After the fix, `LATENCY LATEST` max values stay under the threshold over a full
day including persistence runs.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the latency-monitor page: `latency-monitor-threshold` default 0 (off) and near-zero cost, LATENCY LATEST/HISTORY/RESET/GRAPH/DOCTOR, event names (`command`, `fast-command`, `fork`, `aof-fsync-always`, `aof-write-pending-fsync`, `expire-cycle`, `eviction-cycle`, `eviction-del`). Confirmed from the latency troubleshooting page: `redis-cli --intrinsic-latency` runs on the server and its sample numbers, `--latency-history`, fork times per GB, THP disable command and copy-on-write effect, smaps Swap check, `no-appendfsync-on-rewrite`, expiry cycle behaviour, the single-threaded blocking nature. Removed unconfirmed: the a few hundred microseconds threshold, the THP startup warning, `-i 5`, vm.swappiness advice, 10-20 ms per GB.
Method: documentation only; no commands were run.
