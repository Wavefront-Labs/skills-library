---
id: computing-software.cloud-infrastructure-engineering.kyverno.monitoring-metrics
name: monitoring-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [monitoring, metricsservice, kyverno-metrics, servicemonitor, prometheusrule, opentelemetry, grafana-dashboard]
level: practitioner
status: docs-checked
description: "Monitor Kyverno: metrics Services on port 8000, kyverno-metrics ConfigMap, ServiceMonitor, PrometheusRule alerts, OpenTelemetry flags, key metrics."
sources:
  - https://kyverno.io/docs/guides/monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Metrics listen on port 8000. Enable a Service per controller in Helm with `admissionController`, `backgroundController`, `cleanupController`, `reportsController` `.metricsService.create: true`. The default type is ClusterIP; use NodePort or LoadBalancer to expose it. Service name `kyverno-svc-metrics`.

ConfigMap `kyverno-metrics`: `metricsConfig.namespaces.include` (default all), `.exclude` (default empty, exclude wins), `.bucketBoundaries` (default 0.005 to 30 seconds), and `metricsExposure.<metric>` with `enabled`, `disabledLabelDimensions`, `bucketBoundaries`.

Key metrics: `kyverno_admission_review_duration_seconds` (histogram), `kyverno_policy_execution_duration_seconds` (`rule_type`), `kyverno_admission_requests_total` (`resource_kind`, `resource_request_operation`, `request_allowed`), `kyverno_policy_results_total` (`rule_result`, `rule_execution_cause`). The page also writes the counters without `_total` in places; check your version.

ServiceMonitor (kube-prometheus-stack): port 8000, path `/metrics`, scheme http, interval 60s, `tlsConfig.insecureSkipVerify: true`, `namespaceSelector.matchNames: [kyverno]`, selector label `app.kubernetes.io/instance: kyverno`, plus the release label your Prometheus selects.

Alerts: Helm `prometheusRule.enabled: true`, with `prometheusRule.additionalLabels` matching the Prometheus `ruleSelector`. Example alert fires when p99 admission latency exceeds 1s for 5m. Kubernetes webhooks hard-timeout at 10s. For high latency: check request volume, raise CPU limits and replicas, move non-urgent validate rules to background.

Grafana: Helm `grafana.enabled: true` (plus `grafana.grafanaDashboard.enabled: true` for the Grafana Operator) or import `kyverno-dashboard.json`.

OpenTelemetry (needs cert-manager): Kyverno flags `metricsPort`, `otelConfig=grpc`, `transportCreds` (Secret holding `ca.pem`, empty means insecure). Datadog uses annotation `ad.datadoghq.com/kyverno.checks`.

## Checked

2026-11-08. Claims were read against: https://kyverno.io/docs/guides/monitoring/.

Method: documentation only; no commands were run.
