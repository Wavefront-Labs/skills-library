---
id: computing-software.cloud-infrastructure-engineering.observability.ottl-metric-transformations
name: ottl-metric-transformations
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [convert-gauge-to-sum, aggregate-datapoints, metric-ottl-functions, transforming-telemetry, ottl]
level: advanced
status: docs-checked
description: "Reshape metrics with transform processor OTTL functions: convert gauge and sum, extract count and sum, scale units, copy, and aggregate datapoints on attributes."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/transformprocessor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metric OTTL transformations

Metric functions are documented in the transform processor README. They operate in `metric_statements`; several
(`convert_sum_to_gauge`, `aggregate_on_attributes`, `aggregate_on_attribute_value`) work only in the `metric`
context, not on datapoints.

## Functions (as documented)
| Function | What it does |
|---|---|
| `convert_sum_to_gauge()` | Sum to Gauge, keeping datapoints; no-op for other types. May break Gauge semantics |
| `convert_gauge_to_sum(temporality, is_monotonic)` | Gauge to Sum; temporality is `"cumulative"` or `"delta"`; no-op for other types. May break Sum semantics |
| `extract_count_metric(is_monotonic, suffix?)` | New Sum from a Histogram, ExponentialHistogram or Summary count; only created if there is at least one datapoint |
| `extract_sum_metric(is_monotonic, suffix?)` | Same for the sum value; datapoints with a missing sum are skipped |
| `extract_avg_metric(suffix?)` | New Gauge of sum / count, default suffix `_avg`; skips missing sums and zero counts |
| `convert_summary_count_val_to_sum(temporality, is_monotonic, suffix?)` | New Sum from a Summary's count |
| `copy_metric(name?, description?, unit?)` | Copies the metric to the end of the metric slice |
| `scale_metric(factor, unit?)` | Multiplies datapoint values by a float factor, optionally sets unit; Gauge, Sum, Histogram, Summary |
| `aggregate_on_attributes(function, attributes?)` | Aggregates datapoints; see below |
| `aggregate_on_attribute_value(function, attribute, values, newValue)` | Merges datapoints having the attribute with one of `values` into one datapoint with `newValue` |

```yaml
processors:
  transform/metrics:
    error_mode: ignore
    metric_statements:
      - convert_gauge_to_sum("cumulative", true) where metric.name == "legacy_requests"
      - scale_metric(0.001, "s") where metric.name == "http.server.duration" and metric.unit == "ms"
      - extract_count_metric(true, ".count") where metric.name == "http.server.request.duration"
      - aggregate_on_attributes("sum", ["http.route"]) where metric.name == "http.server.request.duration"
```

## aggregate_on_attributes
- `function` is case-sensitive: `sum`, `max`, `min`, `mean`, `median`, `count`. Histogram and exponential histogram
  only support `sum`. Aggregatable types: sum, gauge, histogram, exponential histogram.
- `attributes` omitted: all attributes kept, so only datapoints with identical attribute sets combine.
- `[]`: all datapoint attributes removed, aggregate across all datapoints.
- `["a", "b"]`: only those keys kept, then group on the remainder.
- It can be combined with `keep_matching_keys` or `delete_matching_keys` to prune by regex first.

## Verify
- [ ] The debug exporter shows the expected metric type, name and datapoints after the processor.

## Checked
2026-11-09. Confirmed against the transform processor README (metric function sections convert_*, extract_*,
copy_metric, scale_metric and aggregate_* read). Removed unconfirmed claims and sources: examples using `name`,
`type` and `unit` as bare paths, the datapoint-context Substring and Concat example, partial-sum warnings for
cumulative streams, Prometheus `_total` and rate() remarks, the metricstransform comparison, the advice to prefer
OTTL, and the ottlmetric and ottldatapoint READMEs (not read).
Method: docs-checked 2026-11-09 against the transformprocessor README; documentation only, no commands run.
