---
id: computing-software.database-administration.memcached.lru-crawler-expiry-reclaim
name: lru-crawler-expiry-reclaim
category: computing-software
field: database-administration
product: memcached
tags: [lru-crawler, expired-items, crawler-reclaimed, reclaim, background-thread]
level: advanced
status: docs-checked
description: "Reclaim expired items proactively with the LRU crawler: enable, sleep, tocrawl, crawl classes, and what the stats show."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/serverguide/performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Memcached expires lazily, so expired items sit in memory until looked at. Since 1.5.0 (or earlier with `-o modern`) a background thread scans the cache and frees expired items. The LRU crawler walks from tail to head of slab classes freeing expired items; useful with a mix of long and short TTLs that are rarely accessed. It is not required for normal usage and can add small latency and CPU.

```
lru_crawler enable|disable
lru_crawler sleep <microseconds>    (0 disables sleep, max 1000000)
lru_crawler tocrawl <32u>           (max items inspected per class per run)
lru_crawler crawl <1,3,10|all>
```
`crawl` replies `OK`, `BUSY` (a run is in progress; it cannot be stopped or restarted until done) or `BADCLASS`.

Watch `crawler_reclaimed`, `crawler_items_checked`, `lru_crawler_starts` in `stats`, and `crawler_reclaimed` per class in `stats items`.

`stats settings` shows `lru_crawler`, `lru_crawler_sleep`, `lru_crawler_tocrawl`.

## Checked

2026-11-04. Confirmed against protocol.txt (lru_crawler enable, sleep and its 0 and 1000000 bounds, tocrawl, crawl, OK/BUSY/BADCLASS, crawler stats and settings) and the Performance page (1.5.0, -o modern). Removed: nothing.

Method: documentation only; no commands were run.
