---
id: computing-software.database-administration.memcached.worker-threads-sizing
name: worker-threads-sizing
category: computing-software
field: database-administration
product: memcached
tags: [threads, t, worker-threads, libevent, cpu]
level: practitioner
status: docs-checked
description: "Understand memcached's worker-thread model, the default of 4 threads (-t) and why more is rarely better."
sources:
  - https://docs.memcached.org/serverguide/configuring/
  - https://docs.memcached.org/serverguide/hardware/
  - https://docs.memcached.org/advisories/grafanaloki/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Memcached scales across CPUs with worker threads; each thread runs a libevent loop and handles many connections, so it behaves more like nginx than Apache.

- Default: 4 threads (`-t`). Unless memcached is run extremely hard, do not raise it. Very large values (80+) make it considerably slower.
- Do not set `-t` higher than the number of CPUs.
- Most installs only need a single thread's worth of CPU.
- Each worker thread runs its own event loop and handles its own clients.

Check: `stats settings` shows `num_threads`; `stats` shows `threads`.

On NUMA machines with extreme performance needs, run one instance per NUMA node bound with `numactl`.

## Checked

Confirmed 2026-11-09: worker-thread model, libevent, nginx-like comparison, default of 4 threads, 80+ threads being considerably slower, most installs needing a single thread, NUMA advice (Configuring, Hardware and Performance pages); `-t` should not exceed the CPU count (Loki with Extstore page); `num_threads` in `stats settings` and `threads` in `stats` (protocol.txt). Removed the claim that a connection sticks to one worker for its lifetime.

Method: docs-checked 2026-11-09 against docs.memcached.org Configuring, Hardware, Performance and Loki with Extstore pages and memcached doc/protocol.txt
