---
id: computing-software.networking-hardware-and-wireless.unbound.cache-sizes-and-slabs
name: cache-sizes-and-slabs
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, msg-cache-size, rrset-cache-size, slabs, key-cache-size, memory]
level: advanced
status: docs-checked
description: "Size Unbound's message, RRset, key and negative caches and understand slabs, including the rule of thumb and memory overhead from the performance guide."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/core/performance.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache sizes and slabs
Defaults: `msg-cache-size` 4m, `rrset-cache-size` 4m, `key-cache-size` 4m, `neg-cache-size` 1m. Sizes accept k, m, g suffixes.

The performance guide: increase `rrset-cache-size` and `msg-cache-size`, with roughly twice as much rrset cache as msg cache (example `100m` and `50m`). Total memory can reach 2 to 2.5 times the configured cache size because of malloc overhead.

Slabs (`msg-cache-slabs`, `rrset-cache-slabs`, `infra-cache-slabs`, `key-cache-slabs`) reduce lock contention. Unconfigured, Unbound sets a power of 2 close to the thread count; they can be set explicitly if needed, and the value must be a power of 2. In forked mode each process has its own cache, so total usage is the per-process figure times the cores; the guide's forked example sets the slabs to 1.

`fast_reload` keeps the cache and can change cache size options, but does not work with any `*-slabs` option. `reload_keep_cache` needs cache sizes and the number of threads unchanged between reloads.

Check usage with `mem.cache.rrset` and `mem.cache.message` in extended statistics, and the `msg.cache.max_collisions` and `rrset.cache.max_collisions` counters: very high values, such as hundreds, suggest a hash table or hash value problem.

## Checked
Method: 2026-11-08 read the unbound.conf, performance guide and unbound-control pages for the defaults, slab, reload and counter claims. Added the forked-mode note; removed the guide attribution for the explicit-slabs advice, which the guide does not state that way.
