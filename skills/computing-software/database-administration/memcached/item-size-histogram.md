---
id: computing-software.database-administration.memcached.item-size-histogram
name: item-size-histogram
category: computing-software
field: database-administration
product: memcached
tags: [stats-sizes, track-sizes, size-histogram, metadump, slab-factor]
level: advanced
status: docs-checked
description: "Build an item size histogram with -o track_sizes and stats sizes, or lru_crawler metadump, to tune the slab growth factor."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/serverguide/maintenance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`stats sizes` returns `STAT <size> <count>`: an approximate item size (within 32 bytes) and the approximate number of items in that 32-byte range, as if there were a slab class for every 32 bytes. Use it to decide whether adjusting the slab growth factor would save memory overhead; for example, more classes in the lower range could fit items more snugly if most are under 200 bytes.

Enable at start time with `-o track_sizes` (low overhead). If disabled, `stats sizes` returns `STAT sizes_status disabled`; on an error it returns `STAT sizes_status error` and `STAT sizes_error [error_message]`.

Warnings:
- Before 1.4.27, `stats sizes` locks the cache server while it iterates the items (the Maintenance page says it can hang the cache while it scans all items). 1.4.27 and later are safe.
- From 1.4.27 to 1.6.24 the feature could be toggled at runtime with `stats sizes_enable` / `stats sizes_disable`, but that was not thread safe and could crash the server; the start-time option remains.
- For an already running instance, you can make a histogram with `lru_crawler metadump` and process the output; this does not block the server.

`stats settings` shows `track_sizes`.

## Checked

2026-11-04. Confirmed against protocol.txt "Item size statistics" and settings table, and the Maintenance page (stats sizes warning). Removed: nothing; wording tightened to the page.

Method: documentation only; no commands were run.
