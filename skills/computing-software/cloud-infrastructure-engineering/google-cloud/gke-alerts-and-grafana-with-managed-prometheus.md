---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-alerts-and-grafana-with-managed-prometheus
name: gke-alerts-and-grafana-with-managed-prometheus
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, gke-alerting, gke-recommended-alerts, grafana-gmp, prometheus-frontend, managed-prometheus, promql, rules]
level: practitioner
status: docs-checked
description: "Alert on GKE health with recommended alerts, GMP Rules and PromQL alert policies, and point Grafana at Managed Service for Prometheus via the frontend or datasource syncer."
sources: ["https://cloud.google.com/kubernetes-engine/docs/how-to/configure-recommended-alerts", "https://cloud.google.com/stackdriver/docs/managed-prometheus/rules-managed", "https://cloud.google.com/stackdriver/docs/managed-prometheus/query", "https://cloud.google.com/monitoring/promql/create-promql-alerts-console"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE alerts and Grafana with Managed Prometheus

## 1. Alert policies as code
Create alerts as Cloud Monitoring alerting policies, attach notification channels, and keep the policy files in version control. Export existing policies with `gcloud monitoring policies list --format=json` and create from a file with `gcloud monitoring policies create --policy-from-file=<FILE>`.

## 2. PromQL alert policies
Cloud Monitoring alerting policies can use PromQL conditions over both Managed Service for Prometheus metrics and Cloud Monitoring metrics (use `GlobalRules` for rules over Cloud Monitoring metrics). Cloud Monitoring system metrics are addressed in PromQL with `:` and `_` mapping (for example `kubernetes.io/container/cpu/limit_cores` becomes `kubernetes_io:container_cpu_limit_cores`). Alerts from PromQL policies are closed automatically a set time after the condition last held, not by the policy autoclose duration. Build the query in the Metrics Explorer PromQL editor first.

## 3. In-cluster GMP Rules (Prometheus-style)
```yaml
apiVersion: monitoring.googleapis.com/v1
kind: Rules
metadata: {name: api-slo, namespace: payments}
spec:
  groups:
  - name: api
    interval: 30s
    rules:
    - alert: HighErrorRate
      expr: sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.02
      for: 5m
      labels: {severity: page}
```
Rules are evaluated by the managed rule evaluator; the `OperatorConfig` resource in the `gmp-public` namespace configures it to send alerts to an Alertmanager (the automatically deployed managed Alertmanager and/or your own). `ClusterRules` and `GlobalRules` apply the same interface to wider scopes.

## 4. Grafana
Use the **data source syncer**: it generates OAuth2 credentials for your service account and syncs them to a Grafana Prometheus data source through the Grafana data source API. Required to query globally; grant the service account `roles/monitoring.viewer`. The data source URL is `https://monitoring.googleapis.com/v1/projects/<P>/location/global/prometheus` (the Prometheus API is under `/api/v1/`). The frontend proxy is the other option described in the query docs.

## Gotchas
- Query a project whose **metrics scope** includes the other projects to see their metrics in one Grafana.
- Each GMP sample is billed; high-cardinality labels in rules and scrape configs drive cost.

## Verify
- [ ] A test condition that is deliberately true fires the alert and sends a notification.
- [ ] Grafana Explore returns `up` series for the cluster.

## Checked

2026-10-27. Confirmed in the Managed Service for Prometheus rules and query pages, the PromQL alerting page and the `gcloud monitoring policies create/list` reference pages: Rules/ClusterRules/GlobalRules, OperatorConfig in `gmp-public` for Alertmanager, data source syncer and OAuth2 flow, `roles/monitoring.viewer`, the Prometheus URL prefix, `:`/`_` metric name mapping, PromQL alert autoclose behaviour, `--policy-from-file`. Removed: the recommended-alerts console steps (page 404), the `conditionPrometheusQueryLanguage` example and metric name, kube-state metric name, the frontend deployment snippet and image, the `alertmanager` Secret claim, per-sample billing remark. Read end to end.

Method: documentation only; no commands were run.
