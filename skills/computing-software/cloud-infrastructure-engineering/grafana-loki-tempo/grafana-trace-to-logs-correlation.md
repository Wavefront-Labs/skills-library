---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.grafana-trace-to-logs-correlation
name: grafana-trace-to-logs-correlation
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [trace-to-logs, grafana, tracestologsv2, span-to-logs, filter-by-trace-id, custom-query, tag-mapping]
level: practitioner
status: docs-checked
description: "Configure Tempo trace-to-logs so a span opens matching Loki logs, with time shifts, tag mapping, a custom query and the Loki derived field back to traces."
sources: ["https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/configure-trace-to-logs/", "https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/provision/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: from a span jump to its logs, and from a log line back to its trace. Both data sources must be configured.

Tempo data source (provisioning key `tracesToLogsV2`; YAML needs `$$` to escape `$`):
```yaml
jsonData:
  tracesToLogsV2:
    datasourceUid: 'loki'
    spanStartTimeShift: '-2s'
    spanEndTimeShift: '2s'
    tags: [{ key: 'service.name', value: 'service_name' }, { key: 'namespace' }]
    filterByTraceID: true
    filterBySpanID: false
    customQuery: false
```
- Time shifts widen the log window; the default `0` can return no logs. Docs suggest `-2s`/`2s`, more for slow or batch spans.
- Tags map span attributes to Loki label names that must exactly match the stream labels, or the correlation silently breaks. Defaults when none set: `cluster`, `hostname`, `namespace`, `pod`, `service.name` (becomes `service_name`) and `service.namespace` (becomes `service_namespace`); remapping only applies to those, so custom tags need the explicit Loki name.
- With Loki, the **Logs for this span** link shows only if at least one configured tag exists on the span.
- **Filter by trace ID** returns all logs for the trace; **Filter by span ID** needs a span ID field in logs. Both toggles are disabled when a custom query is on. The link filters by trace ID, not span ID.
- Custom query uses variables: `{${__tags}} | logfmt | trace_id=`${__trace.traceId}``. If a tag is structured metadata not an indexed label, put it in the pipeline: `{${__tags}} | pod=`${__span.tags["k8s.pod.name"]}` |= `${__trace.traceId}``.

Loki data source, for the reverse direction: Additional settings > Derived fields > add field (for example `TraceID`), type Regex in log line (one capture group, such as `trace_id=(\w+)`) or Label, enable Internal link, choose Tempo, set Query to `${__value.raw}`.

Gotchas
- A provisioned data source is read-only in the UI; change the YAML, or in Grafana Cloud clone the data source.
- Use low-cardinality labels; keep trace IDs and pod names as structured metadata rather than labels.
- Apps must put trace IDs in logs; without them the query falls back to a time-range filter.
- Different trace ID field names need separate derived fields.

## Verify
In Explore with the Tempo data source, click a span and choose **Logs for this span**; the Loki query should show lines in the window. In Explore with Loki, a line containing the trace ID shows a link to Tempo.

## Checked
2026-11-03. Confirmed against the Grafana "Configure trace to logs correlation" and "Provision the Tempo data source" pages. Removed: the draft's `${__span.traceId}` variable (docs use `${__trace.traceId}`), the `-5m/5m` shifts as a recommendation, the cross-tenant header gotcha, and the claim that Grafana adds a structured-metadata filter for the trace ID.
Method: documentation only; no commands were run.
