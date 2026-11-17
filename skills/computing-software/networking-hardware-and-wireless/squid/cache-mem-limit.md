---
id: computing-software.networking-hardware-and-wireless.squid.cache-mem-limit
name: cache-mem-limit
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, cache-mem, memory-cache, hot-objects]
level: intro
status: docs-checked
description: "Set the ideal memory limit for in-transit, hot and negative-cached objects with cache_mem."
sources:
  - https://www.squid-cache.org/Doc/config/cache_mem/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache_mem
Sets the ideal memory limit for in-transit objects, hot objects and negative-cached objects, stored in 4 KB blocks. Default: 256 MB.

- It does not limit Squid's total process memory.
- In-transit objects have top priority, so Squid can exceed the limit under load and frees blocks as load drops.
- With shared memory caching enabled, in-transit objects still use local memory.

## Checked

2026-11-04. Read the cache_mem directive page and confirmed the 256 MB default, 4 KB blocks, in-transit priority and shared-memory note. Nothing was removed.

Method: documentation only; no commands were run.
