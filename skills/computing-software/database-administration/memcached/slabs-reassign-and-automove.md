---
id: computing-software.database-administration.memcached.slabs-reassign-and-automove
name: slabs-reassign-and-automove
category: computing-software
field: database-administration
product: memcached
tags: [slabs-reassign, slabs-automove, slab-page-mover, slab-reassign, rebalance]
level: advanced
status: docs-checked
description: "Move slab pages between classes at runtime with slabs reassign, and enable the background automover with slabs automove 0/1/2."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Both commands are marked in protocol.txt as subject to change.

Manual move:
```
slabs reassign <source class> <dest class>
```
Source -1 means pick from any valid class. Replies: `OK` (page scheduled), `BUSY`, `BADCLASS`, `NOSPARE` (source has no spare pages), `NOTFULL` (dest must be full), `UNSAFE`, `SAME`.

Automover (background thread):
```
slabs automove <0|1|2>      -> OK
```
- 0: standby.
- 1: return pages to a global pool when a class has more than 2 pages' worth of free chunks; pages are reassigned as needed.
- 2: very aggressive, moves a page on every eviction; do not run long unless access patterns are well understood.

Check state with `stats` (`slab_reassign_running`, `slabs_moved`, `slab_global_page_pool`) and `stats settings` (`slab_reassign`, `slab_automove`).

Lowering the limit with `cache_memlimit` (argument in megabytes) can release free memory back to the OS asynchronously when slab reassignment and the automover are enabled.

## Checked

Confirmed 2026-11-09: both commands marked subject to change; `slabs reassign` syntax, source -1 and all reply codes; `slabs automove` modes 0, 1 and 2 and their descriptions; stats `slab_reassign_running`, `slabs_moved`, `slab_global_page_pool`; settings `slab_reassign` and `slab_automove`; `cache_memlimit` behaviour (protocol.txt). Reworded the cache_memlimit sentence to match the text.

Method: docs-checked 2026-11-09 against memcached doc/protocol.txt
