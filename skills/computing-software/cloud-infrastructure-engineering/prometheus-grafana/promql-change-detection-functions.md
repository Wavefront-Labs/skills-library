---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-change-detection-functions
name: promql-change-detection-functions
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, resets-function, changes-function, delta-function, idelta, gauges, flapping-detection, crashloop]
level: practitioner
status: verified
description: "Use resets(), changes(), delta() and idelta() for restarts, config flapping and gauge movement, and know which work on counters vs gauges."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# resets, changes, delta, idelta

| Function | Input | Returns |
|---|---|---|
| `resets(c[w])` | counter | number of decreases (counter resets) in w |
| `changes(g[w])` | any | number of times the value changed in w |
| `delta(g[w])` | **gauge** | last - first, extrapolated to window edges |
| `idelta(g[w])` | **gauge** | difference of the last two samples |

## Recipes
```promql
# Process restarted more than 3 times in 30m (crashloop without k8s metrics)
resets(process_cpu_seconds_total[30m]) > 3
changes(process_start_time_seconds[30m]) > 3              # more robust: start time changes per restart

# Config reload flapping or leader election churn
changes(prometheus_config_last_reload_success_timestamp_seconds[1h]) > 10
changes(etcd_server_is_leader[1h]) > 3                    # flapping leadership

# Gauge moved by > 10 GiB in 1h (disk consumption)
delta(node_filesystem_avail_bytes{mountpoint="/"}[1h]) < -10 * 2^30

# Queue depth jumped between the last two scrapes
idelta(queue_depth[5m]) > 1000

# Has this metric been constant (stuck exporter)?
changes(some_gauge[30m]) == 0
```

## Rules
- `delta`/`idelta` on counters give wrong results across resets; use `increase`/`rate`.
- `resets` on gauges is meaningless (every drop counts).
- `delta` extrapolates like `increase`, so values are not exact differences; for exact use
  `x - x offset 1h` (note: no extrapolation, and fails if either point is missing).
- `deriv(g[w])` (least-squares slope per second) is more robust than `delta` for noisy gauges.

## Checked
Run on Prometheus 3.15.0: `delta(dsk[1h])` over a gauge falling 5 per minute for 59 steps returned -300, not the raw difference of -295, which shows the extrapolation; `dsk - dsk offset 1h` returned nothing when the older point did not exist; `delta()` over a counter with a reset gave 22.2 where `increase()` gave 40; `resets()` over a gauge counted every drop (5); `deriv(dsk[1h])` returned -0.0833 per second (-5 per minute); `changes(g[30m]) == 0` returned the constant series.

## Verify
- [ ] Each change-detection alert has a tested threshold against a week of history.
- [ ] No `delta(` or `idelta(` applied to `_total` metrics in rules.
