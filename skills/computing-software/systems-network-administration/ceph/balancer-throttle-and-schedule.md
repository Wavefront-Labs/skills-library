---
id: computing-software.systems-network-administration.ceph.balancer-throttle-and-schedule
name: balancer-throttle-and-schedule
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, balancer, target-max-misplaced-ratio, upmap-max-deviation, sleep-interval, schedule]
level: advanced
status: docs-checked
description: "Tune how fast and when the Ceph balancer runs: target_max_misplaced_ratio, upmap_max_deviation, time windows and pool restriction."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/balancer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The balancer moves PGs in phases and only when the cluster is healthy. Main knobs:

```
ceph config set mgr target_max_misplaced_ratio .03
ceph config set mgr mgr/balancer/upmap_max_deviation 1
ceph config set mgr mgr/balancer/sleep_interval 60
```

- `target_max_misplaced_ratio`: maximum fraction of PGs remapped in one phase, default 5%. A larger value converges faster at greater client impact.
- `upmap_max_deviation`: how far an OSD's PG shard count may be from its weight-proportional target before it counts as unbalanced. It is an absolute number of PGs, not a percentage. The docs call 1 reasonable and safe for most clusters, and note that a very low value can make the balancer shuffle forever; clusters with several device classes or mixed capacities benefit from the smaller number.
- `sleep_interval`: seconds between runs.

Limit it to a window or to certain pools:

```
ceph config set mgr mgr/balancer/begin_time 0000
ceph config set mgr mgr/balancer/end_time 2359
ceph config set mgr mgr/balancer/begin_weekday 0
ceph config set mgr mgr/balancer/end_weekday 6
ceph config set mgr mgr/balancer/pool_ids 1,2,3
```

Times are HHMM; weekdays use 0 for Sunday as in crontab. Find pool IDs with `ceph osd pool ls detail`.

## Checked

2026-11-03. Confirmed against: the Ceph Balancer Module page (docs.ceph.com/en/latest/rados/operations/balancer/): Throttling (target_max_misplaced_ratio, upmap_max_deviation, sleep_interval, begin/end time and weekday, pool_ids).

Removed: nothing; the page says upmap_max_deviation defaulted to 5 at time of writing (June 2025), and the skill does not state a default.

Method: documentation only; no commands were run.
