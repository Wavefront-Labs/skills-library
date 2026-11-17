---
id: computing-software.data-engineering.apache-flink.flink-autoscaler
name: flink-autoscaler
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-autoscaler, flink-kubernetes-operator, parallelism, backpressure, autoscaling]
level: advanced
status: docs-checked
description: "Configure the Flink Kubernetes operator autoscaler: target utilisation, metrics windows, scaling limits, catch-up time, dry runs, and verifying decisions."
sources:
  - https://cwiki.apache.org/confluence/display/FLINK/FLIP-271%3A+Autoscaling
  - https://raw.githubusercontent.com/apache/flink-kubernetes-operator/main/docs/layouts/shortcodes/generated/auto_scaler_configuration.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Flink autoscaler

The operator autoscaler (FLIP-271) scales **each vertex's parallelism** independently based on busy time and processing rates, aiming to keep up with the input rate with headroom, rather than scaling on CPU. It is disabled by default (`job.autoscaler.enabled` defaults to false).

```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
spec:
  flinkConfiguration:
    job.autoscaler.enabled: "true"
    job.autoscaler.stabilization.interval: 5m     # default 5 min: no new scaling in this period
    job.autoscaler.metrics.window: 15m            # default 15 min aggregation window
    job.autoscaler.utilization.target: "0.7"      # default 0.7
    job.autoscaler.utilization.min: "0.5"         # optional, no default
    job.autoscaler.utilization.max: "0.9"         # optional, no default
    job.autoscaler.restart.time: 5m               # default 5 min, used until measured from history
    job.autoscaler.catch-up.duration: 30m         # default 30 min; 0 disables backlog-based scaling
    job.autoscaler.vertex.max-parallelism: "64"   # default 200
    job.autoscaler.vertex.min-parallelism: "2"    # default 1
```

## How it decides
- Computes the true processing rate from busy time; `job.autoscaler.metrics.busy-time.aggregator` is MAX by default (robust to skew), AVG or MIN are alternatives.
- Targets `utilization.target` per vertex, with extra capacity to clear backlog within `catch-up.duration` after a scaling operation.
- `job.autoscaler.scaling.parallelism-alignment.mode` (default `BALANCED`; also `EVENLY_SPREAD`, `OFF`) aligns source and keyBy vertex parallelism to source partitions or key groups.
- Ineffective scale-ups are detected and further scale-ups blocked when `job.autoscaler.scaling.effectiveness.detection.enabled` is true (default false; `effectiveness.threshold` default 0.1).
- `scale-down.interval` (default 1 h) delays and merges scale-downs to reduce restarts; `scale-down.max-factor` default 0.6.
- `vertex.max-parallelism` is ignored if higher than the max parallelism set in the Flink config or on the operator.
- `job.autoscaler.excluded.periods` forbids autoscaling during cron-style periods; `quota.cpu` / `quota.memory` stop scaling beyond a quota.

## Operate
- Dry run first: `job.autoscaler.scaling.enabled: "false"` collects metrics and evaluates suggested parallelism but does not upgrade jobs (default is true).
- `job.autoscaler.memory.tuning.enabled` (default false) adjusts TaskManager memory according to observed needs.
- `job.autoscaler.restart.time-tracking.enabled` (default false) uses observed restart times, capped by `restart.time-tracking.limit` (default 15 min).
- External bottlenecks (saturated sink database) cannot be solved by scaling; use effectiveness detection.
- Combine with a Kubernetes cluster autoscaler so new TaskManagers get nodes.

## Verify
- [ ] Load test: lag rises, autoscaler scales up after the stabilization and metrics window, lag drains in about `catch-up.duration`.
- [ ] No flapping (scale up/down cycles) over a day of normal traffic.

## Checked
2026-11-09. Option names and defaults confirmed against the operator's generated autoscaler configuration table (main branch). Corrected: `target.utilization` and `target.utilization.boundary` are `utilization.target`, `utilization.min` and `utilization.max`; defaults for metrics window, restart time, catch-up duration and max-parallelism. Removed: `scale-up.grace-period` (not in the table), operator and Flink version gates, in-place rescaling via the adaptive scheduler, the `kubectl describe` event name, and the max-parallelism recommendation. The main autoscaler guide page was not readable (empty page).
Method: documentation only; no commands were run.
