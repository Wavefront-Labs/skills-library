---
id: computing-software.database-administration.memcached.probabilistic-hot-key-cache
name: probabilistic-hot-key-cache
category: computing-software
field: database-administration
product: memcached
tags: [hot-keys, local-cache, h-flag, l-flag, client-side-cache]
level: advanced
status: docs-checked
description: "Detect hot keys without coordination using mg h and l flags and promote them to a client-side cache probabilistically."
sources:
  - https://docs.memcached.org/protocols/meta/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Request `mg foo v h l` -> `VA 4 h1 l5`. `h` returns 0 or 1 depending on whether the item has been requested since it was stored; `l` is the seconds since last access (both reflect the state before this request).

Rule from the docs: `if (h == 1 && l < 5 && random(1000) == 0) { add_to_local_cache(it); }`. The random factor is a weight that could reflect other factors (database, network or system load, local cache hit rate). Keys that suddenly get a lot of traffic filter in slowly, with the highest traffic keys cached very quickly. No live coordination between servers is needed to discover or communicate hot keys; implementations must decide how validation is done.

Invalidation options:
- For truly hot keys, cache them in a client for only a couple of seconds; a "shadow key" with a slightly longer expiration (30 seconds or so) can signal a client to recache immediately if seen again. Total requests to memcached will be higher than in a perfect system.
- Especially useful for items that are large or CPU intensive to deserialize: periodically revalidate. `mg foo v h l c` also returns the CAS (for example `c500`); a client can schedule asynchronous background revalidations with `mg foo c`, which returns `HD c500` with no value, so only the CAS is compared.
- protocol.txt also documents `C<token>` on mg: with `v`, the value is returned only if the CAS does not match (otherwise `HD`).

## Checked

2026-11-04. Confirmed against the Meta page (Probabilistic Hot Cache, Hot Key Cache Invalidation) and protocol.txt (mg C flag). Removed: the loose "mg foo v c500-style" example, replaced by the documented C flag.

Method: documentation only; no commands were run.
