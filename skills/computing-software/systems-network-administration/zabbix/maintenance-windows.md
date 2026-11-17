---
id: computing-software.systems-network-administration.zabbix.maintenance-windows
name: maintenance-windows
category: computing-software
field: systems-network-administration
product: zabbix
tags: [maintenance, problem-suppression, no-data-collection, trigger-tags, timer, suppression, window]
level: practitioner
status: docs-checked
description: "Schedule maintenance for hosts, groups or tagged triggers and understand how it interacts with escalations."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/maintenance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Maintenance suppresses problems during planned periods. Define it for hosts and host groups, or restrict it to specific triggers using trigger tags so other triggers on the host keep alerting.

Types:
- With data collection: triggers are processed normally and events are created. If Pause operations for suppressed problems is ticked in the action, escalation steps (notifications, remote commands) are skipped while maintenance lasts.
- No data collection: no values are stored. The server or proxy still collects data regardless of type.

Escalation example from the docs: steps at 0, 30 and 60 minutes with a half-hour maintenance from minute 10 to 40 means steps two and three run 30 minutes later, at 60 and 90. A problem starting during maintenance starts escalating after it ends. Untick Pause operations for suppressed problems to receive notifications normally.

Details:
- Recovery and update operations are not suppressed, only escalations. Recovery notifications are not sent if the problem started during maintenance.
- If at least one host used in the trigger expression is not in maintenance, a problem notification is sent.
- Zabbix server must be running during maintenance.
- Timer processes act at 0 seconds of every minute and each second for period changes, so start and stop speed depends on the configuration update interval (10 seconds by default). Hosts added to an active maintenance are picked up at the next minute.
- When a host enters maintenance, the server reads all open problems to decide on suppression, which can cost performance with many open problems. It also reads them at startup.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (maintenance): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
