---
id: computing-software.cloud-infrastructure-engineering.keda.prometheus-metrics-from-keda-operator
name: prometheus-metrics-from-keda-operator
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [prometheus-metrics, keda-scaler-active, keda-scaler-metrics-value, keda-scaler-detail-errors-total, operator-metrics, port-8080]
level: practitioner
status: docs-checked
description: "List the KEDA operator Prometheus metrics on port 8080 at /metrics for scaler activity, values, latency, errors and CloudEvents."
sources:
  - https://keda.sh/docs/2.17/integrations/prometheus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The KEDA Operator exposes Prometheus metrics at `/metrics` on port `8080`. Key series:

- `keda_build_info`: version, git commit and Go runtime. With no scalers deployed this is the only metric you see; others appear as scalers of matching types are created.
- `keda_scaler_active`: 1 when the scaler is active, 0 when inactive.
- `keda_scaled_object_paused`: 1 when a ScaledObject is paused.
- `keda_scaler_metrics_value`: the value the HPA uses to compute the target average.
- `keda_scaler_metrics_latency_seconds`: time to retrieve the metric from each scaler.
- `keda_scaler_detail_errors_total`, `keda_scaled_object_errors_total`, `keda_scaled_job_errors_total`: error counters per scaler, ScaledObject and ScaledJob.
- `keda_resource_registered_total` and `keda_trigger_registered_total`: counts of custom resources per namespace and triggers per type.
- `keda_internal_scale_loop_latency_seconds`: deviation between expected and actual scaling loop execution, caused by accumulated scaler latency or load; internal.
- `keda_cloudeventsource_events_emitted_total` and `keda_cloudeventsource_events_queued`.
- `keda_internal_metricsservice_grpc_server_*`: started, handled, message received, message sent totals and a handling-seconds histogram.
- Operator SDK framework metrics.

Trigger `name` values from the ScaledObject specification are the way to tell a trigger's metrics apart in this Prometheus output.

## Checked

2026-11-03. Confirmed on the 2.17 Prometheus integration page: port 8080 /metrics, every listed metric name, the keda_build_info note.

Method: documentation only; no commands were run.
