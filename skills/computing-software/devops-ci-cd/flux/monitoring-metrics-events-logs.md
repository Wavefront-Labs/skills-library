---
id: computing-software.devops-ci-cd.flux.monitoring-metrics-events-logs
name: monitoring-metrics-events-logs
category: computing-software
field: devops-ci-cd
product: flux
tags: [monitoring, prometheus, gotk-reconcile-duration-seconds, kube-state-metrics, events]
level: sme
status: docs-checked
description: "Monitor Flux with controller Prometheus metrics on port 8080 and kube-state-metrics resource metrics such as gotk_resource_info."
sources:
  - https://fluxcd.io/flux/monitoring/metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Controllers expose Prometheus metrics on port 8080 at `/metrics`, including:
- `gotk_reconcile_duration_seconds_{bucket,sum,count}{kind,name,namespace}` for reconcile duration.
- `gotk_cache_events_total` for cache events (useful for tuning Helm index cache).
- token cache metrics (`gotk_token_cache_events_total`, `gotk_token_cache_requests_total`, `gotk_token_cached_items`).
- `controller_runtime_reconcile_total{controller,result}` and `workqueue_longest_running_processor_seconds`.
- CPU and memory via `process_cpu_seconds_total` and `container_memory_working_set_bytes`.

Resource state is not exported by the controllers. Use kube-state-metrics with a custom resource state config, which yields `gotk_resource_info{customresource_kind, exported_namespace, name, ready, suspended, ...}` plus kind-specific labels such as `revision`, `source_name`, `url`, `chart_name`. The `ready` label shows readiness and `suspended` shows whether reconciliation is suspended. Extra labels seen in Prometheus may come from the kube-prometheus-stack scrape config and can be ignored.

The fluxcd/flux2-monitoring-example repo deploys kube-prometheus-stack and loki-stack, a PodMonitor selecting the Flux controller pods on port `http-prom`, and two Grafana dashboards (Flux Cluster Stats and Flux Control Plane).

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/monitoring/metrics/ (raw source in the fluxcd/website repository).

Removed or corrected: the Kubernetes events and structured logs sections and the alerting advice, which are not on the metrics page; the description was narrowed to match.

Method: documentation only; no commands were run.
