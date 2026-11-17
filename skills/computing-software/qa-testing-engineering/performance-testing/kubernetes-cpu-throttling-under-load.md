---
id: computing-software.qa-testing-engineering.performance-testing.kubernetes-cpu-throttling-under-load
name: kubernetes-cpu-throttling-under-load
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [cpu-throttling, kubernetes-resources, cfs-quota, container-limits, performance-monitoring]
level: practitioner
status: draft
description: "Detect and explain Kubernetes CPU throttling and memory pressure during load tests: CFS quota metrics, requests vs limits, OOMKills, HPA interplay and what to graph."
sources:
  - https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
  - https://docs.kernel.org/scheduler/sched-bwc.html
  - https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kubernetes resource monitoring under load (CPU throttling)

## The trap
A pod with `limits.cpu: 1` gets CFS quota of 100ms CPU per 100ms period. A multi-threaded service can burn its quota in the first 20ms of a period and is then frozen for 80ms: p99 latency spikes while average CPU utilisation looks fine (e.g. 60%).

## Metrics (cAdvisor / Prometheus)
```promql
# fraction of CFS periods throttled, per container
sum by (pod, container) (rate(container_cpu_cfs_throttled_periods_total[5m]))
/ sum by (pod, container) (rate(container_cpu_cfs_periods_total[5m]))

# CPU usage vs limit
sum by (pod) (rate(container_cpu_usage_seconds_total{container!=""}[5m]))
/ sum by (pod) (kube_pod_container_resource_limits{resource="cpu"})

# memory near limit, OOM kills
container_memory_working_set_bytes / on(pod, container) kube_pod_container_resource_limits{resource="memory"}
kube_pod_container_status_last_terminated_reason{reason="OOMKilled"}
```
Throttled ratio above a few percent during the test correlates with tail latency.

## Interpreting
- High throttling, moderate usage: limit too low for burstiness or too many threads (JVM/Go see host CPU count: set `-XX:ActiveProcessorCount` / `GOMAXPROCS` to match limits; automaxprocs).
- Memory working set climbing to limit: OOMKill risk; restart counts during the test invalidate results.
- HPA scales on usage relative to **requests**; tight requests trigger early scale-out, loose ones delay it.

## Test practice
- Graph these per pod alongside latency during every run.
- Run one experiment with CPU limits removed (requests only) to quantify throttling's latency cost.
- Record node-level saturation too (noisy neighbours, node CPU steal).

## Gotchas
- `kubectl top` shows averages; it won't reveal throttling.
- Generators running in the same cluster compete for nodes: isolate them (separate node pool).

## Verify
After adjusting limits or thread counts, throttled-period ratio drops and p99 improves at the same load.
