---
id: computing-software.database-administration.memcached.diagnose-evictions
name: diagnose-evictions
category: computing-software
field: database-administration
product: memcached
tags: [evictions, evicted-nonzero, evicted-time, stats-items, lru]
level: practitioner
status: docs-checked
description: "Read evictions, evicted_nonzero and evicted_time in stats items to tell whether memcached is truly out of memory."
sources:
  - https://docs.memcached.org/serverguide/maintenance/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

An item is evicted if it still has time to live but ends up at the tail of the LRU when a new item must be allocated. Memcached tries a little to find an expired item at the tail but does not guarantee it.

`stats items` (per slab class, `items:<class>:<stat>`):
- `evicted`: items tossed early from that slab class.
- `evicted_nonzero`: evicted items that had an explicit expire time; `evicted - evicted_nonzero` are items that were stored forever.
- `evicted_time`: seconds since the last access of the most recently evicted item. If this is small you are evicting items that were recently used.
- `evicted_unfetched`: valid items evicted that were never touched after being set. `evicted_active`: valid items evicted that were recently touched but not yet moved to the top of the LRU again.
- `outofmemory`: times the slab class was unable to store a new item; this means you are running with -M or an eviction failed.

Procedure from the Maintenance page: watch the global `evictions` stat; look at `evicted` and `evicted_nonzero` per slab in `stats items`; read `total_pages` from `stats slabs` and overlay it. If the slabs with the most evictions line up with the slabs holding the most pages, you might legitimately be out of memory; if they do not line up, memory is misallocated (see diagnose-slab-imbalance).

A high eviction count does not always mean you need more memory: an application that sets many keys that are never used again also causes it, so audit what the application stores.

## Checked

2026-11-04. Confirmed against the Maintenance page (Evictions, Slab imbalance, Looks can be deceiving) and protocol.txt item statistics. Removed: the "(a real shortage)" gloss and the vague "refine the picture" line, replaced with the documented meanings.

Method: documentation only; no commands were run.
