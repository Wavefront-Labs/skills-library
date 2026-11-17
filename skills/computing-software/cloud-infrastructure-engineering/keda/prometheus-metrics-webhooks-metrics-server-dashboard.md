---
id: computing-software.cloud-infrastructure-engineering.keda.prometheus-metrics-webhooks-metrics-server-dashboard
name: prometheus-metrics-webhooks-metrics-server-dashboard
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [keda-webhook-metrics, metrics-adapter, grpc-client-metrics, grafana-dashboard, apiserver-metrics]
level: practitioner
status: docs-checked
description: "Scrape the KEDA admission webhook and metrics adapter endpoints and use the premade Grafana dashboard that visualises the metrics adapter."
sources:
  - https://keda.sh/docs/2.17/integrations/prometheus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The adapter endpoint reuses port 8080 and path /metrics exactly like the operator, so one scrape pattern covers all three components. In the dashboard, use the scaledObject and scaledJob variables to focus on a single resource.
Besides the operator, two more KEDA components publish Prometheus metrics on port `8080` at `/metrics`.

Admission webhooks:
- `keda_webhook_scaled_object_validation_total`: current value for ScaledObject validations;
- `keda_webhook_scaled_object_validation_errors`: number of validation errors.

Metrics server (the KEDA Metrics Adapter):
- `keda_internal_metricsservice_grpc_client_started_total`, `_handled_total`, `_msg_received_total`, `_msg_sent_total`: client-side RPC counters toward the operator's gRPC metrics service;
- `keda_internal_metricsservice_grpc_client_handling_seconds`: histogram of gRPC response latency;
- Operator SDK framework metrics;
- Kubernetes API server metrics, prefixed with `apiserver_`.

A premade Grafana dashboard visualises the metrics adapter. It has two sections: KEDA's metric server, and the scale target with its replica changes driven by KEDA. Variables at the top: `datasource`, `namespace`, `scaledObject`, `scaledJob`, `scaler` and `metric`.

## Checked

2026-11-03. Confirmed on the 2.17 Prometheus integration page: webhook and metrics adapter metrics, dashboard sections and variables. Removed: the dashboard file name and repository path, which the page does not give.

Method: documentation only; no commands were run.
