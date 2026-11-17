---
id: computing-software.systems-network-administration.nagios-core.notification-escalations
name: notification-escalations
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, escalations, notification-escalation, first-notification, last-notification, overlapping-escalations, escalation-recovery]
level: advanced
status: docs-checked
description: "How Nagios Core escalations pick recipients by notification number, how overlapping ranges, intervals of 0 and recovery notices behave."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/escalations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Escalation behaviour

- Escalation applies only when at least one escalation definition matches the notification number; otherwise the object's default `contact_groups` are used.
- `first_notification` / `last_notification` give the range; `last_notification 0` means no upper bound.
- Numbers outside all ranges fall back to the default groups.
- Carry lower-level groups into higher levels so earlier recipients keep being notified.

## Overlap
Overlapping ranges are allowed; all matching groups are notified. With ranges 3-5 and 4-0: notice 3 goes to level one; 4 and 5 go to all three groups; 6+ goes only to the second level's group.

## Recovery
A recovery counts as the next notification number but only contacts who got the most recent problem notice are told.

## Intervals
`notification_interval` in an escalation replaces the default for that range. With overlaps the smallest applicable interval wins. `0` sends only the first notice of the range and stops, so any later unreachable escalation has no effect.

## Limits
`escalation_period` (default always valid) must sit inside `notification_period`. `escalation_options` restricts by state; omitted = all.

Syntax: `computing-software.systems-network-administration.nagios-core.escalation-definition`.

## Checked

2026-11-04. Confirmed on the Escalations page: escalation only when a definition matches, holes fall back to default groups, carry lower groups into higher levels, overlapping ranges (3-5 and 4-0 example), recovery goes only to those told of the last problem, notification_interval replacement with smallest wins and 0 meaning one notice, escalation_period subset of the notification period; escalation_options on the object definitions page. Nothing removed.

Method: documentation only; no commands were run.
