---
id: computing-software.cloud-infrastructure-engineering.crossplane.metrics
name: metrics
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [metrics, prometheus, promql, observability]
level: practitioner
status: docs-checked
description: "Enable Crossplane Prometheus metrics and know the core, provider and controller-runtime metric families."
sources:
  - https://docs.crossplane.io/latest/guides/metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable metrics in the Helm chart with `--set metrics.enabled=true`. These Prometheus annotations expose the metrics: `prometheus.io/path: /metrics`, `prometheus.io/port: "8080"`, `prometheus.io/scrape: "true"`. Providers expose metrics on the `metrics` port (default `8080`); scrape them with a `PodMonitor` or add the annotations to the provider's `DeploymentRuntimeConfig`.

Core (Crossplane pod):

- `function_run_function_request_total`, `function_run_function_response_total`, `function_run_function_seconds`.
- `function_run_function_response_cache_*` (hits, misses, errors, writes, deletes, bytes, read and write seconds).
- `engine_controllers_started_total`, `engine_watches_started_total` and their stopped counterparts.

Providers built on crossplane-runtime:

- `crossplane_managed_resource_exists`, `_ready`, `_synced`.
- `crossplane_managed_resource_deletion_seconds`, `_first_time_to_readiness_seconds`, `_first_time_to_reconcile_seconds`, `_drift_seconds`.

Upjet providers add `upjet_resource_ttr`, `upjet_resource_external_api_calls_total`, `upjet_resource_ext_api_duration`, `upjet_terraform_cli_duration` and `upjet_terraform_active_cli_invocations`.

Controller-runtime and client metrics from both: `controller_runtime_reconcile_errors_total` (sharp or continuous rises signal problems), `controller_runtime_reconcile_time_seconds`, `workqueue_depth`, `workqueue_retries_total`, `rest_client_requests_total`.

Circuit breaker metrics from Crossplane core: `circuit_breaker_opens_total`, `circuit_breaker_closes_total` and `circuit_breaker_events_total`. All carry a `controller` label formatted `composite/<plural>.<group>`; `circuit_breaker_events_total` also has a `result` label with values `Allowed`, `Dropped` and `HalfOpenAllowed`. `Dropped` means active throttling. The docs' recommended alerts are a drop ratio above 0.2 for 5m and more than 6 opens per hour for 15m:

```promql
sum by (controller) (rate(circuit_breaker_events_total{result="Dropped"}[5m]))
/
sum by (controller) (rate(circuit_breaker_events_total[5m]))
```

Also useful: `crossplane_managed_resource_first_time_to_readiness_seconds` (time to first Ready after creation) and `crossplane_managed_resource_drift_seconds` (time since the last successful reconcile when an out-of-sync resource is detected).

## Checked

2026-11-08: read the whole Crossplane Metrics guide (raw source of docs.crossplane.io/latest/guides/metrics). Confirmed the Helm value, the three Prometheus annotations, port 8080, the metric names in the core, circuit breaker, provider, Upjet and controller-runtime tables, the `controller` and `result` labels, and the two recommended circuit breaker alert thresholds. Removed an unsourced three-alert recommendation and a claim that metrics are invisible without annotations or a PodMonitor.
Method: documentation only; no commands were run.
