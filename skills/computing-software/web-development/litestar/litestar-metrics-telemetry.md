---
id: computing-software.web-development.litestar.litestar-metrics-telemetry
name: litestar-metrics-telemetry
category: computing-software
field: web-development
product: litestar
tags: [litestar, metrics, opentelemetry, prometheus, telemetry, observability, middleware, prometheuscontroller]
level: practitioner
status: docs-checked
description: "Instrument a Litestar app with OpenTelemetryPlugin or the Prometheus exporter (PrometheusConfig and PrometheusController), including labels, buckets and exemplars."
sources: [https://docs.litestar.dev/latest/usage/metrics/opentelemetry.html, https://docs.litestar.dev/latest/usage/metrics/prometheus.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar metrics: OpenTelemetry and Prometheus

Goal: export traces/metrics (OpenTelemetry) or a scrape endpoint (Prometheus).

## Method

### OpenTelemetry

1. Install `opentelemetry-instrumentation-asgi` or the extra `pip install 'litestar[opentelemetry]'`.
2. Register the plugin:

```python
from litestar import Litestar
from litestar.plugins.opentelemetry import OpenTelemetryConfig, OpenTelemetryPlugin

open_telemetry_config = OpenTelemetryConfig()
app = Litestar(plugins=[OpenTelemetryPlugin(open_telemetry_config)])
```

3. This works out of the box if you configure a global `tracer_provider` and/or `metric_provider` plus an exporter. Alternatively pass the providers you want to `OpenTelemetryConfig` (see its reference docs for options).

### Prometheus

1. Install `prometheus-client` or the extra `pip install 'litestar[prometheus]'`.
2. Add the controller and middleware:

```python
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController

prometheus_config = PrometheusConfig(group_path=True)
app = Litestar(route_handlers=[PrometheusController], middleware=[prometheus_config.middleware])
```

3. Defaults: app name and prefix are `litestar`; metrics are served in Prometheus format at `/metrics`.
4. Change the path or format by subclassing the controller: `class CustomPrometheusController(PrometheusController): path = "/custom-path"; openmetrics_format = True`.
5. `PrometheusConfig` options shown on the page: `app_name`, `prefix`, `labels` (dict whose values are a string or a callable taking the request and returning a string), `buckets` (histogram buckets, for example `[0.1, 0.2, 0.3, 0.4, 0.5]`), `exemplars` (callable taking the request and returning a dict such as `{"trace_id": "1234"}`; supported only in the openmetrics format), `excluded_http_methods` (for example `["POST"]`), `group_path`.

## Verify

Request the metrics path (`/metrics` by default, or your controller's `path`) and expect Prometheus-format output.

## Checked

2026-11-07. Read the full cited page(s) (usage/metrics/opentelemetry.html, usage/metrics/prometheus.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
