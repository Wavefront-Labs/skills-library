---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.grafana-trace-to-metrics-correlation
name: grafana-trace-to-metrics-correlation
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [trace-to-metrics, grafana, tracestometrics, span-to-metrics, linked-queries, prometheus-query]
level: practitioner
status: docs-checked
description: "Configure Tempo trace-to-metrics so a span links to Prometheus-compatible queries, with tag mapping, time shifts, custom queries and provisioning."
sources: ["https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/configure-trace-to-metrics/", "https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/provision/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: from a span jump to metrics for the same service or pod. Works with any Prometheus-compatible data source and does not require the Tempo metrics-generator (the generator creates new metrics; this links to metrics that already exist).

Provisioned form (`$$` escapes `$` in YAML):
```yaml
jsonData:
  tracesToMetrics:
    datasourceUid: 'prom'
    spanStartTimeShift: '-1h'
    spanEndTimeShift: '1h'
    tags: [{ key: 'service.name', value: 'service' }, { key: 'job' }]
    queries:
      - name: 'Sample query'
        query: 'sum(rate(traces_spanmetrics_latency_bucket{$$__tags}[5m]))'
```
In the UI: select the metrics data source, optionally set shifts (placeholders `-2m` start and `2m` end, used when the fields are empty), optionally add tags, and either leave **Add query** unused for the basic configuration or add queries. The link appears as **Metrics for this span**.

- Tag key is the span attribute name; optional value is the metric label name (for example `k8s.pod` to `pod`, or `service.name` to `service_name` when the target does not allow dots).
- `$__tags` expands to the mapped tags present on the span only. Example from the docs: `requests_total{$__tags}` with tags `k8s.pod=pod` and `cluster` becomes `requests_total{pod="nginx-554b9", cluster="us-east-1"}`.
- Without mapping tags you can still use span values: `method="${__span.tags.method}"`.
- Each query has an optional Link Label and the Query text.
- Configured tags must exist on the span's attributes or resources for the link to appear.

Gotchas
- A provisioned data source (and Grafana Cloud Traces) is read-only in the UI: edit the provisioning YAML or clone the data source.
- Metric label names must match the mapped names in your metrics store.
- Reverse direction (metric to trace) uses exemplars on the Prometheus data source, not this setting.

## Verify
Open a trace, click a span and follow **Metrics for this span**; the query should open with selectors filled in from the span.

## Checked
2026-11-03. Confirmed against the Grafana "Configure trace to metrics correlation" and "Provision the Tempo data source" pages. Removed: the claim that the link is called "Related metrics", the claim that the metrics-generator must be running, the unconfirmed `http.route` mapping and `histogram_quantile` example, and the "dashboards must use correct UID" remark.
Method: documentation only; no commands were run.
