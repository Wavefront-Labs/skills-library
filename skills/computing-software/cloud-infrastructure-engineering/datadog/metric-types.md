---
id: computing-software.cloud-infrastructure-engineering.datadog.metric-types
name: metric-types
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, metric-types, count-rate-gauge, histogram, distribution]
level: practitioner
status: docs-checked
description: "Choose between Datadog count, rate, gauge, set, histogram and distribution submission types and see how each maps to an in-app type."
sources: ["https://docs.datadoghq.com/metrics/types/", "https://docs.datadoghq.com/metrics/distributions/", "https://docs.datadoghq.com/metrics/custom_metrics/type_modifiers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metric types
Goal: submit the right type so queries give correct answers.

Submission types are COUNT, RATE, GAUGE, SET, HISTOGRAM and DISTRIBUTION. They map to five in-app types: COUNT, RATE, GAUGE, DISTRIBUTION and HISTOGRAM (explicit, exponential). A metric submitted without a type shows as Not Assigned in the Metrics Summary side panel and cannot be changed to another in-app type until a type is submitted.

- COUNT: total number of event occurrences in one interval (it can go down as well as up).
- RATE: occurrences per second in one interval.
- GAUGE: a snapshot; the last value submitted to the Agent in the interval.
- HISTOGRAM: distribution computed Agent-side per interval. For metric `NAME` the Agent produces `NAME.avg`, `NAME.count` (a RATE), `NAME.median`, `NAME.95percentile` and `NAME.max`. By default only `max`, `median`, `avg` and `count` are sent (`sum` and `min` also exist), set with `histogram_aggregates` in `datadog.yaml`; percentiles are set with `histogram_percentiles`.
- DISTRIBUTION: all raw values go to Datadog and are aggregated server-side across hosts, so percentiles are global rather than per host. Queryable by default: avg, count, max, min, sum. Globally accurate percentiles (p50, p75, p90, p95, p99 or your own, up to two decimals) are enabled per metric on the Metrics Summary page.

Worked example from the docs: values `[1,1,1,2,2,2,3,3]` in one 10 s flush interval give a COUNT of 15, a RATE of 1.5, and a GAUGE of the last value.

Data sent to the Datadog API is not aggregated, except distributions.

Query-time conversion: `as_count()` shows a metric as the absolute change over the rollup interval; `as_rate()` shows it per second. Because `as_count()` depends on the rollup interval, graphing a longer window changes the graph shape.

Gotcha: changing the type in the Metrics Summary side panel changes behaviour in all existing visualizations and monitors and can make historical data meaningless.

## Verify
- The Metrics Summary side panel shows the intended type after the first submission.

## Checked
2026-11-03. Confirmed against the Metrics Types, Distributions and Type Modifiers pages of the Datadog docs: the type list and in-app mapping, Not Assigned behaviour, histogram aggregates and defaults, distribution aggregations and percentile enabling, the worked example, and `as_count()`/`as_rate()`. Removed: DogStatsD examples moved to the dogstatsd skill, the unsupported claim that the type is fixed at first submission "in some paths", the percentiles-affect-billing wording, and generic Metrics Summary advice.
Method: documentation only; no commands were run.
