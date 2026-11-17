---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-timestamps-and-time-functions
name: promql-timestamps-and-time-functions
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, promql, timestamp-metrics, time-functions, timestamp, time, unix-timestamp, last-success, freshness-alerts, age, staleness, backup-age, cronjob-monitoring, day-of-week, hour, days-in-month, month, year, minute, time-of-day-alerts, process-start-time, node-boot-time, pca]
level: practitioner
status: verified
description: "Use timestamp-valued metrics and PromQL time functions: time(), timestamp(), freshness and age alerts for backups/cron/pushes, uptime from *_start_time_seconds, and time-of-day/day-of-week conditions."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/", "https://prometheus.io/docs/practices/instrumentation/#timestamps-not-time-since", "https://prometheus.io/docs/prometheus/latest/querying/basics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timestamp metrics and time functions

**Goal:** express "how old is X" and "did Y happen on time" correctly, using the
instrumentation convention of exporting Unix timestamps rather than ages.

## 1. The convention: export *when*, not *how long ago*
Expose `mysql_backup_last_success_timestamp_seconds 1760522400` (a gauge holding a Unix
time). Never `backup_age_seconds`: the exporter would have to be scraped to update it and it
goes stale wrongly when the exporter dies. Age is then a query:
```promql
time() - mysql_backup_last_success_timestamp_seconds > 36 * 3600
```
`time()` is the **evaluation time** of the query (not wall-clock when run over a range),
so the alert and graphs stay consistent in `query_range` and in rule evaluation.
The metric names used below exist in their projects (Pushgateway `push_time_seconds`, kube-state-metrics
`kube_cronjob_status_last_successful_time`, blackbox `probe_ssl_earliest_cert_expiry`, node_exporter
`node_boot_time_seconds`, client libraries `process_start_time_seconds`).

## 2. The functions
| Function | Returns |
|---|---|
| `time()` | scalar; evaluation timestamp in seconds |
| `timestamp(v)` | per-series scalar-ish vector: the timestamp of each sample in `v` (when it was scraped) |
| `minute(v)`, `hour(v)`, `day_of_week(v)` (0=Sunday), `day_of_month(v)`, `day_of_year(v)`, `days_in_month(v)`, `month(v)`, `year(v)` | from Unix-time values in `v` (default `v = vector(time())`); all **UTC** |
| `vector(s)` | scalar → single series with no labels |

## 3. Patterns
```promql
# process uptime (restart detection)
time() - process_start_time_seconds < 300            # restarted in last 5m
changes(process_start_time_seconds[1h]) > 2          # flapping

# node uptime and reboot
time() - node_boot_time_seconds

# freshness of a pushed/batch metric (Pushgateway)
time() - push_time_seconds{job="nightly_export"} > 26 * 3600

# "last scrape of this series" — detects silently stuck exporters even when up==1
time() - timestamp(some_slow_updating_metric) > 600

# CronJob last successful run (kube-state-metrics)
time() - max by (namespace, cronjob) (kube_cronjob_status_last_successful_time) > 2 * 3600

# certificate expiry (blackbox / x509 exporters)
(probe_ssl_earliest_cert_expiry - time()) / 86400 < 14

# business hours only (UTC!) — ticket-level alert
(my_condition) and on() (hour() >= 8 < 18) and on() (day_of_week() >= 1 <= 5)

# end-of-month batch window
days_in_month() - day_of_month() < 2
```
`and on()` with a time condition works because `hour()` etc. return a labelless series;
`on()` matches it against every series on the left.

## 4. Local time zones
Time functions are UTC only. For London/Sydney business hours either:
- compute with an offset: `hour(vector(time() + 1*3600))` (breaks across DST changes), or
- keep alert rules UTC-agnostic and move time-based muting into Alertmanager
  `time_intervals` with `location: Europe/London` (correct across DST; preferred), or
- in Grafana use the dashboard time zone for display only.

## 5. Timestamps as values vs explicit sample timestamps
Exposing `metric 1 1700000000000` (a sample timestamp in the text format) is different and
usually wrong. The exporter guidance is that you should not set timestamps on the metrics you expose and should
let Prometheus do it (use the Pushgateway if you think you need them), and series that stop being exported
while carrying their own timestamps keep their last value for 5 minutes by default before disappearing
(querying docs, staleness). Keep timestamps **as the value** of a gauge.

## Gotchas
- `timestamp(rate(x[5m]))` returns the evaluation time, not a sample time, because the
  inner expression is computed, not scraped.
- `time()` inside a recording rule records the evaluation time each cycle; recording
  `time() - last_success` as a series stores an age that is then valid only at that cycle.
  Record the raw timestamp instead and compute the age in the alert.
- Over long ranges Grafana shows `time() - x` as a sawtooth: correct, each success resets it.
- A timestamp metric reset to 0 (exporter bug) makes age enormous and fires every alert;
  guard with `and x > 0`.

## Checked
Run on Prometheus 3.15.0: `hour()` with no argument returned the current UTC hour; `vector(1) and on() (hour() >= 8 < 18) and on() (day_of_week() >= 1 <= 5)` returned the series inside the window and nothing for `hour() >= 12 < 18` at 10:05 UTC on a Monday; `hour(vector(time() + 1*3600))` returned 11 at 10:05 UTC; `days_in_month() - day_of_month()` returned 12 on 19 October; `timestamp(rate(c[5m]))` returned the evaluation time, `timestamp(sparse)` the sample time.

## Verify
- [ ] Every "last success" metric is a Unix-time gauge named `*_timestamp_seconds` or `*_time_seconds`.
- [ ] Age alerts use `time() - metric` and have a `> 0` guard.
- [ ] Business-hours logic lives in Alertmanager `time_intervals` with an explicit `location`.
