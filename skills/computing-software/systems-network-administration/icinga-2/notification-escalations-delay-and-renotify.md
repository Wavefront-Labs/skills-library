---
id: computing-software.systems-network-administration.icinga-2.notification-escalations-delay-and-renotify
name: notification-escalations-delay-and-renotify
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, notification-escalation, times-begin-end, interval, renotification, delay]
level: practitioner
status: docs-checked
description: Build Icinga 2 notification escalations and delays with the times dictionary, and disable re-notifications with interval = 0.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# notification escalations, delay and re-notify
**Escalation.** A Notification becomes an escalation when you give it start and end times in the `times` dictionary. Share basics through a template (users, `interval`) and override for the escalation. Example from the docs with a shared `generic-notification` template (interval 15m):
```
apply Notification "escalation-sms-2nd-level" to Service {
  import "generic-notification"
  command = "sms-notification"
  users = [ "icinga-oncall-2nd-level" ]
  times = {
    begin = 30m
    end = 1h
  }
  assign where service.name == "ping4"
}
```
A further escalation can use `begin = 1h` and `end = 2h`. The escalated users are notified only if the problem is neither resolved nor acknowledged. Lower the `interval` in escalations by using a secondary template or overriding it directly.

**Delay.** Set only `begin` (for example `begin = 15m`) to postpone the notification past the HARD state; with no `end` there is no end-time check. Setting `end` to `0` stops notifications immediately, effectively disabling it. Use a relatively low `interval` so you are notified again soon enough.

**Disable re-notifications.** Set `interval = 0` to be notified only once.

SMS needs a provider or local hardware with an active SIM card; the docs' SMS NotificationCommand example is not complete because providers differ.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the Notification Escalations, Notification Delay and Disable Re-notifications sections of the Icinga 2 Monitoring Basics chapter (03-monitoring-basics.md from the Icinga/icinga2 repository, the source of the cited page). Confirmed the times dictionary, template sharing, the 30m to 1h and 1h to 2h escalation windows, the 15m interval note, escalation only while unresolved and unacknowledged, begin-only delay, end = 0 disabling the notification, the interval advice, interval = 0, and the SMS note. Nothing was removed. No commands were run.
