---
id: computing-software.database-administration.redis.fragmentation-and-active-defrag
name: fragmentation-and-active-defrag
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, redis-memory-optimization, activedefrag, mem-fragmentation-ratio, jemalloc, memory-purge, allocator-fragmentation]
level: practitioner
status: docs-checked
description: "Read Redis mem_fragmentation_ratio correctly and reclaim fragmented memory online with activedefrag thresholds and CPU limits, or MEMORY PURGE."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/
  - https://raw.githubusercontent.com/redis/redis/unstable/redis.conf
  - https://redis.io/docs/latest/commands/memory-purge/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fragmentation and active defrag

**Goal:** get back RSS lost to fragmentation after mass deletes/expiry without restarting.

## Reading the ratio
```text
INFO memory
mem_fragmentation_ratio:1.85
allocator_frag_ratio:1.60      # jemalloc external fragmentation: what activedefrag fixes
allocator_rss_ratio:1.05
mem_fragmentation_bytes:...
```
- `mem_fragmentation_ratio` is `used_memory_rss / used_memory` and includes process overhead beyond fragmentation; a high ratio with only a few MB in `mem_fragmentation_bytes` is harmless.
- `allocator_frag_ratio` (`allocator_active / allocator_allocated`) is the true external fragmentation metric; a high `allocator_rss_ratio` (`allocator_resident / allocator_active`) suggests pages the allocator can release to the OS.
- The ratio is unreliable when peak memory use was far above current use: Redis does not always return freed memory to the OS.

Common trigger: many keys with varied sizes deleted/expired, leaving partially empty allocator pages.

## Active defrag (needs Redis built with its bundled jemalloc)
```text
CONFIG SET activedefrag yes
active-defrag-ignore-bytes 100mb          # start only if fragmentation waste > 100 MB
active-defrag-threshold-lower 10          # and fragmentation > 10%
active-defrag-threshold-upper 100         # max effort above 100%
active-defrag-cycle-min 1                 # % CPU at lower threshold
active-defrag-cycle-max 25                # % CPU at upper threshold
active-defrag-max-scan-fields 1000        # big collections processed incrementally
```
It moves values to compact pages in the background. Watch `INFO stats` `active_defrag_running`, `active_defrag_hits`, `active_defrag_key_hits` and latency.

## MEMORY PURGE
`MEMORY PURGE` asks the allocator to purge dirty pages so they can be reclaimed. It is implemented only for jemalloc; with another allocator it does nothing and returns OK.

## Last resort
Fail over to a freshly synced replica (full resync rebuilds memory compactly), then restart the old primary.

## Gotchas
- Works only if Redis was compiled with the copy of jemalloc shipped in its source.
- Defrag CPU competes with the main thread: keep `cycle-max` modest on latency-sensitive instances.

## Verify
`allocator_frag_ratio` trends down and RSS drops while p99 latency stays within your SLO.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from redis.conf (8.2): activedefrag is off by default and works only with the bundled jemalloc; `active-defrag-ignore-bytes 100mb`, `threshold-lower 10`, `threshold-upper 100`, `cycle-min 1`, `cycle-max 25`, `max-scan-fields 1000` and their meanings; `CONFIG SET activedefrag yes`. Confirmed from INFO: definitions of `mem_fragmentation_ratio`, `mem_fragmentation_bytes`, `allocator_frag_ratio`, `allocator_rss_ratio`, `active_defrag_running`, `active_defrag_hits`, `active_defrag_key_hits`. Confirmed MEMORY PURGE is jemalloc-only. Removed unconfirmed: the 1.0-1.5 and 1.5 ratio thresholds, 'Redis 4+', convergence time.
Method: documentation only; no commands were run.
