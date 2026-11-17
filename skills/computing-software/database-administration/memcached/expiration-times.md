---
id: computing-software.database-administration.memcached.expiration-times
name: expiration-times
category: computing-software
field: database-administration
product: memcached
tags: [exptime, expiration, ttl, unix-time, clock]
level: practitioner
status: docs-checked
description: "Rules for exptime: 0 never expires, up to 30 days is relative, larger is Unix time, negative expires now, plus +/- 1 second accuracy."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/serverguide/performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

An expiration time sent by a client is either Unix time (seconds since January 1, 1970, as a 32-bit value) or a number of seconds from the current time. Storage commands (set/add/replace/append/prepend/cas), touch and gat all take one:
- 0: the item never expires (although it may be deleted from the cache to make room for other items).
- A relative number of seconds may not exceed 60*60*24*30 (30 days); a larger number is treated as a real Unix time rather than an offset.
- Negative: the item is immediately expired (stated for storage commands).

Gotchas:
- A TTL of 1 will sometimes expire immediately. Time is internally updated on second boundaries, so expiration is roughly +/- 1 s, which affects very low TTLs proportionally more.
- Expiration values are stored as timestamps, so the OS clock must be correct: if the clock is set far into the past after storing items, they will not expire on time; jumping it forward can expire items prematurely.

Expiry is lazy: fetching an expired item frees it, and expired items found while storing are reused (see the lazy-expiration-curr-items skill). In meta commands the `t` flag returns the remaining TTL in seconds (-1 for unlimited).

## Checked

2026-11-04. Confirmed against protocol.txt "Expiration times", the storage command exptime description and mg flags, and the Performance page (clock accuracy, clock jumps, memory reclaim). Removed: the unstated warm-restart clock rule and the Verify line.

Method: documentation only; no commands were run.
