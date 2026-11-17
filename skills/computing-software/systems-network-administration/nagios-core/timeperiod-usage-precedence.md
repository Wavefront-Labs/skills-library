---
id: computing-software.systems-network-administration.nagios-core.timeperiod-usage-precedence
name: timeperiod-usage-precedence
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, timeperiod, check-period, notification-period, escalation-period, dependency-period, precedence, blackout, 24x7]
level: practitioner
status: docs-checked
description: "Where Nagios Core time periods apply (check, notification, escalation, dependency), directive precedence order, and the risks of blackout windows."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/timeperiods.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# How time periods are used

| Directive | Where | If omitted |
|---|---|---|
| `check_period` | host/service | active checks any time (24x7) |
| `notification_period` | host/service | - |
| `host_/service_notification_period` | contact | per-contact window, e.g. on call |
| `escalation_period` | escalations | always valid |
| `dependency_period` | dependencies | always valid |

## Precedence (highest first)
1. Calendar date (2008-01-01)
2. Specific month date (January 1st)
3. Generic month date (day 15)
4. Offset weekday of a specific month (2nd Tuesday in December)
5. Offset weekday (3rd Monday)
6. Normal weekday (Tuesday)

Higher entries override lower ones inside one timeperiod.

## Behaviour
- Only regularly scheduled active checks are restricted; on-demand and passive checks are not.
- A check that falls outside the window is rescheduled to the next valid time, possibly hours or days later.
- Times outside the definition are blackouts: status looks unchanged, contacts will most likely not be re-notified of problems, and recoveries are not notified immediately.
- The docs recommend 24x7 periods for host and service checks unless there is a reason.

Syntax: `computing-software.systems-network-administration.nagios-core.timeperiod-definition-syntax`.

## Checked

2026-11-04. Confirmed against the Time Periods page: precedence list, check_period default and rescheduling, on-demand and passive checks not restricted, blackout consequences, notification_period for hosts, services and contacts, escalation_period and dependency_period defaults, and the 24x7 recommendation. Softened the blackout re-notification wording to match the page.

Method: documentation only; no commands were run.
