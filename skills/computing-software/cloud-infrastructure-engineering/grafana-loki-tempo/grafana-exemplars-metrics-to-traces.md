---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.grafana-exemplars-metrics-to-traces
name: grafana-exemplars-metrics-to-traces
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [exemplars, grafana, exemplar-storage, trace-id-label, send-exemplars, histogram-exemplar]
level: practitioner
status: docs-checked
description: "Link metrics to traces with exemplars: emit them from OpenMetrics clients, send via Prometheus or Alloy, store in Mimir, and add the Grafana exemplar link to Tempo."
sources: ["https://grafana.com/docs/mimir/latest/manage/use-exemplars/before-you-begin/", "https://grafana.com/docs/mimir/latest/manage/use-exemplars/store-exemplars/", "https://grafana.com/docs/mimir/latest/manage/use-exemplars/about-exemplars/", "https://grafana.com/docs/grafana/latest/fundamentals/exemplars/", "https://grafana.com/docs/grafana/latest/datasources/prometheus/configure/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: click a latency spike and land on a representative trace.

Producer (from the Mimir checklist): use an official Prometheus client library emitting OpenMetrics (Go: `EnableOpenMetrics` true), and pass the current trace ID when recording: `ObserveWithExemplar` for histograms, `AddWithExemplar` for counters. Check the exposition: `curl -H "Accept: application/openmetrics-text" http://<app>/metrics | grep -i "traceid"`.

Shipping:
- Prometheus: run with `--enable-feature=exemplar-storage` and add `send_exemplars: true` under `remote_write`.
- Alloy: set `send_exemplars: true` in `prometheus.remote_write` (see the Alloy docs for exact syntax).
- In both, confirm `prometheus_remote_storage_exemplars_total` is non-zero.

Mimir storage (default is 0, so exemplars are off until set):
```yaml
limits:
  max_global_exemplars_per_user: 100000     # start low; adjust
# per tenant, in the runtime config:
overrides:
  "tenant-a":
    max_global_exemplars_per_user: 100000
```
Mimir keeps exemplars in a fixed-size in-memory circular buffer (a simple exemplar uses roughly 100 bytes) and appends them to the WAL. The docs recommend enabling it for specific tenants only. Roll components after a config change; runtime config is reloaded after `-runtime-config.reload-period`. Query them at `<prometheus-http-prefix>/api/v1/query_exemplars`.

Grafana: only the Prometheus data source supports exemplars. In its settings add an exemplar entry: enable **Internal link** and select the Tempo data source (or give an external URL using `${__value.raw}`), and set **Label name** to the label in the exemplar that carries the trace ID. Provisioning key: `exemplarTraceIdDestinations` with `datasourceUid` and `name` (for example `traceID`). Exemplars show as highlighted stars in Explore and dashboards; click the button next to `traceID` to open the trace.

Gotchas
- The label name must match what your client emits (the docs' examples use `traceID`).
- Sampling can drop the trace an exemplar points to; Tempo's sampling guide notes the link then fails to find the trace.
- The circular buffer overwrites old exemplars when full.

## Verify
Run the curl against the application, check the Alloy or Prometheus counter, and query exemplars from Mimir; the panel should show stars that open Tempo.

## Checked
2026-11-03. Confirmed against the Mimir "use exemplars" pages (about, before you begin, store), the Mimir HTTP API page, Grafana's exemplars introduction, the Prometheus data source configuration page and the Tempo sampling page. Removed: "exemplars only on histogram buckets and counters" and `trace_based` OTel filter claims, Alloy sending exemplars by default (docs say set `send_exemplars`), the diamond marker description (docs say stars), and the unconfirmed query_exemplars curl example with a Mimir port.
Method: documentation only; no commands were run.
