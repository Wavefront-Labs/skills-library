---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.tempo-trace-to-logs-and-metrics
name: tempo-trace-to-logs-and-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [trace-to-logs, trace-to-metrics, tempo-data-source, signal-correlation, trace-to-profiles]
level: practitioner
status: docs-checked
description: "Configure the Tempo data source trace-to-logs and trace-to-metrics links in Grafana: tag mappings, time shifts, custom queries and the Loki derived field."
sources: ["https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/", "https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/configure-trace-to-logs/", "https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/configure-trace-to-metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tempo trace-to-logs and trace-to-metrics

You need Editor or Admin permission. A provisioned data source (and the pre-configured Grafana Cloud Traces source) is read-only in the UI: clone it, or edit the provisioning YAML. Provisioning uses the `tracesToLogsV2` and `tracesToMetrics` blocks; see the vendor's "Provision the Tempo data source" page for the full YAML.

## Trace to logs (two-sided)
Tempo data source (Connections > Data sources > Tempo > Trace to logs): controls the query when you click **Logs for this span**. Supports Loki, Elasticsearch, Splunk, OpenSearch, Falcon LogScale, Google Cloud Logging and VictoriaMetrics Logs.
- **Span start/end time shift**: default 0 can return no logs; a common start is -2s and 2s, more for slow or batch spans.
- **Tags**: map span attributes to log label names. The label must exactly match the Loki stream label; a mismatch silently breaks the link. With no tags configured the defaults are cluster, hostname, namespace, pod, service.name (remapped to service_name) and service.namespace (remapped to service_namespace). The dot-to-underscore remap applies only to those defaults; custom tags must name the remapped label.
- The link appears on a span only if at least one configured tag exists on it.
- Prefer low-cardinality labels (service_name, namespace, cluster); keep trace IDs and pod names as structured metadata.
- **Filter by trace ID** returns all logs for the whole trace; **Filter by span ID** needs a span ID field in logs. Both are disabled with a custom query. Logs must contain the trace ID, otherwise the query falls back to a time range.
- **Use custom query**: LogQL with `${__tags}`, for example ``{${__tags}} | logfmt | trace_id=`${__trace.traceId}` ``. A tag stored as structured metadata cannot go in the stream selector; use a pipeline filter.
- Loki side (required for log line to trace): Derived fields with a Regex in log line (for example `trace_id=(\w+)`), Internal link on, Tempo selected, Query `${__value.raw}`.
- Variables in these configs must be wrapped in `${}` (for example `${__span.name}`).

## Trace to metrics
Works with any Prometheus-compatible data source; no Tempo metrics generator needed.
- **Span start/end time shift** default -2m and 2m.
- **Tags**: key is the span attribute, optional value is the metric label (for example `service.name` to `service_name`).
- **Custom queries** (Add query): optional Link Label plus a Query such as `requests_total{$__tags}`, which becomes `requests_total{pod="nginx-554b9", cluster="us-east-1"}`. `${__tags}` includes only tags present on the span. Without mapped tags you can still use `method="${__span.tags.method}"`.
- Metrics to traces needs exemplars configured on the Prometheus data source.

## Checked
2026-11-08. Confirmed in the Tempo data source landing page and the trace-to-logs and trace-to-metrics pages. Removed: the provisioning YAML (field names beyond the two block names, Loki/Prometheus UIDs, profileTypeId, serviceMap, nodeGraph, lokiSearch), the `$$__tags` escape, span-metrics metric names, the "Related metrics" and Service Graph tab verification and the metrics-generator service-graph note; trace to profiles settings were not read.
Method: documentation only; no commands were run.
