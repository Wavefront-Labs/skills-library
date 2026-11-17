---
id: computing-software.cloud-infrastructure-engineering.alertmanager.route-group-interval
name: route-group-interval
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, group-interval, notification-timing, timeout]
level: practitioner
status: docs-checked
description: "The group_interval route field: recurring timer for notifications about changes in an existing group, default 5m, and its send-timeout side effect."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# group_interval

`group_interval` is how long to wait before sending subsequent notifications for an existing group of alerts after `group_wait`. Default: `5m`. Child routes inherit the parent's value if omitted.

It is a recurring timer that starts as soon as `group_wait` has elapsed. At each tick Alertmanager checks whether any new alerts have fired, or any firing alerts have resolved, since the last tick. If so, a notification is sent. If not, it checks whether the `repeat_interval` has elapsed instead.

Important side effect: `group_interval` also sets the context timeout for the notification pipeline for each send. If sending a notification takes longer than `group_interval`, the notification is canceled. This can happen with small `group_interval` values and slow notification receivers.

The same note appears on per-integration `timeout` fields (webhook, Slack, PagerDuty, incident.io): setting the timeout higher than `group_interval` has no effect.

```yaml
route:
  receiver: team-X-mails
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 3h
```

Alerts that missed the initial `group_wait` are delivered at the next `group_interval`.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): group_interval default, timer and context-timeout note.

Method: documentation only; no commands were run.
