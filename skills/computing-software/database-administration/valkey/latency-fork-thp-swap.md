---
id: computing-software.database-administration.valkey.latency-fork-thp-swap
name: latency-fork-thp-swap
category: computing-software
field: database-administration
product: valkey
tags: [latency, fork, latest-fork-usec, transparent-huge-pages, swap, smaps, vmstat, iostat]
level: advanced
status: docs-checked
description: "Diagnose Valkey latency from fork page-table copy, transparent huge pages and OS swapping using latest_fork_usec, smaps Swap, vmstat and iostat."
sources:
  - https://valkey.io/topics/latency/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fork: `BGSAVE` and AOF rewrite fork in the main thread, copying the page table. With 4 kB pages a 24 GB instance needs 24 GB / 4 kB * 8 = 48 MB of page table to allocate and copy, costly on VMs. Modern hardware-assisted virtualisation makes this small (as of 2024 rarely a problem), but old VMs are slow. Measure by running `BGSAVE` and reading `latest_fork_usec` in `INFO`.

Transparent huge pages: after fork both processes share huge pages; on a busy instance a few event-loop iterations touch thousands of pages and trigger copy-on-write of almost all memory, giving big latency and memory use. Disable THP with `echo never > /sys/kernel/mm/transparent_hugepage/enabled`.

Swapping: the kernel pauses Valkey to page memory back in from swap (random I/O). Causes: memory pressure (Valkey using more than available), idle data pages (rare), and heavy I/O from other processes or RDB/AOF writers inflating the file cache.

Check it:
1. `valkey-cli info | grep process_id`.
2. In `/proc/<pid>/smaps`, `grep 'Swap:'`, or `egrep '^(Swap|Size)'` to compare against map size. The page example had a 720896 kB map with only 12 kB swapped, which is harmless; zeros and sporadic 4 kB entries are normal.
3. `vmstat 1`: non-zero `si` and `so` columns mean swapping.
4. `iostat -xk 1` shows global I/O.

If a meaningful share is swapped, reduce memory pressure: add RAM when Valkey exceeds what is available, and keep other memory-hungry processes off the host.

## Checked
2026-11-03. Confirmed against the Valkey latency diagnosis page (valkey.io/topics/latency/): the 24 GB page table arithmetic (48 MB), the 2024 remark on modern virtualisation, `latest_fork_usec` after `BGSAVE`, the THP copy-on-write explanation and disable command, the three swap causes, the smaps Swap and Size check with the 720896 kB / 12 kB sample, `vmstat 1` si/so and `iostat -xk 1`. The page carries an under-review notice. Nothing removed.
Method: documentation only; no commands were run.
