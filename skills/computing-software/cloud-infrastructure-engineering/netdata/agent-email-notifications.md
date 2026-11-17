---
id: computing-software.cloud-infrastructure-engineering.netdata.agent-email-notifications
name: agent-email-notifications
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, health-alarm-notify, email-notifications, duplicate-emails]
level: practitioner
status: docs-checked
description: "Enable Agent email alert notifications via health_alarm_notify.conf, and turn them off on Agents and Parents to avoid duplicates when using Cloud notifications."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/health/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Confirm the system can send mail first (sendmail or an SMTP relay). Then:

```
sudo ./edit-config health_alarm_notify.conf
# SEND_EMAIL="YES"
# DEFAULT_RECIPIENT_EMAIL="you@example.com"
sudo systemctl restart netdata
```

Email is sent by default when an MTA exists.

Cloud alternative: connect nodes, then Space, Notifications, choose an integration (Slack, Amazon SNS, Splunk and others) and set severity filters.

Avoid duplicates: when you use Cloud notifications, set `SEND_EMAIL="NO"` in `health_alarm_notify.conf` on Agents and Parents.

How it works:
- Agents and Parents each evaluate alerts on their own metrics; streaming does not copy alert configs or transitions to Parents.
- Cloud deduplicates transitions by alert name, instance and node; with several sources the highest severity wins (CRITICAL over WARNING over CLEAR).
- Agents and Cloud trigger notifications independently.

Strategies:
- Central: disable health on Children, share alert config across Parents (for example via git or CI/CD), disable Parent email, use only Cloud notifications.
- Edge: set `enable stock health configuration = no` on Children and define only automation alerts; keep stock alerts on Parents with email disabled.

## Checked

2026-11-04. Confirmed against the Netdata Health README: SEND_EMAIL and DEFAULT_RECIPIENT_EMAIL, the sendmail or SMTP relay check, email by default when an MTA exists, Cloud integrations and severity filters, the duplicate-email fix with SEND_EMAIL="NO", independent evaluation without alert propagation, Cloud deduplication with CRITICAL over WARNING over CLEAR, and both strategies. Nothing removed.

Method: documentation only; no commands were run.
