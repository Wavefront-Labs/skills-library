---
id: computing-software.devops-ci-cd.argo-rollouts.controller-metrics-and-grafana
name: controller-metrics-and-grafana
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [prometheus, metrics, controller-metrics, grafana, port-8090, rollout-info, argo-rollouts]
level: practitioner
status: docs-checked
description: "Scrape the Argo Rollouts controller metrics on port 8090 and build Grafana dashboards."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/controller-metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The controller exposes Prometheus metrics at `/metrics` on port 8090. Make Prometheus scrape it; with Kubernetes service discovery and annotation-based configs (like the Prometheus Helm chart) annotate the controller pod template:

```yaml
annotations:
  prometheus.io/scrape: 'true'
  prometheus.io/path: /metrics
  prometheus.io/port: '8090'
```

Check the Prometheus Targets page to confirm it is reached.

Useful metrics from the docs:

- `rollout_info`, `rollout_info_replicas_available`, `rollout_info_replicas_unavailable`, `rollout_info_replicas_desired`, `rollout_info_replicas_updated`
- `rollout_phase` (deprecated, use `rollout_info`)
- `rollout_reconcile` and `rollout_reconcile_error`
- `experiment_info`, `experiment_phase`, `experiment_reconcile`, `experiment_reconcile_error`
- `analysis_run_info`, `analysis_run_metric_phase`, `analysis_run_metric_type`

A starter dashboard JSON is in the repository at `examples/dashboard.json`; import it into Grafana.

Verify with a query for `rollout_info` in Prometheus.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/controller-metrics/.

Removed or corrected: the rollout_duration_seconds, rollout_progression_duration_seconds and rollout_manual_pause_duration_seconds metrics and the alert ideas built on them (not on the page).

Method: documentation only; no commands were run.
