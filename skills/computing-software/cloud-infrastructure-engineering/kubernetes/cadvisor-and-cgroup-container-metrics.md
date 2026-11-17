---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cadvisor-and-cgroup-container-metrics
name: cadvisor-and-cgroup-container-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cadvisor, cgroups, cgroup-v1, cgroup-v2, container-cpu-usage-seconds-total, container-memory-working-set-bytes, throttling, cpu-cfs-quota, kubelet-metrics-cadvisor, prometheus]
level: advanced
status: docs-checked
description: "How the kubelet's embedded cAdvisor derives per-container CPU, memory, network and PSI metrics from cgroups, and the counter, throttling and cgroup v2 gotchas in queries."
sources: ["https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md", "https://kubernetes.io/docs/reference/instrumentation/node-metrics/", "https://kubernetes.io/docs/concepts/cluster-administration/system-metrics/", "https://kubernetes.io/docs/concepts/architecture/cgroups/", "https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cAdvisor: the container-level metrics underneath every k8s dashboard

**Goal:** know where `container_cpu_usage_seconds_total`, `container_memory_working_set_bytes`
and friends come from (cgroup accounting, read by the cAdvisor embedded in the kubelet), and the
gotchas that make naive queries on them wrong.

## 1. Where the numbers come from
The kubelet runs an embedded cAdvisor and exposes its metrics on the kubelet's
`/metrics/cadvisor` endpoint (alongside `/metrics/resource` and `/metrics/probes`); scrape it per
node. cAdvisor reads per-container cgroup accounting. With the `PodAndContainerStatsFromCRI`
feature gate and a runtime that supports it, the kubelet takes pod and container stats from the
container runtime over CRI instead of cAdvisor.

Key metrics and what they mean (from cAdvisor's metric list):
- `container_cpu_usage_seconds_total` — a **counter** of CPU time consumed; always `rate()` or
  `irate()` it over a window, never read it raw.
- `container_cpu_cfs_throttled_periods_total` / `container_cpu_cfs_periods_total` — throttled
  periods versus elapsed enforcement periods; their ratio is the throttling signal
  (`container_cpu_cfs_throttled_seconds_total` gives total throttled time). A container at its
  CPU limit can show latency spikes while average CPU usage looks below the limit, because quota
  is enforced per period.
- `container_memory_working_set_bytes` — the current working set. The kubelet's
  `memory.available` eviction signal is node capacity minus the node's working set, with
  inactive file pages excluded as reclaimable.
- `container_memory_rss` — size of RSS; closer to "what did the app allocate".
- `container_network_*`, `container_fs_*` — per-container network and filesystem counters.
- `container_spec_cpu_quota` / `container_spec_memory_limit_bytes` — the configured limits as
  metrics, useful for `usage / limit` panels without joining against the Kubernetes API.

## 2. cgroup v1 vs v2
- cgroup v2 (stable in Kubernetes since v1.25) unifies controllers under one hierarchy. Kubernetes
  deprecated cgroup v1 in v1.35, and the kubelet no longer starts on a cgroup v1 node by default
  (`failCgroupV1: false` overrides this until removal).
- Metric availability differs by version: several cAdvisor memory metrics are marked cgroup v2
  only (for example `container_memory_pgscan_total`, `container_memory_workingset_refault_*`),
  and Pressure Stall Information (PSI) needs cgroup v2 and Linux 4.20 or later.
- PSI is exposed on `/metrics/cadvisor` as `container_pressure_{cpu,memory,io}_{stalled,waiting}_seconds_total`
  counters. The `KubeletPSI` feature gate is locked on from v1.36.
- Moving a node pool from cgroup v1 to v2 can change which series exist; compare
  `/metrics/cadvisor` output before and after the node image change and re-baseline memory
  thresholds.

## 3. Query gotchas
- Before summing, check whether your scrape keeps series with an empty `container` label
  (cgroups above container level) and filter them out (`container!=""`) so they are not added to
  container series.
- Short-lived containers can be missed when the scrape interval is longer than their lifetime.

## Gotchas
- Summing `container_cpu_usage_seconds_total` across replicas without `rate()` first gives a
  meaningless cumulative number, not a usage rate.
- Throttling can happen even when the averaged CPU rate is below the limit, because quota is
  enforced per CFS period. Graph the throttled-periods ratio alongside usage.
- Node-level CPU (for example from node_exporter) and summed container CPU will not match exactly;
  don't alert on them matching.

## Verify
- [ ] Dashboards `rate()` the `_total` counters over a window of at least two scrape intervals.
- [ ] CPU panels pair usage with the `container_cpu_cfs_throttled_periods_total` / `container_cpu_cfs_periods_total` ratio.
- [ ] Sums filter `container!=""`.
- [ ] Nodes run cgroup v2, and panels still populate after any node OS or kubelet image change.

## Checked
2026-10-27 against the cAdvisor Prometheus metrics list (google/cadvisor master) and Kubernetes
docs (kubernetes/website main, v1.38 development tree; v1.37 is the latest release: node metrics
data, system metrics, cgroups, node-pressure eviction). Confirmed: the embedded cAdvisor and
`/metrics/cadvisor` endpoint, the CRI stats alternative, metric names and meanings, the
`memory.available` definition, cgroup v2 status and the v1.35 cgroup v1 deprecation with
`failCgroupV1`, the PSI requirements, metric names and `KubeletPSI` lock. Removed unchecked claims
about a cAdvisor cache TTL, Prometheus service discovery roles and mixin relabelling, the
"embedded since 1.12" date, and the working set being what drives kernel OOM kills.
Method: documentation only; no commands were run.
