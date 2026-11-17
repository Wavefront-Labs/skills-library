---
id: computing-software.cloud-infrastructure-engineering.datadog.metrics-without-limits
name: metrics-without-limits
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, metrics-without-limits, metric-cardinality, tag-configuration, custom-metric-cost]
level: practitioner
status: docs-checked
description: "Control custom metric volume by configuring queryable tags (allowlist or blocklist) in Metrics Summary or the Metrics API."
sources: ["https://docs.datadoghq.com/metrics/metrics-without-limits/", "https://docs.datadoghq.com/metrics/custom_metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics without Limits and cardinality
Goal: reduce custom metric volume without losing the views you need.

A custom metric is identified by a unique combination of metric name and tag values (including the host tag). Metrics without Limits decouples ingestion from indexing: everything is still ingested, and you choose which tags stay queryable.

Allowlist (Metrics Summary): open the metric, click Manage Tags, then Include tags, pick the tags to keep queryable, review the Estimated New Volume, and save. The dialog pre-populates tags queried on dashboards, notebooks, monitors or the API in the past 30 days; you can also add tags used on assets (dashboards, monitors, notebooks, SLOs) so those assets keep working.

Blocklist: Manage Tags, then Exclude Tags. Blocked tags are not queryable on dashboards and monitors. Through the API the same switch is `exclude_tags_mode: true`.

API: the tag configuration can be created, edited, deleted and impact-estimated through the Metrics APIs. A create request body has `data.type` of `manage_tags`, `data.id` as the metric name, and `attributes` with `tags` (a list of tag keys that stay queryable), `metric_type` and optionally `exclude_tags_mode` and `include_percentiles` (distribution metrics only). Look up the endpoint in the API reference for the Metrics tag configuration.

```json
{"data": {"type": "manage_tags", "id": "ExampleMetric",
  "attributes": {"tags": ["app", "datacenter"], "metric_type": "gauge"}}}
```

- For tags to be managed, the metric must have a type declared (set on submission, or with Edit in Metrics Summary).
- Many metrics at once: Tag Indexing Rules apply an allowlist or blocklist to every metric matching a name or prefix, including metrics submitted later.
- Two volumes show on the Usage page and Metrics Summary: Ingested Custom Metrics (all ingested tags) and Indexed Custom Metrics (still queryable). See the vendor's billing page for how each is charged.

Gotcha: removing a tag that dashboards or monitors group by or filter on leaves those queries without data; include tags used on assets first.

## Verify
- After saving, the Metrics Summary side panel shows indexed custom metrics lower than ingested.

## Checked
2026-11-03. Confirmed against the Metrics without Limits page, the custom metrics page and the Metrics API request schemas (field names, `manage_tags`, `exclude_tags_mode`, `include_percentiles`). Removed: the curl command (endpoint path not confirmed in pages read), billing statements ("per your plan"), the top-ten monthly review advice, and the claim that percentile aggregators add series.
Method: documentation only; no commands were run.
