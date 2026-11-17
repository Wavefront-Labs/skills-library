---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-observability-and-managed-prometheus
name: gke-observability-and-managed-prometheus
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, gke-monitoring, gke-logging, managed-prometheus, gmp, google-cloud-managed-service-for-prometheus, podmonitoring, clusterpodmonitoring, promql, kube-state-metrics, cadvisor, control-plane-metrics, log-exclusions, gke-dashboards, workload-logs, system-logs, cost-of-logging]
level: practitioner
status: docs-checked
description: "Observe GKE: logging and monitoring components, Managed Service for Prometheus with PodMonitoring, PromQL in Cloud Monitoring, and logging cost control."
sources: ["https://cloud.google.com/kubernetes-engine/docs/concepts/about-observability", "https://cloud.google.com/stackdriver/docs/managed-prometheus", "https://cloud.google.com/stackdriver/docs/managed-prometheus/setup-managed", "https://cloud.google.com/kubernetes-engine/docs/how-to/configure-metrics", "https://cloud.google.com/kubernetes-engine/docs/concepts/about-logs", "https://cloud.google.com/stackdriver/docs/managed-prometheus/cost-controls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE observability and Managed Prometheus

**Goal:** every pod's logs and Prometheus metrics land in Cloud Operations without running
your own Prometheus/Loki, with dashboards and alerts in PromQL, and a logging bill you chose.

## 1. Turn the right tiers on
```bash
gcloud container clusters update prod --region=europe-west1 \
  --logging=SYSTEM,WORKLOAD,API_SERVER,SCHEDULER,CONTROLLER_MANAGER \
  --monitoring=SYSTEM,WORKLOAD,API_SERVER,SCHEDULER,CONTROLLER_MANAGER,STORAGE,POD,DEPLOYMENT,STATEFULSET,DAEMONSET,HPA,CADVISOR,KUBELET,JOBSET \
  --enable-managed-prometheus
```
- `SYSTEM` = kube-system, node, GKE components. `WORKLOAD` = your containers' stdout/stderr.
- Control-plane components (`API_SERVER`, `SCHEDULER`, `CONTROLLER_MANAGER`) can be added to both `--logging` and `--monitoring`; the extra monitoring values (`STORAGE`, `POD`, `DEPLOYMENT`, `STATEFULSET`, `DAEMONSET`, `HPA`, `CADVISOR`, `KUBELET`, `JOBSET`) select further metric packages. The kube state metrics package is a managed, curated set of metrics for Pods, Deployments and other objects; see "Use kube state metrics" for the list.
- Managed Service for Prometheus is enabled by default for cluster versions 1.27 or later (`--no-enable-managed-prometheus` disables it). On Autopilot you cannot disable system metrics, and the `NONE` value for logging and monitoring is not supported.

## 2. Managed Service for Prometheus (GMP)
Managed collection uses `PodMonitoring` custom resources (and `ClusterPodMonitoring` for cluster-wide scope) to declare what to scrape; with managed collection enabled but no such resources, no metrics are generated:
```yaml
apiVersion: monitoring.googleapis.com/v1
kind: PodMonitoring
metadata: {name: app, namespace: payments}
spec:
  selector: {matchLabels: {app: payments-api}}
  endpoints: [{port: metrics, interval: 30s, path: /metrics}]
```
Data is stored in Monarch and can be queried across all projects in a metrics scope.
- Query: Cloud Monitoring, Metrics Explorer, PromQL, or the Prometheus HTTP API under `https://monitoring.googleapis.com/v1/projects/<P>/location/global/prometheus/api/v1/`. For Grafana use the data source syncer (see `gke-alerts-and-grafana-with-managed-prometheus`).
- Alerting: `Rules`, `ClusterRules` and `GlobalRules` custom resources (Prometheus rule syntax) are evaluated by the managed rule evaluator and can send to an Alertmanager. PromQL-based alerting policies can also be written directly in Cloud Monitoring.

## 3. Logs
- `resource.type` values include `k8s_cluster` and `k8s_pod`; Kubernetes Events are exported to Cloud Logging (see the GKE logs pages for filters).
- On Standard clusters you can collect only system logs; `WORKLOAD` logs of non-system containers are on by default but optional.

## 4. Control the bill
- Logging: exclusion filters (Autopilot and Standard) reduce the volume sent to Cloud Logging.
- GMP: ingestion is charged by the number of samples (see the vendor pricing page), so reduce samples by lengthening the scrape interval, use relabeling in `PodMonitoring`/`ClusterPodMonitoring` (for example a `keep` rule for kube-state-metrics series, via `metricRelabeling`), and scrape only what has a dashboard or alert. The billing metric "Prometheus Samples Ingested" shows volume.
- Disable `WORKLOAD` logging on Standard clusters that ship application logs elsewhere, so you do not pay twice.

## Gotchas
- A `ClusterPodMonitoring` that selects everything duplicates samples if teams also create `PodMonitoring` for the same pods.
- GKE audit logs: Admin Activity audit logs cannot be disabled.

## Verify
- [ ] PromQL `up{namespace="payments"}` returns 1 per pod in Metrics Explorer.
- [ ] Grafana with the GMP data source shows the same series as Metrics Explorer.
- [ ] Sample ingestion and log volume are reviewed on a cost dashboard; the top contributor is one you expect.

## Checked

2026-10-27. Confirmed in the GKE configure-metrics, about-logs, managed-prometheus, setup-managed, query and cost-controls pages and the `clusters update` reference page: `--logging` and `--monitoring` component values (SYSTEM, WORKLOAD, API_SERVER, SCHEDULER, CONTROLLER_MANAGER, STORAGE, POD, DEPLOYMENT, STATEFULSET, DAEMONSET, HPA, CADVISOR, KUBELET, JOBSET), managed Prometheus on by default from 1.27, PodMonitoring/ClusterPodMonitoring behaviour, Monarch storage and metrics scopes, Prometheus URL prefix, Rules/ClusterRules/GlobalRules, `metricRelabeling` and keep rule, per-sample charging, exclusion filters, Admin Activity logs not disableable. Removed: `--condition-prometheus-query` (not on the policies create page), `prometheus.io/scrape`, remote_write/sidecar line, `attributed_samples_count`, `kubernetes.io/master` namespaces, `_Default` 30-day retention, kube-state metric name, GMP delay figure, Autopilot node-exporter remark, pre-built dashboards claim, JSON log parsing claim, 60 s interval advice. The about-observability page is 404 and was not relied on. Read end to end.

Method: documentation only; no commands were run.
