---
id: computing-software.cloud-infrastructure-engineering.alertmanager.time-interval-fields
name: time-interval-fields
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, time-intervals, weekdays, timezone]
level: practitioner
status: docs-checked
description: "Defining named time_intervals in Alertmanager: times, weekdays, days_of_month, months, years and location, with range syntax and UTC default."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# time_intervals definition

A `time_interval` is a named interval of time referenced from the routing tree to mute or activate routes.

```yaml
time_intervals:
- name: offhours
  time_intervals:
  - times:
    - start_time: '17:00'
      end_time: '24:00'
    weekdays: ['monday:friday']
    location: Australia/Sydney
```

Fields (all lists except `location`):
- `times`: ranges with `start_time` and `end_time` as `HH:MM`, inclusive of the start and exclusive of the end. `17:00` to `24:00` finishes immediately before 24:00.
- `weekdays`: names, with ranges like `monday:wednesday`; the week begins on Sunday. Ranges are inclusive on both ends.
- `days_of_month`: numbers starting at 1; negative values count from month end (`-1` is the last day). `['1:5', '-3:-1']`. Extending past the month is clamped.
- `months`: case-insensitive names or numbers (January = 1); ranges allowed, e.g. `['1:3', 'may:august', 'december']`.
- `years`: e.g. `['2020:2022', '2030']`.
- `location`: an IANA time zone name, `Local`, or `UTC`.

Within a non-empty list at least one element must match; unspecified fields match anything; all fields must match for an instant to match. Without `location`, times are UTC. On Windows only `Local` or `UTC` work unless a custom time zone database is supplied via the `ZONEINFO` environment variable.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): time_interval fields, ranges, UTC default, Windows note.

Method: documentation only; no commands were run.
