---
id: computing-software.cloud-infrastructure-engineering.alertmanager.route-group-wait
name: route-group-wait
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, group-wait, notification-timing, flapping]
level: practitioner
status: docs-checked
description: "The group_wait route field: delay before the first notification of a new alert group, default 30s, and its effect on inhibition and flapping."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# group_wait

`group_wait` is how long to wait before sending the first notification for a new group of alerts. Default: `30s`. If omitted, child routes inherit the parent's value.

Why it exists: it lets alerts arrive from other rule groups or Prometheus servers, and lets one or more inhibiting alerts arrive and mute target alerts before the first notification goes out.

Trade-offs stated in the reference:
- A short `group_wait` reduces time to first notification, but the first notification might not contain the complete set of expected alerts, and alerts that should be inhibited might not be inhibited if the inhibiting alerts have not arrived in time.
- A long `group_wait` means notifications for firing alerts might not be sent within a reasonable time.

Flapping: if an alert is resolved before `group_wait` has elapsed, no notification is sent for it. A notification for any alerts that missed the initial `group_wait` is sent at the next `group_interval` instead.

```yaml
route:
  receiver: default-receiver
  group_wait: 30s
  routes:
  - receiver: database-pager
    group_wait: 10s
    matchers:
    - service=~"mysql|cassandra"
```

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): group_wait default, rationale and trade-offs.

Method: documentation only; no commands were run.
