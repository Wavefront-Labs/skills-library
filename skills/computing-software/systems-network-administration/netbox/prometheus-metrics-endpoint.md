---
id: computing-software.systems-network-administration.netbox.prometheus-metrics-endpoint
name: prometheus-metrics-endpoint
category: computing-software
field: systems-network-administration
product: netbox
tags: [prometheus, metrics-enabled, django-prometheus]
level: practitioner
status: docs-checked
description: "Enable the /metrics endpoint and understand multiprocess caveats."
sources: ["https://netboxlabs.com/docs/netbox/integrations/prometheus-metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prometheus metrics

Goal: monitor NetBox itself.

NetBox exposes native metrics at `/metrics` (for example `https://netbox.local/metrics`). They are off by default; enable with the `METRICS_ENABLED` setting in `configuration.py`.

**Metric types** (via the `django-prometheus` library) include:

- Per-model insert, update and delete counters
- Per-view request counters and latency histograms
- REST API requests by endpoint and method, and GraphQL requests
- Request and response body size histograms, response code counters
- Database connection, execution and error counters
- Cache hit, miss and invalidation counters
- Django middleware latency histograms

The exhaustive list is whatever your own `/metrics` endpoint returns.

**Multiprocess.** With several gunicorn workers the Prometheus client needs a shared directory to collect metrics from every worker process. If accurate long-term metrics matter in a multiprocess setup, the docs recommend the uwsgi library over gunicorn because of how gunicorn tracks workers.

**Checklist**

1. Set `METRICS_ENABLED`.
2. Add a Prometheus scrape job.
3. Plan for the shared directory.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Prometheus page: /metrics, METRICS_ENABLED, django-prometheus metric list, multiprocess directory and uwsgi recommendation. Removed: Nothing.

Method: documentation only; no commands were run.
