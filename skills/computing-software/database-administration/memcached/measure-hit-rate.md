---
id: computing-software.database-administration.memcached.measure-hit-rate
name: measure-hit-rate
category: computing-software
field: database-administration
product: memcached
tags: [hit-rate, get-hits, get-misses, cache-efficiency, stats]
level: practitioner
status: docs-checked
description: "Compute global and per-slab hit rate from get_hits and get_misses and avoid misreading misses from never-cached flags."
sources:
  - https://docs.memcached.org/serverguide/maintenance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Hitrate is defined as `get_hits / (get_hits + get_misses)`. The higher the better; watch that it is higher than you expect and whether it changes with time or releases of your application.

Per slab: an actual per-slab hit rate cannot be calculated because a get miss does not know how large the item could have been, but you can monitor `get_hits` and `cmd_set` per slab via `stats slabs`. Watch that `get_hits` is usually above `cmd_set` (more fetches than updates is often what you want), and watch for changes over time.

Looks can be deceiving: a low hit rate and a high eviction rate do not necessarily mean you need more memory.
- Your application sets large numbers of keys, most of which are never used again: this causes a high eviction count even though the data was not important. Audit what the application stores.
- Your application tests for keys on most requests that do not exist and are not recached, such as flags or values for a buggy user: many get_misses are accounted for by this. A workaround is to have the app recache a flag with a value of "not set" so the flag stays in cache and does not throw off hit rate calculations.

## Checked

2026-11-04. Confirmed against the Maintenance page (Global hitrate, Hitrate per slab, Looks can be Deceiving). Removed: the closing "sample counters twice and compute deltas" line, which the page does not state.

Method: documentation only; no commands were run.
