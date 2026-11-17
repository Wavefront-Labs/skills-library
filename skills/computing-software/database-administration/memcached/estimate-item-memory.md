---
id: computing-software.database-administration.memcached.estimate-item-memory
name: estimate-item-memory
category: computing-software
field: database-administration
product: memcached
tags: [item-overhead, sizes-utility, key-size, memory-per-item, slab-chunk]
level: advanced
status: docs-checked
description: "Estimate memory per item (key, item struct, data) and measure struct sizes with the ./sizes utility built with memcached."
sources:
  - https://docs.memcached.org/serverguide/performance/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

An item uses space for the full length of its key, the internal data structure for an item, and the length of the data. Items are pushed into the slab class of the nearest fit.

You can discover how large an item is by compiling memcached on your system and running the `./sizes` utility that is built. The docs example prints `Item (no cas) 32`, `Item (cas) 40`, `Settings 88` and `Connection 320`, so in that example an item with CAS is 8 bytes larger than one without.

Compare with reality using `stats slabs` (`chunk_size`, `chunks_per_page`) and `stats items` (`mem_requested`); per protocol.txt, `(total_chunks * chunk_size) - mem_requested` shows memory wasted in a slab class.

## Checked

2026-11-04. Confirmed against the Performance page ("How Much Memory Will an Item Use", sizes output) and protocol.txt (slab and item statistics, mem_requested footnote). Removed: the cross-reference to a key-size skill.

Method: documentation only; no commands were run.
