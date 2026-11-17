---
id: computing-software.cloud-infrastructure-engineering.alertmanager.mute-and-active-time-intervals
name: mute-and-active-time-intervals
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, mute-time-intervals, active-time-intervals, routing-tree]
level: practitioner
status: docs-checked
description: "Using mute_time_intervals and active_time_intervals on routes to silence or enable notifications on a schedule, and how they interact with continue."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Muting and activating routes by time

Routes reference named entries from the top-level `time_intervals` section.

- `mute_time_intervals`: times when the route should be muted. A muted route sends no notifications but otherwise acts normally, including ending the route-matching process if `continue` is not set.
- `active_time_intervals`: times when the route should be active. An empty value means always active. The route sends notifications only when active, but otherwise acts normally, again including ending matching unless `continue` is set.
- The root node cannot have any mute times or active times.

The top-level `mute_time_intervals` list is deprecated; use `time_intervals`.

Example from the reference:

```yaml
routes:
- receiver: 'dev-pager'
  matchers:
    - service="inhouse-service"
  mute_time_intervals:
    - offhours
    - holidays
  continue: true
- receiver: 'on-call-pager'
  matchers:
    - service="inhouse-service"
  active_time_intervals:
    - offhours
    - holidays
```

The first route is muted during off hours and holidays but, because `continue: true`, the alert goes on to the second route, which notifies only during those intervals. Together they give a day/night split for the same alerts.

## Checked

2026-11-08. Confirmed against the Alertmanager configuration reference source (prometheus/alertmanager, docs/configuration.md, main branch, read in full), the published form of the cited prometheus.io page: the mute and active time interval route example. Removed: nothing.

Method: documentation only; no commands were run.
