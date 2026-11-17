---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-utc-time-functions-and-timezones
name: promql-utc-time-functions-and-timezones
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql-timezone, utc-offset-queries, time-functions, business-hours-alerts, promql-timestamps]
level: practitioner
status: gated
description: "PromQL time functions are UTC only: compute local hours and weekdays with offsets, handle DST, and when to move business-hours logic into Alertmanager time_intervals."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/#hour", "https://prometheus.io/docs/alerting/latest/configuration/#time_interval", "https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/modify-dashboard-settings/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UTC time functions and timezones

`hour()`, `minute()`, `day_of_week()`, `day_of_month()`, `day_of_year()`, `days_in_month()`, `month()`, `year()` all return values in **UTC**. With no argument they use the evaluation time (`vector(time())`).

All twelve expressions below were checked with `promtool test rules` (Prometheus 3.15.1) at fixed `eval_time` values, which is how the gate was boundary-tested: for Thu 2026-10-22 20:00 UTC, `hour()` 20, `minute()` 0, `day_of_week()` 4, `day_of_month()` 22, `day_of_year()` 295, `days_in_month()` 31, `month()` 10, `year()` 2026, `(hour() + 10) % 24` 6, `hour(vector(time() + 10*3600))` 6, `day_of_week(vector(time() + 10*3600))` 5 (Friday local, the weekday did change), and `hour() + 10` 30 (the overflow gotcha below).

## Fixed offset
```promql
# local hour for UTC+10 (no DST)
(hour() + 10) % 24
# weekday for UTC+10: shift the timestamp instead of the hour
day_of_week(vector(time() + 10*3600))
# only during 09:00-17:00 local, Mon-Fri, gate an expression
my_expr and on() ((hour(vector(time() + 10*3600)) >= 9) and on() (hour(vector(time() + 10*3600)) < 17))
        and on() (day_of_week(vector(time() + 10*3600)) > 0 < 6)
```
The gate returned 1 at Thu 09:00 and 16:59 local (UTC+10) and nothing at 08:59 and 17:00, nothing for Saturday 09:00 and Sunday 09:00, and 1 for Monday 09:00 (`day_of_week` is 0 for Sunday, so `> 0 < 6` keeps Monday to Friday).

## Daylight saving
PromQL has no timezone database. Options:
- Recording rule producing the current offset from a series you maintain (e.g. an exporter exposing `tz_offset_seconds{tz="Europe/London"}`).
- Better: keep rule expressions timezone-free and do business-hours muting in Alertmanager `time_intervals` with `location: Europe/London` (the docs say the location gives the time zone for the interval; DST transitions were not tested, and on Windows Alertmanager needs the `ZONEINFO` environment variable pointing at a tz database), or Grafana mute timings (gated: unconfirmed, source is paywalled or blocked; Grafana not run).

## Grafana
Dashboards render in browser or dashboard timezone; queries still run in UTC. `$__from`/`$__to` are epoch ms, timezone-independent (gated: unconfirmed, source is paywalled or blocked; Grafana was not run).

## Gotchas
- `hour() + 10` overflows past 23 without `% 24`, and the weekday does not change with it; shift the timestamp for date functions.
- Daily aggregations aligned to midnight UTC (`increase(x[1d])` at 00:00Z) are not local days.

## Verify
- [ ] Business-hours logic tested with `promtool test rules` at boundary times, or moved to Alertmanager time intervals.

## Checked
Prometheus 3.15.1 (windows-amd64) `promtool test rules` with 19 expression/eval_time cases covering the eight UTC functions, the offset arithmetic, the overflow gotcha and seven boundary times for the weekday/hour gate: all passed. Docs read: Alertmanager configuration.md (`location`). Not run: Grafana, DST transitions, a recording rule exposing a timezone offset.
