---
id: computing-software.cloud-infrastructure-engineering.datadog.metric-queries
name: metric-queries
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, metric-query, query-syntax, rollup, formula]
level: practitioner
status: docs-checked
description: "Write Datadog metric queries with space aggregation, tag scope, group by, rollup, fill, top, per_second and formulas."
sources: ["https://docs.datadoghq.com/dashboards/querying/", "https://docs.datadoghq.com/metrics/advanced-filtering/", "https://docs.datadoghq.com/dashboards/functions/rollup/", "https://docs.datadoghq.com/dashboards/functions/interpolation/", "https://docs.datadoghq.com/dashboards/functions/rank/", "https://docs.datadoghq.com/dashboards/functions/rate/", "https://docs.datadoghq.com/metrics/custom_metrics/type_modifiers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metric query syntax
Goal: query metrics precisely.

```
avg:system.cpu.user{env:staging AND (availability-zone:us-east-1a OR availability-zone:us-east-1c)} by {availability-zone}
avg:system.disk.free{*}.rollup(avg, 60)
sum:requests.count{*}.as_count().rollup(sum, weekly, monday)
sum:kubernetes.pods.running{service:*-canary} by {service}
avg:system.disk.in_use{!device:/dev/loop*} by {device}
```

- Shape: `space_aggregator:metric{filter} by {tag}` followed by optional modifiers. The graph editor's space aggregation defaults to `avg by` and can be `max by`, `min by` or `sum by`.
- Filters accept boolean `AND`/`OR`, `IN (...)`, negation with `!`, and wildcards.
- `.rollup(<AGGREGATOR>, <INTERVAL>)` overrides the default time aggregation; aggregators are `avg`, `min`, `max`, `count`, `sum`; interval in seconds. Calendar-aligned form: `.rollup(<AGGREGATOR>, <CALENDAR_UNIT>, <ALIGNMENT>, '<TIMEZONE>')`.
- `.fill(<METHOD>, <LIMIT>)` interpolates gaps: `linear`, `last`, `zero`, `null`; limit in seconds, default 300, maximum 600.
- `top(<METRIC>{*}, <LIMIT_TO>, '<BY>', '<DIR>')`: LIMIT_TO is one of 5, 10, 25, 50, 100; BY one of `max`, `mean`, `min`, `sum`, `last`, `l2norm`, `area`; DIR is `asc` or `desc`.
- `per_second(<METRIC>{*})` graphs the per-second change; `diff(<METRIC>{*})` the delta between intervals; `monotonic_diff` only positive deltas; `timeshift(<METRIC>{*}, -<SECONDS>)` shifts back in time.
- `.as_count()` and `.as_rate()` convert between count and rate forms; as_count depends on the rollup interval.
- Formulas (Advanced... in the graph editor): add queries, which are lettered `a`, `b`, ...; enter `a / b`. Formulas are not lettered, so arithmetic cannot be done between formulas.
- Other documented functions: `moving_rollup`, `anomalies`, `outliers`, `forecast`.

Gotcha: graphs hold at most about 1,500 points per series, so Datadog rolls up automatically (default `avg`) and the default interval depends on the window; a short spike can disappear on a long window. Set an explicit rollup when exact buckets matter.

## Verify
- The JSON tab of the widget shows the same query string.

## Checked
2026-11-03. Confirmed against the Dashboards Querying, Advanced Filtering, Rollup, Interpolation, Rank, Rate and Type Modifiers pages (the examples are from those pages or built from their syntax tables). Removed: the claim about empty series from mismatched scopes, Terraform copy advice, and `moving_rollup`/`anomalies`/`forecast` parameter details.
Method: documentation only; no commands were run.
