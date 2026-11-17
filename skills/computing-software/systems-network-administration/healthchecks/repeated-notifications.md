---
id: computing-software.systems-network-administration.healthchecks.repeated-notifications
name: repeated-notifications
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, repeated-alerts, pagerduty-escalation, pushover-emergency, email-reminders]
level: practitioner
status: docs-checked
description: "Keep Healthchecks alerts coming while a check stays down using incident systems, Pushover Emergency priority or hourly and daily email reminders."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/configuring_notifications.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_configuration.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To keep getting notified while a check is down, you have these options:

1. Incident management systems: PagerDuty, Splunk On-Call, Opsgenie and PagerTree let you configure escalation rules.
2. Pushover with "Emergency" priority: Pushover repeats a loud alert every 5 minutes until acknowledged.
3. Email reminders: hourly or daily reminders while any check in any of your projects is down. Configure under Account Settings, Email Reports.

Self-hosted Pushover tuning:
- `PUSHOVER_EMERGENCY_RETRY_DELAY` (default 300): seconds between repeated emergency notifications.
- `PUSHOVER_EMERGENCY_EXPIRATION` (default 86400): seconds the notifications keep being retried.

Self-hosted note: reminders and reports are sent by `sendreports`, which must run (`--loop` runs it continuously).

## Checked

2026-11-04. Confirmed against the Healthchecks Configuring Notifications page, server configuration page and README: the three options (incident systems, Pushover Emergency every 5 minutes, hourly or daily email reminders), PUSHOVER_EMERGENCY_RETRY_DELAY default 300, PUSHOVER_EMERGENCY_EXPIRATION default 86400, and sendreports with --loop. Removed the one-alert-per-change statement and the closing combine advice, which the pages do not state.

Method: documentation only; no commands were run.
