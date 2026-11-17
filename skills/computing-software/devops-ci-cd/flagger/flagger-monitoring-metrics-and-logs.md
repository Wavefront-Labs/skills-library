---
id: computing-software.devops-ci-cd.flagger.flagger-monitoring-metrics-and-logs
name: flagger-monitoring-metrics-and-logs
category: computing-software
field: devops-ci-cd
product: flagger
tags: [monitoring, prometheus-metrics, grafana, logging]
level: practitioner
status: docs-checked
description: "Monitor Flagger itself with its Prometheus metrics, JSON logs, Grafana dashboard and event webhook."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/monitoring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flagger exposes Prometheus metrics: `flagger_info` (version, mesh provider), `flagger_canary_total`, `flagger_canary_status` (0 running, 1 successful, 2 failed), `flagger_canary_weight` per workload (primary and canary), `flagger_canary_duration_seconds` histogram, `flagger_canary_metric_analysis` (last result per metric), and the counters `flagger_canary_successes_total` and `flagger_canary_failures_total` (labelled by deployment strategy and analysis status).

Logs are JSON and mirror Kubernetes events, for example `kubectl -n istio-system logs deployment/flagger --tail=100 | jq .msg` shows lines like "Advance podinfo.test canary weight 5" and "Halt podinfo.test advancement success rate 98.69% < 99%".

A Grafana dashboard for canary analysis (RED and USE metrics for primary and canary) installs with `helm upgrade -i flagger-grafana flagger/grafana --set url=http://prometheus:9090`. The `event` webhook sends every Flagger event as JSON to an endpoint of your choice.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/monitoring.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
