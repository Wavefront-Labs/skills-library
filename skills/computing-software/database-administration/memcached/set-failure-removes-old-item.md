---
id: computing-software.database-administration.memcached.set-failure-removes-old-item
name: set-failure-removes-old-item
category: computing-software
field: database-administration
product: memcached
tags: [set-failure, store-no-memory, object-too-large, stale-data, set]
level: advanced
status: docs-checked
description: "A failed set on an existing key removes the old item, because memcached assumes you wanted to replace stale data."
sources:
  - https://docs.memcached.org/serverguide/performance/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A `set` can fail because there is no free memory, the object is too large, or another cause. When the key already existed, the failure usually removes the old item. Memcached assumes that issuing a set means the cached value is stale, and errs on the side of caution.

Consequence: after a failed set, the next get is a miss rather than an old value, so the application falls back to the source of truth. Do not treat failed sets as harmless no-ops, and do not expect the previous value to survive.

Counters: `store_too_large` (over `-I`), `store_no_memory` (the `-m` limit exhausted, relevant when `-M` is used), and per-class `outofmemory` in `stats items`.

Related: `outofmemory` counts failed stores when running with `-M` or when an eviction failed. Watch these counters if a hot key keeps disappearing after updates.

## Checked

Confirmed 2026-11-09: failed sets (no free memory, object too large, unknown cause) usually remove the existing item because memcached assumes the value is stale (Performance page, How It Handles set Failures); `store_too_large` (larger than the -I limit), `store_no_memory` and per-class `outofmemory` (protocol.txt stats sections). Removed the unsupported statement that -M makes memcached return errors instead of evicting.

Method: docs-checked 2026-11-09 against docs.memcached.org Performance page and memcached doc/protocol.txt
