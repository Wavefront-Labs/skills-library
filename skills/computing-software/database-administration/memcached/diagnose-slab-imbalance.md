---
id: computing-software.database-administration.memcached.diagnose-slab-imbalance
name: diagnose-slab-imbalance
category: computing-software
field: database-administration
product: memcached
tags: [slab-imbalance, slab-rebalance, total-pages, evictions, automove]
level: advanced
status: docs-checked
description: "Detect when memory is assigned to the wrong slab classes by comparing evictions per class with total_pages."
sources:
  - https://docs.memcached.org/serverguide/maintenance/
  - https://docs.memcached.org/serverguide/performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Why it happens: the Performance page says memory is split (by default) into 1 megabyte pages, assigned to slab classes as needed, and once a page is assigned to a class it is never moved (that page describes the classic behaviour). If 80% of pages end up in class 3, less memory is available for class 4. Each class has its own statistical counters and its own LRU.

Diagnosis (Maintenance page):
1. Monitor the global `evictions` stat.
2. Monitor `evicted` and `evicted_nonzero` per slab in `stats items`.
3. Read `total_pages` from `stats slabs` and overlay it on the eviction numbers.
4. If the slabs with the most evictions line up with the slabs holding the most pages, you might legitimately be out of memory. You can also correlate the per-slab hit rate with the number of pages.
5. If the slabs with the most evictions do not line up with the pages, you need to restart memcached so it can reallocate memory.

Recent versions (1.4.25 and later) have well tuned automated features for repairing this without a restart; see the release notes and protocol.txt (and the slabs-reassign-and-automove skill).

## Checked

2026-11-04. Confirmed against the Maintenance page (Slab imbalance) and the Performance page (pages and slab classes). Removed: nothing factual; reworded step 4 to the page's two-way test.

Method: documentation only; no commands were run.
