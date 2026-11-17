---
id: computing-software.networking-hardware-and-wireless.unbound.statistics-collection
name: statistics-collection
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, statistics-interval, statistics-cumulative, unbound-control-stats, cachehits, monitoring]
level: practitioner
status: draft
description: "Collect Unbound statistics with statistics-interval, statistics-cumulative and unbound-control stats, and read the core per-thread and total counters."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/core/monitoring.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# statistics collection
Options:
- `statistics-interval` (0, disabled) prints per-thread statistics to the log every N seconds.
- `statistics-cumulative` (no): default resets counters after each printout; set yes if a graphing tool expects counters that keep increasing.
- `extended-statistics` (no): adds detail such as query types, at some tracking overhead.

Commands: `unbound-control stats` prints `name: value` lines and then resets (subject to `statistics-cumulative`); `stats_noreset` does not reset; `flush_stats` zeroes them.

Core counters (`threadX.*` and `total.*`): `num.queries`, `num.cachehits`, `num.cachemiss`, `num.prefetch` (counted within cachehits), `num.expired`, `num.recursivereplies`, `recursion.time.avg` and `.median`, `requestlist.*`, `tcpusage`. Time: `time.now`, `time.up`, `time.elapsed`.

`total.requestlist.max` is a maximum across threads; `total.requestlist.avg` and `total.recursion.time.median` are averaged.

`unbound-control` must be set up first; see remote-control-setup.
