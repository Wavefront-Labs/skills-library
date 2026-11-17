---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alerts-and-alerts-for-state-series
name: alerts-and-alerts-for-state-series
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [alerts-metric, alerts-for-state, alerting-rules, alert-history, promql, meta-monitoring]
level: practitioner
status: docs-checked
description: "Query the synthetic ALERTS and ALERTS_FOR_STATE series for alert history, firing counts and time-in-alert reports, and know what each series holds."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/#inspecting-alerts-during-runtime", "https://prometheus.io/docs/prometheus/latest/command-line/prometheus/", "https://prometheus.io/docs/prometheus/latest/querying/functions/", "https://raw.githubusercontent.com/prometheus/prometheus/main/rules/alerting.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ALERTS and ALERTS_FOR_STATE

For pending and firing alerts Prometheus stores synthetic series:
- `ALERTS{alertname="<alert name>", alertstate="<pending or firing>", <additional alert labels>}`: sample value 1 while the alert is in that state; the series is marked stale when it no longer is (alerting rules page).
- `ALERTS_FOR_STATE{alertname="...", <alert labels>}`: the sample value is the alert's active-since time as a Unix timestamp (Prometheus source, `rules/alerting.go`: `float64(a.ActiveAt.Unix())`). Prometheus uses it to restore the `for` state after a restart, see below.

## Queries
```promql
# currently firing, by severity
count by (severity) (ALERTS{alertstate="firing"})
# time firing in the last 7 days, in hours (samples x rule evaluation interval)
sum by (alertname) (count_over_time(ALERTS{alertstate="firing"}[7d])) * <eval interval seconds> / 3600
# episodes: the value changes whenever the active-since time changes
sum by (alertname) (changes(ALERTS_FOR_STATE[7d]))
# how long an active alert has been active (seconds)
time() - ALERTS_FOR_STATE
```
Replace `<eval interval seconds>` with your rule evaluation interval. `count_over_time` counts the samples in the interval; `changes` counts how often a series' value changed in the range; `time()` is the evaluation time (functions page). The `changes(ALERTS_FOR_STATE)` episode count is an approximation derived from the value being the active-since time.

## Restoring `for` state after a restart
Command-line flags (Prometheus command-line page): `--rules.alert.for-outage-tolerance` (max time to tolerate a Prometheus outage when restoring the `for` state of alerts, default 1h) and `--rules.alert.for-grace-period` (minimum duration between alert and restored `for` state, default 10m, kept only for alerts whose `for` is greater than the grace period).

## Gotchas
- Silencing happens in Alertmanager, not Prometheus, so silenced alerts are still active in Prometheus and appear in `ALERTS`.
- The Alerts tab of the Prometheus UI shows the exact label sets for which each alert is active, which is the quickest cross-check of `ALERTS`.

## Verify
- [ ] `ALERTS{alertstate="firing"}` returns the same label sets the Alerts tab shows as firing.

## Checked
Date: 2026-11-07. Read in full: the Prometheus alerting rules page (ALERTS series and its stale behaviour; the page does not mention ALERTS_FOR_STATE), the command-line flags table (the two `--rules.alert.*` flags and their defaults), and the functions page entries for `changes()`, `time()` and the `*_over_time` list (including `count_over_time`). `ALERTS_FOR_STATE` and its value come from `rules/alerting.go` in the Prometheus repository (the metric name, and the sample value being `ActiveAt.Unix()`); that file is a raw source page (about 20 KB) and I read the constants and the `forStateSample` function and its call site, not the whole file. Removed: the "Thanos/Mimir have them" claim, the "recording rules over ALERTS" remark, the dashboard/meta-alert suggestions and the old Verify step about a paging tool.
Method: documentation only; no commands were run.
