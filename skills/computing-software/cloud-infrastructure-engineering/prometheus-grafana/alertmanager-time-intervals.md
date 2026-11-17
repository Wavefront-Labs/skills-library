---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanager-time-intervals
name: alertmanager-time-intervals
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [alertmanager, time-intervals-config, maintenance-windows, mute-time-intervals, active-time-intervals, business-hours-routing]
level: practitioner
status: verified
description: "Use Alertmanager time_intervals with mute_time_intervals and active_time_intervals for business-hours routing and recurring maintenance windows, including time zones."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/#time_interval"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alertmanager time_intervals

```yaml
time_intervals:
  - name: business-hours
    time_intervals:
      - weekdays: ['monday:friday']
        times: [{start_time: '09:00', end_time: '17:30'}]
        location: Australia/Brisbane          # IANA tz; default UTC
  - name: weekly-maintenance
    time_intervals:
      - weekdays: [sunday]
        times: [{start_time: '02:00', end_time: '04:00'}]
        location: Europe/London
  - name: christmas-freeze
    time_intervals:
      - months: [december]
        days_of_month: ['24:31']
      - months: [january]
        days_of_month: ['1']

route:
  receiver: default
  routes:
    - matchers: [severity="ticket"]
      receiver: jira
      active_time_intervals: [business-hours]     # only notify during these
    - matchers: [severity="page", team="data"]
      receiver: data-pager
      mute_time_intervals: [weekly-maintenance]   # suppress during these
```

## Semantics
- An interval matches if **all** specified fields match (weekdays AND times AND months ...); unspecified fields match
  everything. Multiple entries under one name are ORed. Run: a name with a `years: ['2020']` entry and a second all-weekdays entry muted a route; one entry with weekdays AND `years: ['2020']` did not.
- `times` end is exclusive (docs); `days_of_month` supports negatives (`-1` = last day) and ranges such as `['24:31']` (docs; `check-config` accepts the December/January freeze above, and an alert routed to that interval notified in October as expected).
- `mute_time_intervals` and `active_time_intervals` are set on a route, are NOT inherited by child routes, and cannot be set on the root route (docs). Run: a child of a muted route with its own receiver still notified, while an alert that stopped at the muted route did not.
- Muted/inactive alerts are not dropped: they stay in Alertmanager and notify when the interval ends if still firing (subject to group/repeat intervals). Run: an alert muted by a `time_intervals` window with `start_time`/`end_time` one minute apart was delivered to the webhook about one second after the window ended (13:05:01 local for a window ending 03:05 UTC). While muted, `GET /api/v2/alerts` still showed `state: active` with empty `mutedBy`, so time-interval mutes are not visible there.
- Top-level `mute_time_intervals` is deprecated in favour of `time_intervals` (configuration docs).
- `location` needs a tz database: with no zoneinfo on Windows, `amtool check-config` failed `unknown time zone Australia/Brisbane (on Windows platforms, you may have to pass the time zone database using the ZONEINFO environment variable ...)`. Setting `ZONEINFO` to Go's `zoneinfo.zip` fixed it. Without `location` times are UTC.

## When to use what
| Need | Use |
|---|---|
| Recurring windows (weekly maintenance, nights for tickets) | time_intervals |
| One-off maintenance | silence (amtool/API) with expiry |
| Suppress alerts caused by another alert | inhibit_rules |

## Verify
- [ ] `amtool check-config` passes (it validates the interval definitions and `location`). `amtool config routes show` and `routes test` do not print `mute_time_intervals` or `active_time_intervals` (run), so verify them by reading the config and by the delivery check below.
- [ ] A ticket-severity test alert sent outside the window is delivered only when the window opens (the equivalent mute-window check above was run with a one-minute window).

## Checked
Alertmanager and amtool 0.34.1 (windows-amd64) with a local webhook listener: `check-config` on the skill's `time_intervals` (fails on Windows without ZONEINFO), then a config with `mute_time_intervals` and `active_time_intervals` on routes (muted, inactive, active, not-inherited cases all matched the docs), a one-minute `times` window (notification after the window ended), OR across list entries and AND within an entry, and a December/January freeze. Docs read: Alertmanager configuration.md (route and time_interval_spec sections).
