---
id: computing-software.cloud-infrastructure-engineering.kubernetes.golden-signals-workload-dashboards
name: golden-signals-workload-dashboards
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, slo-dashboards, golden-signals-dashboard, grafana, latency, saturation]
level: practitioner
status: docs-checked
description: "Build per-workload golden-signals dashboards (latency, traffic, errors, saturation) in Grafana with namespace and workload variables and Kubernetes saturation metrics."
sources: ["https://sre.google/sre-book/monitoring-distributed-systems/", "https://grafana.com/docs/grafana/latest/dashboards/variables/", "https://github.com/kubernetes-monitoring/kubernetes-mixin", "https://istio.io/latest/docs/reference/config/metrics/", "https://grafana.com/docs/grafana/latest/datasources/prometheus/template-variables/", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/workload/pod-metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Golden-signals dashboards per workload

One dashboard template, selected by `namespace` and `workload` variables, beats a hand-made
dashboard per service.

## Variables
```
namespace: label_values(kube_pod_info, namespace)
workload:  label_values(namespace_workload_pod:kube_pod_owner:relabel{namespace="$namespace"}, workload)
```
(the recording rule comes from kubernetes-mixin / kube-prometheus-stack).

## Panels
| Signal | Query (Istio example; swap for ingress or app metrics) |
|---|---|
| Traffic | `sum(rate(istio_requests_total{reporter="destination",destination_workload="$workload",destination_workload_namespace="$namespace"}[5m]))` |
| Errors | same filtered `response_code=~"5.."` divided by traffic |
| Latency p50/p95/p99 | `histogram_quantile(0.99, sum by (le) (rate(istio_request_duration_milliseconds_bucket{reporter="destination",destination_workload="$workload"}[5m])))` |
| CPU saturation | usage vs request: `sum(rate(container_cpu_usage_seconds_total{namespace="$namespace",pod=~"$workload-.*",container!=""}[5m])) / sum(kube_pod_container_resource_requests{namespace="$namespace",pod=~"$workload-.*",resource="cpu"})` |
| Memory | working set vs limit: `container_memory_working_set_bytes` / `kube_pod_container_resource_limits{resource="memory"}` |
| Restarts and replicas | `increase(kube_pod_container_status_restarts_total[1h])`, available vs desired replicas |

## Layout rules
- Top row: SLO status and error budget remaining.
- Show deploy annotations (from CI or Argo CD) so regressions line up with releases.
- Same units and axis ranges across services.
- Keep the dashboard in Git (Grafana provisioning or grafana-operator).

## Verify
Selecting any workload fills every panel; a known incident window shows clear signal changes.

## Checked
2026-11-01. Confirmed: the Google SRE book (four golden signals: latency, traffic, errors, saturation; dashboards normally include them), the Istio standard metrics reference (`istio_requests_total`, `istio_request_duration_milliseconds`, the `reporter` and `destination_workload` labels), kube-state-metrics pod metrics (`kube_pod_container_resource_limits`, `kube_pod_container_status_restarts_total`) and the kubernetes-mixin rules (`namespace_workload_pod:kube_pod_owner:relabel`, `container_memory_working_set_bytes`). Removed: the CPU throttling row (cAdvisor throttling metrics not confirmed in fetched pages) and the log-scale advice.
Method: documentation only; no commands were run.
