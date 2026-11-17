---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-capacity-dashboards
name: cluster-capacity-dashboards
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, slo-dashboards, capacity-dashboards, capacity-planning, requests-vs-allocatable, grafana]
level: practitioner
status: docs-checked
description: "Build cluster capacity dashboards comparing requests, usage and allocatable per node pool, with headroom, pod slots and forecast panels for planning."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/", "https://github.com/kubernetes/kube-state-metrics/tree/main/docs/metrics", "https://prometheus.io/docs/prometheus/latest/querying/functions/#predict_linear", "https://kubernetes.io/docs/reference/instrumentation/metrics/", "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster capacity dashboards

The scheduler places pods by requests, so requests vs allocatable is the capacity number that
matters; usage tells you how honest the requests are.

## Core panels (per node pool via a `pool` label variable)
```promql
# requested share of allocatable CPU (running and pending pods only)
sum(kube_pod_container_resource_requests{resource="cpu"} * on (namespace, pod) group_left() (kube_pod_status_phase{phase=~"Running|Pending"} == 1))
/ sum(kube_node_status_allocatable{resource="cpu"})

# actual usage share
sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) / sum(kube_node_status_allocatable{resource="cpu"})

# memory requested share
sum(kube_pod_container_resource_requests{resource="memory"} * on (namespace, pod) group_left() (kube_pod_status_phase{phase=~"Running|Pending"} == 1))
/ sum(kube_node_status_allocatable{resource="memory"})

# pod slots used
sum(kube_pod_info) / sum(kube_node_status_allocatable{resource="pods"})
```
Join nodes to pools with `kube_node_labels` (needs the pool label in KSM's
`--metric-labels-allowlist=nodes=[...]`).

## Headroom and fragmentation
- Largest pod that still fits: allocatable minus requests per node, max over nodes.
- Pending pods count (`kube_pod_status_phase{phase="Pending"}`) next to autoscaler activity.

## Forecast
```promql
predict_linear(sum(kube_pod_container_resource_requests{resource="cpu"})[14d:1h], 30*86400)
```
compared with current allocatable and the node-group maximum.

## Reading it
Requests close to allocatable with usage far below requests means over-requesting: rightsize before buying nodes.
Usage close to requests and requests close to allocatable means real growth.

## Verify
Totals match `kubectl describe nodes` "Allocated resources" summed over a pool.

## Checked
2026-11-01. Confirmed: the kube-state-metrics docs for `kube_pod_container_resource_requests`, `kube_node_status_allocatable`, `kube_pod_status_phase`, `kube_pod_info`, `kube_node_labels` and `--metric-labels-allowlist`; the Kubernetes metrics reference for `container_cpu_usage_seconds_total`; the Prometheus function docs for `predict_linear`; the Kubernetes resource-management page for the `kubectl describe nodes` Allocated resources section. Removed: the specific percentage thresholds. The `pool` label is a user-defined placeholder.
Method: documentation only; no commands were run.
