---
id: computing-software.database-administration.memcached.soft-expiration-recache
name: soft-expiration-recache
category: computing-software
field: database-administration
product: memcached
tags: [soft-expiration, recache, ttl, stampede, jitter]
level: advanced
status: docs-checked
description: "Avoid stampedes by embedding a soft timeout inside cached objects and recaching early under a lock or randomly."
sources:
  - https://docs.memcached.org/userguide/usecases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Store the object with a hard expiry later than the soft one: if it should live an hour, set it to expire in 1.5 hours or more, and embed a soft timeout inside the value.

On fetch past the soft timeout, pick a strategy:
- Take the add lock; the winner recaches, losers return the old item.
- Also record a hard timeout (or assume soft + constant) and recache randomly with probability rising with age.
- Dispatch an asynchronous job to recache.

The cached object can still vanish for other reasons (restart, LRU, eviction). Treat this as mitigation, not your only defence.

Job servers such as Gearman can coalesce duplicates: asynchronous jobs collapse, synchronous ones broadcast one result to all waiters.

Server-side equivalents: `mg key v R30` (early recache) and `md I` (stale). See those skills.

## Checked

Confirmed 2026-11-09: soft timeout embedded in the object with a later hard expiry, the three recache strategies, the warning that the object can vanish for other reasons, Gearman coalescing of asynchronous and synchronous jobs (Use Cases page, Scaling expiration and Gearmand sections); `R` early recache and `md I` stale (Meta protocol page). Nothing removed.

Method: docs-checked 2026-11-09 against docs.memcached.org Use Cases and Meta protocol pages
