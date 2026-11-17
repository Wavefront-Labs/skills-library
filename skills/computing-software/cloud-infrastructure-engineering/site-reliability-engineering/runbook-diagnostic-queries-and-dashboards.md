---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.runbook-diagnostic-queries-and-dashboards
name: runbook-diagnostic-queries-and-dashboards
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, runbooks, runbook-diagnostic-queries, dashboards, deep-links, promql]
level: practitioner
status: draft
description: "Embed ready-to-run diagnostic queries and parameterised dashboard deep links in runbooks so responders get answers in one click, and keep them tested."
sources: ["https://sre.google/workbook/on-call/", "https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/create-dashboard-url-variables/", "https://grafana.com/docs/grafana/latest/explore/", "https://prometheus.io/docs/prometheus/latest/querying/api/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Diagnostic queries and dashboards in runbooks

**Goal:** runbook steps that are links returning the answer, not instructions to go find it.

## Deep links
- Grafana dashboard with variables and time range from the alert:
```
https://grafana.example.com/d/checkout?var-cluster={{ $labels.cluster }}&from=now-1h&to=now
```
- Grafana Explore link with a query encoded (copy "Share link" from Explore, then replace the label value with the alert template variable).
- Prometheus graph link: `https://prom.example.com/graph?g0.expr=<urlencoded>&g0.range_input=1h`.
- Logs: Loki/Elastic query links filtered by service and time.
- Trace search: TraceQL link `{ resource.service.name = "checkout" && status = error }`.

## Embedded queries (copy-paste ready)
```promql
# Which route is failing?
topk(5, sum by (route) (rate(http_requests_total{service="checkout", code=~"5.."}[5m])))
# Did a deploy just happen?
changes(kube_deployment_status_observed_generation{deployment="checkout"}[30m])
```
```bash
kubectl -n payments get pods -l app=checkout -o wide
kubectl -n payments logs deploy/checkout --since=15m | grep -i error | tail -50
```
State what a normal vs abnormal result looks like for each query.

## Keep them working
- Store runbooks in Git next to alert rules; CI validates PromQL syntax with `promtool` (wrap queries in a test file) and checks links return 200.
- Use stable dashboard UIDs; renaming a dashboard must not break links.
- Prefer a dedicated "alert investigation" dashboard per service with rows matching runbook steps.
- Review during each Wheel of Misfortune and after real use.

## Verify
- [ ] Clicking every link from a test alert opens the right panel with data for the alert's labels.
