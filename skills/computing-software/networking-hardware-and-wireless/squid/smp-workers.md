---
id: computing-software.networking-hardware-and-wireless.squid.smp-workers
name: smp-workers
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, workers, smp, multi-process, rock]
level: advanced
status: docs-checked
description: "Run multiple Squid worker processes with the workers directive, and pair them with SMP-aware rock storage."
sources:
  - https://www.squid-cache.org/Doc/config/workers/
  - https://www.squid-cache.org/Doc/config/cache_dir/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# workers (SMP)
`workers N` sets the number of main Squid processes to fork and maintain. Default: SMP disabled (1, one main process). In SMP mode each worker does nearly everything a single Squid does, such as listening on `http_port` and forwarding requests.

For disk caching, `rock` is the only SMP-aware `cache_dir` type.

## Checked

2026-11-04. Read the workers directive page and the cache_dir page and confirmed the meaning of the worker counts, the default and that rock is the only SMP-aware cache_dir type. Nothing was removed.

Method: documentation only; no commands were run.
