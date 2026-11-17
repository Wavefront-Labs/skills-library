---
id: computing-software.database-administration.redis.info-memory-and-memory-doctor
name: info-memory-and-memory-doctor
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, info-memory, memory-doctor, memory-stats, memory-usage, bigkeys, memkeys, oom]
level: practitioner
status: docs-checked
description: "Read INFO memory, MEMORY STATS/DOCTOR/USAGE and redis-cli --bigkeys/--memkeys to find what uses Redis memory and size maxmemory with headroom."
sources:
  - https://redis.io/docs/latest/commands/info/
  - https://redis.io/docs/latest/commands/memory-stats/
  - https://redis.io/docs/latest/commands/memory-usage/
  - https://redis.io/docs/latest/commands/memory-doctor/
  - https://redis.io/docs/latest/develop/tools/cli/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/admin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# INFO memory and MEMORY DOCTOR

**Goal:** explain where every gigabyte of a Redis process goes before it hits maxmemory or the OOM killer.

## INFO memory: fields that matter
```text
redis-cli INFO memory
used_memory_human          # memory allocated by Redis through its allocator
used_memory_rss_human      # resident set size, what the OS sees
used_memory_peak_human
used_memory_dataset / used_memory_overhead    # dataset = used_memory minus overhead
mem_fragmentation_ratio    # used_memory_rss / used_memory (see defrag skill)
maxmemory_human / maxmemory_policy
mem_clients_normal         # memory used by normal clients
mem_replication_backlog
mem_aof_buffer             # AOF and AOF rewrite buffers
mem_not_counted_for_evict  # transient replica and AOF buffers not counted for key eviction
```
Starting with Redis 7.0 replica buffers share memory with the replication backlog, so `mem_clients_slaves` can show 0.

## MEMORY DOCTOR and STATS
```text
MEMORY DOCTOR      # reports memory-related issues the server sees and advises remedies
MEMORY STATS       # breakdown: overhead.total, keys.count, keys.bytes-per-key, dataset.bytes, dataset.percentage, clients.normal, ...
```
`dataset.percentage` is `dataset.bytes` as a share of total memory; a low value means overhead dominates (many tiny keys, big buffers).

## Find the heavy keys
```bash
redis-cli --bigkeys          # keys with many elements, per type (uses SCAN, safe on a busy server; throttle with -i)
redis-cli --memkeys          # keys using the most memory
redis-cli --keystats         # both, plus size distribution
redis-cli MEMORY USAGE session:abc SAMPLES 0    # SAMPLES 0 samples all nested values (default 5)
```
`--memkeys` and `--bigkeys` also work against cluster replicas. For an offline analysis of a full RDB, use a
tool on another machine.

## Usual suspects
| Symptom | Cause |
|---|---|
| `mem_clients_normal` huge | Slow subscriber or MONITOR client; huge pipelined replies |
| Overhead high, many keys | Per-key overhead: bucket into hashes |
| RSS >> used | Fragmentation, or freed memory the allocator did not return to the OS (RSS tracks the peak) |
| Spikes during BGSAVE or AOF rewrite | Copy-on-write: a write-heavy instance can use up to 2 times its normal memory |
| Keys without TTL growing | Missing expiry; `INFO keyspace` shows `expires` vs `keys` |

## Sizing rule
Provision for peak usage, set an explicit `maxmemory`, and leave room for Redis overhead, fragmentation,
and the copy-on-write cost of saving. The administration page's example: with 10 GB free, set `maxmemory`
to 8 or 9 GB. In containers set it below the container limit. Swap or an OOM kill can otherwise take Redis down.

## Verify
After the fix, `MEMORY DOCTOR` reports no issues and `used_memory` vs `maxmemory` has the planned headroom at peak.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): INFO (memory, keyspace sections),
MEMORY STATS, MEMORY USAGE, MEMORY DOCTOR, redis-cli reference, administration page, memory optimization page.
Confirmed: INFO field names and definitions, MEMORY STATS metric names, SAMPLES default 5 and `SAMPLES 0`, MEMORY
DOCTOR purpose, `--bigkeys`/`--memkeys`/`--keystats`, the RSS-tracks-peak explanation, the 2x copy-on-write note.
Fixed: the sizing heuristic "60-75% of RAM" was replaced by the documented example (8 or 9 GB of 10 GB free).
Removed: version tags on `--memkeys`, the third-party tool names (rdb-tools, redis-rdb-cli), and "RSS can almost double"
(the documentation says up to 2 times).
Method: documentation only; no commands were run.
