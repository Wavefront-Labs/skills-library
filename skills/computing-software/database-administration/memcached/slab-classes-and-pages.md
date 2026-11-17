---
id: computing-software.database-administration.memcached.slab-classes-and-pages
name: slab-classes-and-pages
category: computing-software
field: database-administration
product: memcached
tags: [slab-allocator, slab-classes, chunk-size, vv, growth-factor]
level: advanced
status: docs-checked
description: "How -m memory splits into 1 MB pages, slab classes and chunks, and how to print the class table with -vv."
sources:
  - https://docs.memcached.org/serverguide/performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Memory from `-m` is reserved for item data, split by default into 1 MB pages. Pages are assigned to slab classes and cut into chunks of that class's size. Each class has its own counters and LRU, so memcached acts like many small caches.

See the classes: `./memcached -vv` prints lines such as `slab class 1: chunk size 80 perslab 13107` and `slab class 2: chunk size 104 perslab 10082`.

An item goes into the nearest fitting class: 50 bytes total (key + misc data + value) in the 80-byte class wastes 30; 90 bytes in the 104-byte class wastes 14.

Adjust class spacing with `-f` (default `growth_factor 1.25` in `stats settings`) once you know your size distribution (see the item size histogram skill).

Other memory: the hash table and per-connection buffers add up to a few percent over -m. Waste per class: `(total_chunks * chunk_size) - mem_requested` using `stats items`.

## Checked

2026-11-04. Confirmed against the Performance page (1 MB pages, slab classes, -vv output, nearest-fit waste, -f, extra memory). Removed: nothing.

Method: documentation only; no commands were run.
