---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.cadvisor-container-metrics
name: cadvisor-container-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [cadvisor, cadvisor-metrics, container-cpu-throttling, memory-working-set, kubelet, oomkilled, kubernetes-monitoring]
level: practitioner
status: docs-checked
description: "Query cAdvisor container metrics: CPU usage vs throttling, memory working set vs RSS vs cache, OOM events, and which metric families need which cAdvisor option."
sources: ["https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md", "https://kubernetes.io/docs/concepts/cluster-administration/system-metrics/", "https://github.com/kubernetes-sigs/kubernetes-mixin", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/workload/pod-metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cAdvisor container metrics

On Kubernetes the kubelet exposes cAdvisor metrics at `/metrics/cadvisor` (alongside `/metrics`, `/metrics/resource` and `/metrics/probes`; these do not have the same lifecycle as `/metrics`). Standalone cAdvisor serves Prometheus metrics at `/metrics` by default; the endpoint can be changed with `-prometheus_endpoint`, and metric groups switched with `-disable_metrics` / `-enable_metrics` (cAdvisor docs). Each metric family belongs to an option group (`cpu`, `memory`, `network`, `disk`, `diskIO`, `process`, `oom_event`...), and some need extra build flags.

## CPU
Per the cAdvisor metric table:
- `container_cpu_usage_seconds_total` (counter): cumulative CPU time consumed; `container_cpu_user_seconds_total`, `container_cpu_system_seconds_total` split it.
- `container_cpu_cfs_periods_total` (number of elapsed enforcement period intervals), `container_cpu_cfs_throttled_periods_total` (number of throttled period intervals) and `container_cpu_cfs_throttled_seconds_total` (total time throttled).
```promql
# cores used per container
sum by (namespace, pod, container) (rate(container_cpu_usage_seconds_total[5m]))
# fraction of enforcement periods that were throttled
sum by (namespace, pod, container) (rate(container_cpu_cfs_throttled_periods_total[5m]))
  / sum by (namespace, pod, container) (rate(container_cpu_cfs_periods_total[5m]))
```
Inspect the label sets on your own cluster before filtering: the cAdvisor page does not document which series represent pod-level cgroups or pause containers, so check for series with an empty or placeholder `container` label and exclude them in per-container sums.

## Memory (gauges, bytes)
| Metric | Description in the cAdvisor table |
|---|---|
| `container_memory_working_set_bytes` | Current working set |
| `container_memory_rss` | Size of RSS |
| `container_memory_cache` | Total page cache memory |
| `container_memory_usage_bytes` | Current memory usage, including all memory regardless of when it was accessed |
| `container_memory_max_usage_bytes` | Maximum memory usage recorded |
| `container_spec_memory_limit_bytes` | Memory limit for the container |

`container_oom_events_total` (counter, option group `oom_event`) counts out-of-memory events observed for the container. kube-state-metrics has `kube_pod_container_status_last_terminated_reason` (the `reason` label holds the last terminated reason; container, pod, namespace labels) and `kube_pod_container_resource_limits` (labels include `resource`, `unit`, `container`, `pod`, `namespace`), which you can join to compare usage with limits:
```promql
max by (namespace, pod, container) (container_memory_working_set_bytes)
  / on (namespace, pod, container) kube_pod_container_resource_limits{resource="memory"}
```

## Network and filesystem
Network: `container_network_receive_bytes_total`, `container_network_transmit_bytes_total` and the matching `_errors_total` and `_packets_dropped_total` families (option group `network`). Filesystem: `container_fs_usage_bytes`, `container_fs_limit_bytes`, and the `container_fs_*` I/O counters (option groups `disk` and `diskIO`). What a given runtime reports depends on the runtime, so check the series exist on your cluster.

## Gotchas
- To attribute pods to workloads, join with `kube_pod_owner` (kube-state-metrics; labels `pod`, `namespace`, `owner_kind`, `owner_name`, `owner_is_controller`).
- Which cAdvisor labels to drop for cardinality is a decision for your scrape config; the cited pages do not prescribe one.

## Verify
- [ ] The series you query exist in your Prometheus (`container_cpu_cfs_throttled_periods_total`, `container_memory_working_set_bytes`, `container_oom_events_total`); a missing family usually means its cAdvisor option group is disabled or unsupported by the runtime.

## Checked
Date: 2026-11-07. Read in full: the cAdvisor Prometheus metrics page (every metric name, type and description above is from its tables), the Kubernetes "Metrics For Kubernetes System Components" page (kubelet `/metrics/cadvisor` note, first 20 lines read closely, rest of the page not relevant), the kube-state-metrics pod metrics page (searched for `kube_pod_owner`, `kube_pod_container_status_last_terminated_reason`, `kube_pod_container_resource_limits` rows; not read end to end) and the kubernetes-mixin README (only a mention of a cadvisorSelector config key, nothing else used). Removed as unconfirmed: the `container!="POD"` double-counting rule, the 25% throttling alert threshold, the 100 ms CFS period explanation and remove-CPU-limits advice, "working set is what the kubelet evicts on / what the OOM killer compares", the `reason="OOMKilled"` literal, the mixin recording-rule name, the "network metrics only at pod level" and "containerd reports limited fs stats" claims, the metricRelabelings advice and the `kubectl top` verify.
Method: documentation only; no commands were run.
