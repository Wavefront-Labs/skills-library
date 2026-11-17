---
id: computing-software.database-administration.valkey.maxmemory-eviction-policies
name: maxmemory-eviction-policies
category: computing-software
field: database-administration
product: valkey
tags: [maxmemory, maxmemory-policy, eviction, allkeys-lru, volatile-ttl, noeviction, mem-not-counted-for-evict]
level: practitioner
status: docs-checked
description: "Valkey maxmemory and maxmemory-policy: eviction policies, replication buffer accounting, mem_not_counted_for_evict and how to monitor eviction."
sources:
  - https://valkey.io/topics/lru-cache/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`maxmemory` (in `valkey.conf` or `CONFIG SET`, e.g. `maxmemory 100mb`) caps dataset memory. 0 means unlimited, the default on 64-bit; 32-bit builds use an implicit 3 GB. At the limit, `maxmemory-policy` decides: error on writes, or evict.

Policies: `noeviction` (reject new values; on a replicated setup this applies to the primary), `allkeys-lru`, `allkeys-lfu`, `volatile-lru`, `volatile-lfu`, `allkeys-random`, `volatile-random`, `volatile-ttl` (shortest remaining TTL first). The `volatile-*` policies act like `noeviction` when no key has a TTL. LRU, LFU and `volatile-ttl` use approximated randomised algorithms. The policy can be changed at runtime; watch hits and misses in `INFO`.

Choosing: `allkeys-lru` for power-law popularity (the safe pick when unsure); `allkeys-random` for cyclic scans or uniform access; `volatile-ttl` when you hint expiry through TTL values. `volatile-lru`/`volatile-random` suit one instance mixing cache and persistent keys, but two instances is usually better. TTLs cost memory, so `allkeys-lru` is more efficient.

Replication and AOF buffers are not counted toward eviction, otherwise eviction output would feed back into more eviction. Set `maxmemory` lower on replicated setups. Eviction triggers when:
```
used_memory - mem_not_counted_for_evict > maxmemory
```
Read both fields in `INFO MEMORY`; in the page example 12498952 - 12336 = 12486616, far below 10737418240, so nothing is evicted. `INFO STATS` adds `total_eviction_exceeded_time` (ms spent above the limit).

Eviction runs per command: usage is checked, keys evicted, next command. A big operation (such as a large `SINTERSTORE`) can overshoot the limit noticeably for a while.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/lru-cache/ (page text read in full): maxmemory 100mb, 0 default on 64-bit, 3 GB implicit on 32-bit, all eight policies, volatile-* behaving like noeviction, approximated algorithms, rule-of-thumb choices, TTL memory cost, replication/AOF buffers excluded, mem_not_counted_for_evict formula and 12498952 example, total_eviction_exceeded_time, per-command eviction.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
