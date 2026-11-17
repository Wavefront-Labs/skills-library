---
id: computing-software.database-administration.memcached.lru-tune-mode-temp-ttl
name: lru-tune-mode-temp-ttl
category: computing-software
field: database-administration
product: memcached
tags: [lru, lru-tune, segmented-lru, temp-ttl, lru-maintainer]
level: advanced
status: docs-checked
description: "Tune memcached's LRU at runtime with lru tune, lru mode flat or segmented, and lru temp_ttl for the TEMP LRU."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The traditional model is "flat" mode, a single LRU chain per slab class. The newer model (with `-o modern` or `-o lru_maintainer`) is segmented into HOT, WARM and COLD, plus a TEMP LRU. See doc/new_lru.txt for details. You can tune while the daemon is running.

```
lru tune <percent hot> <percent warm> <max hot factor> <max warm age factor>
lru tune 10 25 0.1 2.0
lru mode <flat|segmented>
lru temp_ttl <ttl>
```
- The example caps HOT at 10% of the cache, or tail idle longer than 10% of COLD; WARM is up to 25% of the cache, or tail idle longer than 2x COLD.
- `mode segmented` requires `-o lru_maintainer` at start time. If switching from segmented to flat, the background thread pulls items from HOT and WARM into COLD.
- `temp_ttl`: if the TTL is less than zero, usage of the TEMP LRU is disabled. If zero or above, items set with a TTL lower than this go into the TEMP LRU and are unevictable until they naturally expire or are otherwise deleted or replaced.

Replies: `OK`, or `ERROR [message]` for a failure or improper arguments.

`stats settings` lists `hot_lru_pct`, `warm_lru_pct`, `hot_max_factor`, `warm_max_factor`, `temp_lru` and `temporary_ttl`; `stats items` has per-class `moves_to_cold`, `moves_to_warm`, `moves_within_lru` and `hits_to_hot`.

## Checked

2026-11-04. Confirmed against protocol.txt "LRU Tuning", the settings table and item statistics. Removed: nothing; wording aligned to the page.

Method: documentation only; no commands were run.
