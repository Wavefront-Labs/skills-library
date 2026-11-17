---
id: computing-software.networking-hardware-and-wireless.squid.cache-replacement-and-swap-marks
name: cache-replacement-and-swap-marks
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, cache-replacement-policy, lru, gdsf, lfuda, cache-swap-low]
level: advanced
status: docs-checked
description: "Pick a disk eviction policy (lru, GDSF, LFUDA) and tune the cache_swap_low and cache_swap_high water marks."
sources:
  - https://www.squid-cache.org/Doc/config/cache_replacement_policy/
  - https://www.squid-cache.org/Doc/config/cache_swap_low/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replacement policy and swap marks
`cache_replacement_policy` applies to cache_dir lines listed below it.
- `lru` (default): list-based, keeps recently referenced objects
- `heap GDSF`: favours small popular objects; better object hit rate, lower byte hit rate
- `heap LFUDA`: favours popular objects regardless of size; better byte hit rate. Raise `maximum_object_size` above its 4 MB default with it
- `heap LRU`: LRU using a heap

`cache_swap_low` (default 90%) is where eviction starts for aufs, ufs and diskd; `cache_swap_high` (default 95%) is where eviction becomes aggressive. For large caches the 5% gap can mean hundreds of MB, so consider moving the values closer.

## Checked

2026-11-04. Read the cache_replacement_policy and cache_swap_low directive pages and confirmed the policies, 90 and 95 defaults and the 5% gap advice; the maximum_object_size advice for LFUDA comes from the maximum_object_size page. Nothing was removed.

Method: documentation only; no commands were run.
