---
id: computing-software.systems-network-administration.varnish-cache.varnishstat-counters
name: varnishstat-counters
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [varnishstat, counters, hit-ratio, lru-nuked]
level: practitioner
status: docs-checked
description: "Monitor Varnish with varnishstat: one-shot -1 output, -f glob filtering, curses mode, and the key MAIN counters for hits, misses, evictions, threads, bans and failures."
sources:
  - https://www.varnish.org/docs/tutorials/varnish-monitoring/
  - https://www.varnish.org/docs/reference/varnishstat/
  - https://www.varnish.org/docs/reference/varnish-counters/
  - https://www.varnish.org/docs/users-guide/operation-statistics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# varnishstat counters

```bash
varnishstat                      # curses view (INFO level counters)
varnishstat -1                   # print once and exit
varnishstat -1 -f 'MAIN.*'       # glob filter; -I/-X include/exclude
varnishstat -j                   # JSON
```

Synopsis flags include `-1 -c -f -I -j -l -n -r -t -x -X`. Curses columns: Current, Change (per second), Average, Avg_10, Avg_100, Avg_1000.

Key `MAIN.*` counters:
- `client_req`, `cache_hit`, `cache_miss`: compute hit ratio from these.
- `n_object`: objects in cache.
- `n_lru_nuked`: evictions to make room; zero means no need to enlarge the cache.
- `bans`: all bans, including superseded ones.
- `fetch_failed`: failed backend fetches.
- `sess_queued`, `sess_dropped`, `threads`, `threads_limited`: thread pressure.
- `exp_mailed`, `exp_received`: expiry thread traffic.

Full list: the varnish-counters reference.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the SMA.Transient.c_bytes example and the monitoring-agent advice.

Method: documentation only; no commands were run.
