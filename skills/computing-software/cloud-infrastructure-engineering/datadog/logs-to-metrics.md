---
id: computing-software.cloud-infrastructure-engineering.datadog.logs-to-metrics
name: logs-to-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, generate-metrics, log-based-metrics, logs-metrics, custom-metric]
level: practitioner
status: docs-checked
description: "Create Datadog log-based count or distribution metrics from the ingest stream, choose group-by tags safely and know what can be edited later."
sources: ["https://docs.datadoghq.com/logs/log_configuration/logs_to_metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generate metrics from logs
Goal: keep long-term trends of logs even when logs are excluded from indexes.

Create at Logs > Generate Metrics > New Metric (or Export > Generate new metric from an Analytics search):

1. Query: Log Explorer search syntax, evaluated against the log stream at ingest time, not against indexed logs. Full-text search (`*:search_term`) is not supported, and a query that works in Log Explorer can still match nothing here. Only logs ingested with a timestamp within the past 20 minutes are aggregated. Exclude the index from the query.
2. Field: `*` for a count of matching logs, or a log attribute such as `@network.bytes_written` to produce `count`, `min`, `max`, `sum` and `avg` metrics (the attribute facet should be a measure).
3. Group by: metrics have no tags unless you add them. Any attribute or tag can become a metric tag, named as the attribute without the `@`.
4. Percentiles (optional): p50, p75, p90, p95, p99 for distribution metrics; they count as custom metrics too.
5. Name: must follow the custom metric naming convention.

- Because the stream is the source, you can exclude logs from indexes and still chart trends at 10-second granularity for 15 months.
- Log-based metrics are billed as custom metrics, so avoid unbounded group-by attributes (timestamps, user IDs, request IDs, session IDs).
- After saving, confirm the metric produces datapoints in Metrics Explorer. If the query matches logs in Log Explorer but the metric stays empty, rewrite the term as a quoted phrase, for example `message:"Database operation failed."`.
- Editable later: the filter query, the group-by tags and the percentile selection. To change the metric type or name, create a new metric.

Gotcha: renaming or reshaping attributes in a pipeline can leave the metric empty because its query no longer matches.

## Verify
- The metric appears in Metrics Explorer with datapoints for the same period in which Log Explorer shows matching logs.

## Checked
2026-11-03. Confirmed against the Generate Metrics from Ingested Logs page. Removed: the `.as_count()` query example and the "distribution from `@duration`" example (not on the page), and the unconfirmed documentation-owner advice.
Method: documentation only; no commands were run.
