---
id: computing-software.cloud-infrastructure-engineering.fluentd.in-tail-watchers-and-group-rate-limit
name: in-tail-watchers-and-group-rate-limit
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, in-tail, inotify, enable-watch-timer, enable-stat-watcher, group, rate-limit]
level: advanced
status: docs-checked
description: "Reduce in_tail CPU with watch timer and stat watcher settings, and throttle noisy files per namespace or pod with the group and rule sections."
sources:
  - https://docs.fluentd.org/input/tail
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# in_tail watchers and group rate limits
**Watchers**
- `enable_watch_timer` (default true): extra 1-second timer. Setting `false` greatly reduces CPU and I/O with many files on `inotify` systems; the page says tests suggest it works without the timer.
- `enable_stat_watcher`: per-file stat watchers (inotify). `false` leaves only the timer, so `enable_watch_timer` must stay true; mainly avoids inotify stuck issues. It does not control directory watchers.
- `enable_dir_watcher`: watches directories to find new files early; collected for one second before refreshing; adds overhead. Pair with `follow_inodes true`; it does not prevent re-reading a copytruncate archive.

**Group rate limit** (since 1.15): cap lines per file group per period.
```
<group>
  rate_period 5s
  <rule>
    match {
        "namespace": "/shopping/",
        "podname": "/frontend/",
    }
    limit 1000
  </rule>
</group>
```
- `pattern`: regexp extracting metadata from the file path; the default extracts `podname`, `namespace`, `container`, `docker_id` from Kubernetes container log names. Custom named captures work, e.g. `/^\/home\/logs\/(?<file>.+)\.log$/`.
- `rate_period`: counter reset interval.
- `<rule>` (required): `match` hash of capture name to regexp string (default `{"namespace": "/./", "podname": "/./"}`), and `limit` (default -1, no throttle).

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/input/tail and confirmed: enable_watch_timer, enable_stat_watcher, enable_dir_watcher, group and rule parameters and defaults. Removed or reworded: nothing.

Method: documentation only; no commands were run.
