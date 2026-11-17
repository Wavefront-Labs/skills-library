---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.kubelet-metrics-endpoints
name: kubelet-metrics-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [kubelet-metrics-endpoint, kubelet-resource-metrics, cadvisor-metrics, kubernetes-monitoring, prober-metrics, volume-stats]
level: practitioner
status: docs-checked
description: "Know which kubelet endpoint (/metrics, /metrics/cadvisor, /metrics/resource, /metrics/probes) serves which metric, the RBAC rule to read them, and the CRI-based cadvisor option."
sources: ["https://kubernetes.io/docs/reference/instrumentation/metrics/", "https://kubernetes.io/docs/reference/instrumentation/cri-pod-container-metrics/", "https://kubernetes.io/docs/concepts/cluster-administration/system-metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubelet metrics endpoints

The kubelet exposes metrics on `/metrics` and also on `/metrics/cadvisor`, `/metrics/resource` and `/metrics/probes`.
Those extra endpoints do not share the lifecycle (stability guarantees) of the main one. If the cluster uses RBAC,
reading metrics needs a user, group or ServiceAccount bound to a ClusterRole that allows `get` on the non-resource URL
`/metrics`:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: prometheus
rules:
  - nonResourceURLs:
      - "/metrics"
    verbs:
      - get
```

Port, scheme and TLS verification settings are not covered by the cited pages: take them from your cluster's kubelet
configuration and your Prometheus `kubernetes_sd_configs` role `node` setup.

## Which metric lives where (per the Kubernetes metrics reference)

| Path | Metrics named on the reference page |
|---|---|
| `/metrics` | `kubelet_running_pods` (gauge, pods with a running sandbox), `kubelet_pleg_relist_duration_seconds` (histogram), `kubelet_volume_stats_available_bytes` and `kubelet_volume_stats_capacity_bytes` (labels `namespace`, `persistentvolumeclaim`), `storage_operation_duration_seconds` (histogram) |
| `/metrics/resource` | `container_cpu_usage_seconds_total`, `container_memory_working_set_bytes` (labels `container`, `pod`, `namespace`), `node_memory_working_set_bytes`, `pod_cpu_usage_seconds_total` |
| `/metrics/probes` | `prober_probe_total` (counter of liveness, readiness or startup probes by `result`; labels include `container`, `namespace`, `pod`, `pod_uid`, `probe_type`, `result`) |
| `/metrics/cadvisor` | per-container and machine-level cAdvisor metrics; the reference page lists no individual cadvisor metric names, so check your own `/metrics/cadvisor` output |

Most of these are ALPHA or BETA on the reference page (`prober_probe_total` and `storage_operation_duration_seconds`
are BETA; the volume-stats and PLEG metrics are ALPHA), so names and labels can change between releases. The `/metrics/resource`
CPU and memory container metrics listed above are STABLE.

## Useful queries

```promql
kubelet_volume_stats_available_bytes / kubelet_volume_stats_capacity_bytes < 0.1    # PVC almost full
sum by (namespace, pod) (rate(prober_probe_total{result="failed"}[5m])) > 0
```

The second query assumes `result` takes the value `failed`; confirm the label values in your own output.

## CRI-based pod and container metrics (beta, off by default)

With the `PodAndContainerStatsFromCRI` feature gate enabled and a compatible runtime (containerd 2.2 or later, CRI-O
1.31.0 or later), the kubelet takes pod and container stats from the container runtime instead of cAdvisor.
`/metrics/cadvisor` keeps the same path and metric names, but pod and container level data comes via the CRI
`ListPodSandboxMetrics` RPC while node and machine-level metrics still come from cAdvisor. The kubelet metric
`kubelet_metrics_provider` has a `provider` label of `cri` or `cadvisor` to show the active source on a node. CRI-O
added namespace, pod and container labels on this endpoint from release 1.36.3, so queries relying on them may break on
earlier versions. If the runtime does not report the expected metrics the kubelet falls back to cAdvisor.

## Verify
- [ ] `up{job="kubelet"}` is 1 for every node for each metrics path you scrape.
- [ ] A test PVC-full alert fires after filling a volume.

## Checked

Checked 2026-11-08 against the Kubernetes metrics reference, the system-metrics page and the CRI pod and container
metrics page: the four endpoints, the ClusterRole example, the endpoint of each listed metric and its stability level,
and the CRI feature details. Removed because the pages do not state them: kubelet port 10250, `nodes/metrics` and
`nodes/proxy` RBAC, the scrape config and `serverTLSBootstrap`, individual cAdvisor metric names, the empty-label
double counting advice, cardinality drop lists and the PLEG latency threshold.
Method: docs-only read of cited pages, 2026-11-08
