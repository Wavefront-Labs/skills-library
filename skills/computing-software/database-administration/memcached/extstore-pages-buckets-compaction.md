---
id: computing-software.database-administration.memcached.extstore-pages-buckets-compaction
name: extstore-pages-buckets-compaction
category: computing-software
field: database-administration
product: memcached
tags: [extstore, compaction, ext-max-frag, ext-drop-unread, page-buckets]
level: sme
status: docs-checked
description: "Understand extstore page buckets and compaction settings ext_max_frag, ext_drop_unread, ext_compact_under, ext_drop_under, ext_low_ttl."
sources:
  - https://docs.memcached.org/features/flashstorage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Pages are grouped in buckets: default, large items (>512k), compacted items, and an optional low-TTL bucket. Low-TTL pages are never compacted, avoiding write amplification; once all items expire the page is reclaimed whole.

Example: TTLs of 86400 and 2400 s: setting `ext_low_ttl` to 2400 or higher colocates the 2400 s items.

When flash is nearly full, pages are compacted or evicted:
- `ext_compact_under`: if fewer than this many pages are free, start compacting. Default 1/4 of pages.
- `ext_max_frag` (e.g. 0.5): rewrite pages at least that empty; if none qualify, the oldest page is evicted.
- `ext_drop_unread`: if no page qualifies, compact anyway but rewrite only new or frequently accessed items (not COLD LRU). More writing than evicting, higher hit ratio.
- `ext_drop_under`: with drop_unread, compact and drop COLD data below this many free pages; defaults to compact_under.

Mechanics: deleting or overwriting items never writes to flash; pages track byte and object counts and are recycled by version number when empty. Compaction reads whole pages back and rewrites survivors.

Too much write load: add RAM and tune these.

## Checked

2026-11-04. Confirmed against the Flash Storage page (page buckets, ext_low_ttl, ext_compact_under, ext_max_frag, ext_drop_unread, ext_drop_under, deletes and overwrites never write). Removed: the claim that 2400 s exactly is the ext_low_ttl value (page says 2400 or higher).

Method: documentation only; no commands were run.
