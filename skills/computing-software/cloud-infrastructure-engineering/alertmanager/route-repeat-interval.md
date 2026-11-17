---
id: computing-software.cloud-infrastructure-engineering.alertmanager.route-repeat-interval
name: route-repeat-interval
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, repeat-interval, renotification, data-retention]
level: practitioner
status: docs-checked
description: "The repeat_interval route field: default 4h, rounding to group_interval multiples, and the interaction with --data.retention."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# repeat_interval

`repeat_interval` is how long to wait before repeating the last notification. Default: `4h`. If omitted, child routes inherit the parent's value.

Rules from the reference:
- Notifications are not repeated if any new alerts have fired or any firing alerts have resolved since the last `group_interval`; in that case a regular change notification is sent.
- The `repeat_interval` is checked after each `group_interval`, so it should be a multiple of `group_interval`. If it is not, it is rounded up to the next multiple.
- If `repeat_interval` is longer than `--data.retention`, the notification is repeated at the end of the data retention period instead.

```yaml
route:
  receiver: 'default-receiver'
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
```

With these values the group is checked every 5 minutes after the initial 30 seconds, and an unchanged firing group is re-notified once the 4 hour interval has elapsed.

The README example overrides it to `3h` at the root and notes that all timing attributes are inherited by child routes and can be overwritten on each.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration) and the README example: repeat_interval default and rules.

Method: documentation only; no commands were run.
