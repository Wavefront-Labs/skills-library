---
id: computing-software.networking-hardware-and-wireless.unbound.libevent-and-forked-operation
name: libevent-and-forked-operation
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, libevent, forked-operation, build-options, outgoing-range, slabs]
level: sme
status: docs-checked
description: "Build Unbound with libevent to lift the 1024 descriptor limit, or without threads for forked operation, and the settings that go with each."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/core/performance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# libevent and forked operation
Libevent: build with `./configure --with-libevent`. This removes the 1024 file descriptor limit, so `outgoing-range` can be much higher (example 8192) with `num-queries-per-thread` about half (example 4096). Libevent 1.4.8 is reported stable; old packages such as 1.1 have crash reports and 1.2.0 fixed a race. If crashes persist, environment variables such as `EVENT_NOEPOLL` or `EVENT_NOKQUEUE` disable backends; the poll backend is reliable but slow.

Forked operation: build with `./configure --without-pthreads --without-solaris-threads`. It runs separate processes and is reported 10 to 20% faster because no locking is needed.
- `num-threads` still sets the number of cores.
- Set all slab options to 1.
- Suggested `outgoing-range: 950` and `num-queries-per-thread: 512`.
- Each process has its own cache and limits, so memory multiplies by the core count and sockets can reach cores times 1024.
- Separate caches mean poisoning one process does not affect the others.
- It can be combined with libevent.

In multi-process mode `dump_cache` and `load_cache` are not supported on the remote Unbound.

## Checked
2026-11-04. Confirmed against the performance topic page and the unbound-control manual: libevent build option and stability notes, EVENT_NO* back-end variables, forked-operation build flags, 10 to 20% speed note, slab and range settings, and the multi-process dump_cache/load_cache limit. Nothing removed.
Method: documentation only; no commands were run.
