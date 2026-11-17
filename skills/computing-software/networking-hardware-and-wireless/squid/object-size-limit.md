---
id: computing-software.networking-hardware-and-wireless.squid.object-size-limit
name: object-size-limit
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, maximum-object-size, byte-hit-ratio, cache-tuning]
level: intro
status: docs-checked
description: "Set the default maximum cacheable object size with maximum_object_size and understand the hit-ratio trade-off."
sources:
  - https://www.squid-cache.org/Doc/config/maximum_object_size/
  - https://www.squid-cache.org/Doc/config/cache_dir/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# maximum_object_size
Sets the default `max-size` for any `cache_dir`. Default: 4 MB (specified in bytes).

- Raising it can improve byte hit ratio.
- Leave it low if you want to raise the request hit ratio more than you want to save bandwidth.
- Increase it when using the LFUDA replacement policy.
- A per-directory `max-size` option on `cache_dir` overrides it.

## Checked

2026-11-04. Read the maximum_object_size and cache_dir directive pages and confirmed the 4 MB default, the LFUDA note and the max-size override. Fixed the hit-ratio line, which had the trade-off reversed.

Method: documentation only; no commands were run.
