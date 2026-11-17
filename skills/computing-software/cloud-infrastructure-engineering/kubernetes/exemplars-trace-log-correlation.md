---
id: computing-software.cloud-infrastructure-engineering.kubernetes.exemplars-trace-log-correlation
name: exemplars-trace-log-correlation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, tracing, exemplars, trace-log-correlation, prometheus, grafana]
level: practitioner
status: docs-checked
description: "Link metrics to traces with Prometheus exemplar storage and the Grafana Prometheus data source, and check exemplars through the Prometheus query_exemplars API."
sources: ["https://prometheus.io/docs/prometheus/latest/feature_flags/", "https://prometheus.io/docs/prometheus/latest/querying/api/", "https://grafana.com/docs/grafana/latest/fundamentals/exemplars/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exemplars and trace-log correlation

## Metrics to traces: exemplars
Grafana defines an exemplar as a specific trace representative of a measurement taken in a given time interval: a link from an aggregated metric to a single request's trace.
1. Instrument: scrape targets add exemplars to certain metrics through OpenMetrics. Exemplars are references to data outside the metric set; a common use is trace IDs. The application's client library must expose the trace ID with the observation.
2. Enable exemplar storage in Prometheus with the feature flag:
   ```
   --enable-feature=exemplar-storage
   ```
   On Kubernetes, pass it through whatever deploys Prometheus (an operator or Helm chart exposes the Prometheus feature flags; find the exact value name in that chart's documentation).
3. In Grafana, exemplars are supported for the Prometheus data source only. Grafana shows exemplars next to a metric in Explore and in dashboards, each as a highlighted star; hovering shows the trace ID, and a button next to the trace ID property opens the investigation. Configure the data source exemplar link as described in Grafana's Prometheus data source documentation.

Check that exemplars exist with the Prometheus HTTP API, which is documented as experimental:
```bash
curl -g 'http://<PROMETHEUS_HOST>:9090/api/v1/query_exemplars?query=<METRIC_NAME>&start=<START>&end=<END>'
```
`GET` and `POST /api/v1/query_exemplars` take a PromQL `query` and a time range.

## Logs to traces
Put the trace ID in every log line (key=value or a JSON field) so a log data source can extract it; the configuration steps depend on the log backend's own documentation.

## Verify
From a latency panel, hover an exemplar, open its trace, and find the same trace ID in the logs.

## Checked
2026-11-01. Confirmed: the Prometheus feature flags page (`--enable-feature=exemplar-storage`, exemplars via OpenMetrics, trace IDs as the common use), the Prometheus HTTP API page (`/api/v1/query_exemplars`, experimental), the Grafana exemplars introduction (definition, Prometheus data source only, star display, trace ID). Removed (not confirmed in fetched pages): kube-prometheus-stack values, `trace_id` link and Loki derived-field regex, Tempo trace-to-logs attribute mapping, the sampling and `max_exemplars` gotchas, and the Grafana Loki page (it returned 404).
Method: documentation only; no commands were run.
