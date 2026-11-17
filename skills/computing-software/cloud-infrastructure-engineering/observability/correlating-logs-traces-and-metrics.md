---
id: computing-software.cloud-infrastructure-engineering.observability.correlating-logs-traces-and-metrics
name: correlating-logs-traces-and-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, signal-correlation, log-trace-correlation, trace-id-in-logs, exemplars, explore, correlations, logs-to-traces, traces-to-logs, traces-to-metrics, metrics-to-traces, derived-fields, data-links, grafana-explore, split-view, trace-context-logging, mdc, service-name, resource-attributes, otel-logs, span-id, pivoting, debugging-workflow]
level: advanced
status: docs-checked
description: "Make signals pivot into each other: trace ids in logs via OTel, exemplars, Grafana trace-to-logs/metrics, derived fields, correlations, consistent service labels."
sources: ["https://opentelemetry.io/docs/concepts/signals/logs/", "https://grafana.com/docs/grafana/latest/administration/correlations/", "https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/", "https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/configure-trace-to-logs/", "https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/provision/", "https://grafana.com/docs/loki/latest/get-started/labels/structured-metadata/", "https://prometheus.io/docs/prometheus/latest/feature_flags/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Correlating logs, traces and metrics

**Goal:** from any one signal, reach the others in one click: metric spike → example trace
→ that request's logs → the pod's other logs → the pod's metrics. This is what turns three
data stores into observability.

## 1. The shared keys
| Key | Where it must appear |
|---|---|
| `trace_id` / `span_id` | every log line emitted inside a request; exemplars on request metrics; the trace itself |
| `service.name` (`service_name`/`job`/`app`) | resource attribute on spans/logs/profiles, metric label; **the same string everywhere** |
| `k8s.pod.name` and other attributes you filter by | resource attributes and labels |
| time | all of them: clocks in sync (NTP/chrony), no timezone surprises in the logger |
Agree on a mapping table (OTel name → Prometheus label → Loki label) and enforce it in the
Collector and shippers. Grafana's trace-to-logs default
tags remap `service.name` to `service_name` automatically; custom tags must name the remapped
label explicitly.

## 2. Trace ids into logs
- **OTel logs bridge / log appenders**: use your logging library with an OpenTelemetry log
  appender (bridge). With auto-instrumentation or an SDK active, OTel correlates existing logs
  with the active trace and span; log records carry `TraceId`, `SpanId` and `TraceFlags`.
- **Without OTel logs**: put the ids in the logger's context from the active span (MDC in
  Java, a `logging` filter in Python, a `slog` handler reading the `ctx` in Go). In structured
  JSON use the same field names everywhere (`trace_id`, `span_id`), not `traceId` in one
  service and `trace-id` in another.
- Loki: ship `trace_id` as **structured metadata** (Grafana Alloy `stage.structured_metadata`),
  never as a label; then filter with `{job="example"} | trace_id="<id>"`.

## 3. Exemplars: metrics → traces
Request histograms/counters carry an exemplar (`trace_id`) per sample:
- Exemplars are an OpenMetrics feature: scrape targets add them to certain metrics, commonly
  trace ids. Prometheus must run with `--enable-feature=exemplar-storage`.
- Mimir: the per-tenant limit `max_global_exemplars_per_user` (default 0) is the maximum number
  of exemplars in memory across the cluster; 0 disables exemplar ingestion.

## 4. Grafana wiring
Provisioning files expand `$` in values, so write `$${...}` for Grafana variables.
```yaml
# Tempo data source jsonData
tracesToLogsV2:
  datasourceUid: loki
  spanStartTimeShift: "-2s"
  spanEndTimeShift: "2s"
  tags: [{ key: service.name, value: app }, { key: k8s.pod.name, value: pod }]   # OTel attr → Loki label
  filterByTraceID: true
  filterBySpanID: false
  customQuery: true
  query: '{$${__tags}} | trace_id=`$${__trace.traceId}`'
tracesToMetrics:
  datasourceUid: mimir
  tags: [{ key: service.name, value: service }]
  queries: [{ name: Latency, query: 'sum(rate(traces_spanmetrics_latency_bucket{$$__tags}[5m]))' }]
tracesToProfiles: { datasourceUid: pyroscope, profileTypeId: "process_cpu:cpu:nanoseconds:cpu:nanoseconds" }
serviceMap: { datasourceUid: mimir }
```
- **Loki derived fields** (on the Loki data source) turn a log field into a link to the Tempo
  data source: the logs-to-traces direction. The Tempo trace-to-logs page covers this setup.
- **Correlations**: a correlation defines how data in one data source is used to query another
  data source or build an external URL, e.g. a Loki `pod` field → a Prometheus query for that
  pod. Configure by provisioning, Administration > Plugins and data > Correlations, or in
  Explore. Links show in Explore's Logs panel and Table; a query link opens in Explore split view.

## 5. The workflow this enables
1. SLO burn alert → dashboard panel with exemplars → pick a slow exemplar → trace.
2. Trace view: find the slow span → trace-to-logs link (trace id + service filter) → the
   error line → the pod was OOM-killed → pod link → memory panel.
3. Or inverse: a log error → trace → service graph shows the downstream dependency that
   failed → its RED metrics (`tracesToMetrics`) → its deploy annotation.
Document this as the team's "first five minutes" in the runbook template.

## Gotchas
- Different `service.name` casing or suffixes between SDK and shipper (`checkout` vs
  `checkout-svc`) silently breaks every link; lint resource attributes in the Collector.
- Sampling: a log line whose trace was not sampled links to "trace not found"; log
  `TraceFlags` and show the link only when sampled, or use tail sampling that keeps errors.
- Mimir `max_global_exemplars_per_user` at its default of 0 disables exemplar ingestion.
- Trace-to-logs time shifts: Grafana's docs say a shift of `0` can return no logs when
  timestamps do not align exactly; start with `-2s` / `2s` and widen for slow or batch spans.
- Do not make high-cardinality fields (`pod`, `traceId`, `spanId`) Loki labels: Grafana warns
  of huge stream counts, slow queries and log loss at ingest.

## Verify
- [ ] From a latency panel, an exemplar click opens the exact trace; from that trace, the trace-to-logs link returns the request's lines.
- [ ] `{app="api"} | trace_id="<id>"` returns lines with `service.name` matching the span's resource attribute exactly.
- [ ] A correlation from a Loki `pod` field opens the pod's memory query in Explore split view with the same time range.

## Checked
2026-10-31. Confirmed against the Tempo data source, trace-to-logs, trace-to-metrics and provisioning pages (grafana/grafana docs sources: `tracesToLogsV2`, `tracesToMetrics`, `tracesToProfiles`, `serviceMap`, `spanStartTimeShift`, `filterByTraceID`, `filterBySpanID`, `customQuery`, `$$` escaping, `profileTypeId` value, default tags and the `service.name` remap, `-2s`/`2s` starting shifts), the Correlations page, the Loki structured metadata page, the Prometheus exemplar-storage feature flag, the Mimir configuration reference (`max_global_exemplars_per_user`, default 0) and the OTel logs concept page (log bridges, `TraceId`/`SpanId`/`TraceFlags`). Removed as unconfirmed: the Grafana Prometheus exemplar data source settings, Collector processor names, named logging libraries and MDC artifact names, client-library exemplar calls, Collector exemplar option names, the OpenMetrics Accept header, the `-5m/+5m` shift, the `traces_spanmetrics_calls_total` query, the Loki derived-field YAML keys, Explore logs-context and volume claims, and dashboard data-link syntax.
Method: documentation only; no commands were run.
