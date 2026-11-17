---
id: computing-software.cloud-infrastructure-engineering.datadog.metric-monitors
name: metric-monitors
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, metric-monitor, threshold-alert, monitor-query, evaluation-window]
level: practitioner
status: docs-checked
description: "Build Datadog metric monitors: pick threshold or change detection, aggregation, evaluation window, thresholds, recovery, evaluation delay and no-data handling."
sources: ["https://docs.datadoghq.com/monitors/types/metric/", "https://docs.datadoghq.com/monitors/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metric monitors
Goal: alert on a metric with sane noise levels. Create at Monitors > New Monitor > Metric.

Detection methods: Threshold (static value; average, min, max or sum over the window), Change (absolute or % change between N minutes ago and now), Anomaly, Outliers and Forecast (each has its own monitor page).

Define the metric: metric (for example `system.cpu.user`), optional `from` filter (default everywhere, for example `env:prod`), aggregation (default `avg by`), group by (for example `host`), monitor query aggregation (default average) and evaluation window (default 5 minutes; presets or custom from 1 minute to 730 hours).

- Aggregation meaning, when alerting above a threshold: `avg` averages the series; `max` alerts if any value crosses; `min` alerts only if all points in the window cross; `sum` sums every point. For monitors that alert below the threshold, max and min behaviour reverses. `percentile(pXX)` is only for distribution metrics.
- Trigger conditions: above, above or equal to, below, below or equal to, equal to, not equal to. A value between zero and one needs a leading zero (`0.3`).
- Thresholds: alert threshold (required) and warning threshold; optional alert and warning recovery thresholds add a recovery condition. Without a recovery threshold a monitor recovers when the value passes back over the alert threshold.
- Data window: "Do not require" (default) evaluates even with one data point, good for sparse data; "Require" waits until the window is filled (first bucket has data and at most three empty buckets).
- Grouping: a query with no group by is a Simple Alert; grouping by a dimension makes it a Multi Alert, which notifies per group. `N/A` groups are not included, so tag keys must have a value.
- Evaluation delay (seconds, non-negative, max 86400): delays evaluation, for example 900 seconds means a 5-minute window evaluated at 7:00 uses 6:40 to 6:45. The docs recommend 15 minutes for cloud metrics (backfilled by providers) and 60 seconds when using a division formula.
- New group delay (default 60 seconds for groups not seen in 24 hours) stops new containers triggering on start-up load.
- On missing data: Evaluate as zero or Show last known status, Show NO DATA, Show NO DATA and notify, Show OK. The monitor must have been able to evaluate data before it can alert on missing data.
- `as_count()` changes evaluation behaviour; see the as_count in monitor evaluations guide before using it.

Gotcha: a very short window alerts on blips; for sparse metrics keep "Do not require" or use Evaluate as zero deliberately, since zero will not breach a `> N` threshold.

## Verify
- The preview graph shows the threshold marker, and a test notification renders the message.

## Checked
2026-11-03. Confirmed against the Metric monitor and Monitor configuration pages. Removed: the JSON monitor body and its option names (`critical_recovery`, `notify_no_data`, `renotify_interval`, `evaluation_delay`) and the `avg(last_5m):...` query string (not on the pages read), the "last_1m" advice, and the team/service tag and quarterly review advice.
Method: documentation only; no commands were run.
