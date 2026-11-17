---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.prometheus
name: prometheus
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, prometheus, status-code-metrics, per-consumer, plugins, metrics]
level: practitioner
status: docs-checked
description: "prometheus plugin options (all default false): per_consumer, status_code_metrics, latency_metrics, bandwidth_metrics, upstream_health_metrics, ai_metrics and wasm_metrics."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/prometheus/schema.lua
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# prometheus plugin

All `config` fields are booleans defaulting to `false`:

| Field | Exports |
|---|---|
| `per_consumer` | adds a consumer label to `kong_http_requests_total` and `kong_bandwidth_bytes` when a consumer is available |
| `status_code_metrics` | `http_requests_total` and `stream_sessions_total` |
| `latency_metrics` | `kong_latency_ms`, `upstream_latency_ms`, `request_latency_ms` |
| `bandwidth_metrics` | `bandwidth_bytes` and `stream_sessions_total` |
| `upstream_health_metrics` | `upstream_target_health` |
| `ai_metrics` | `ai_llm_requests_total`, `ai_llm_cost_total`, `ai_llm_tokens_total` |
| `wasm_metrics` | Wasm metrics collection |

A custom validator requires the `prometheus_metrics` shared dictionary to exist.

The plugin also has a `protocols` field.

## Checked

2026-11-04. Confirmed against the prometheus schema.lua: seven boolean config fields defaulting to false, the metric names each exports, the prometheus_metrics shared dict validator. Removed the status_listen default: the cited schema does not state it.

Method: documentation only; no commands were run.
