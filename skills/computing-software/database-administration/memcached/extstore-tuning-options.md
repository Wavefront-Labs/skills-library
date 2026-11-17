---
id: computing-software.database-administration.memcached.extstore-tuning-options
name: extstore-tuning-options
category: computing-software
field: database-administration
product: memcached
tags: [extstore, ext-threads, ext-wbuf-size, ext-item-size, tuning]
level: advanced
status: docs-checked
description: "Tune extstore with ext_page_size, ext_wbuf_size, ext_threads, ext_item_size, ext_low_ttl and ext_recache_rate; defaults and why."
sources:
  - https://docs.memcached.org/features/flashstorage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Use `-o key=value,...`. Defaults and guidance:
- `ext_page_size` 64M: change only for multi-megabyte values.
- `ext_wbuf_size` 8M: one buffer per bucket (32 MB reserved by default); cannot exceed page size; larger helps write rate.
- `ext_threads` 1: raise if read latency is high while the drive is idle; stay at 8 or fewer.
- `ext_item_size` 512 bytes: only larger items are flushed. Raise it to flush only very large objects (a good place to start; 64k+ frees the most RAM); lower to save RAM with short keys.
- `ext_low_ttl` (off): TTLs below it are colocated.
- `ext_recache_rate` 2000: item read more than once in the last minute has a 1-in-N chance of returning to RAM. Keep it high; recaches fragment the disk.

Runtime: `extstore item_size|item_age|low_ttl|recache_rate|compact_under|drop_under|max_frag|drop_unread <value>`.

Watch: `evictions` (RAM too small or flush too slow), very low `age` in high classes, disk latency (no internal latency metric), drive wear.

## Checked

2026-11-04. Confirmed against the Flash Storage page (defaults and guidance for each ext_* option, runtime extstore commands, what to watch). Removed: nothing.

Method: documentation only; no commands were run.
