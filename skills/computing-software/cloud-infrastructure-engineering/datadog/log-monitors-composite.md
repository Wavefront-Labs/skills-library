---
id: computing-software.cloud-infrastructure-engineering.datadog.log-monitors-composite
name: log-monitors-composite
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, composite-monitor, log-monitor, anomaly, forecast]
level: practitioner
status: docs-checked
description: "Use log count, composite, anomaly and forecast monitors for patterns that simple thresholds miss."
sources: ["https://docs.datadoghq.com/monitors/types/log/", "https://docs.datadoghq.com/monitors/types/composite/", "https://docs.datadoghq.com/monitors/types/anomaly/", "https://docs.datadoghq.com/monitors/types/forecasts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log, composite and anomaly monitors
Goal: alert on log patterns and combined conditions.

Log monitor: choose log count (search bar, no attribute) or the unique value count of an attribute or facet, then a time window and threshold. It evaluates indexed logs only. The default limit is 1000 log monitors per account, so use multi alerts to group.

Composite expression (API): sub-monitors are referenced by ID, for example `1234 && 5678` or `!1234 || 5678`. In the UI they are labelled `a`, `b`, `c` and combined with `&&`, `||`, `!` and parentheses, such as `a || b && !c`.

Anomaly query shape and the documented example:

```
avg(last_1h):anomalies(avg:system.cpu.system{name:cassandra}, 'basic', 3, direction='above', alert_window='last_5m', interval=20, count_default_zero='true') >= 1
```

- A composite uses up to 10 monitors, none of which may itself be a composite. Pick monitors that share the same groups or the composite may never trigger. Deleting a composite does not delete its constituents.
- For `A && B` the result is the least severe status of the two; for `A || B` the most severe. `!A` is OK when A is alert-worthy and Alert when it is not.
- Anomaly algorithms: `basic`, `agile`, `robust`. Seasonality (`hourly`, `daily`, `weekly`) applies to `agile` and `robust`; omit it for `basic`. `direction` is `above`, `below` or `both`.
- Anomaly detection needs history: at least three times the seasonality (three weeks for weekly, three days for daily, three hours for hourly), using up to six weeks of data.
- Forecast monitors alert when a metric is predicted to cross a threshold within a window (12 hours to 3 months custom); algorithms are `linear` (models `default`, `simple`, `reactive`) and `seasonal`.

Gotcha: a new metric shows no `agile` or `robust` bounds for the first few seasons, so these monitors misbehave on new or spiky metrics. `basic` starts showing bounds sooner.

## Verify
- The preview graph shows the expected bands, and the composite status follows its children in Manage Monitors.

## Checked
2026-11-09. Confirmed against the log, composite, anomaly and forecast monitor pages (indexed-logs-only, 1000-monitor limit, composite syntax, 10-monitor and no-nesting limits, status rules, algorithms, seasonality, history requirement, forecast algorithms and window). Removed: the invented `logs("...").index("*").rollup(...)` query string, the `agile` anomaly example (docs require seasonality for it), "one to two weeks of history", the "avoid more than three children" and "stable ID" advice, and the claim that a child deletion breaks the composite (not stated on the page).
Method: documentation only; no commands were run.
