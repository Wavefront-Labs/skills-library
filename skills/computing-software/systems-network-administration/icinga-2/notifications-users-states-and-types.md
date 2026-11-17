---
id: computing-software.systems-network-administration.icinga-2.notifications-users-states-and-types
name: notifications-users-states-and-types
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, notifications, user-object, states, types, recovery, notification-template, user-groups]
level: practitioner
status: docs-checked
description: "Configure Icinga 2 notifications: User states and types filters, Notification templates and apply rules, user_groups, recovery rules."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# notifications: users, states and types
Icinga 2 cannot send notifications by itself; it relies on external scripts via NotificationCommand objects. No notifications go out while a host/service is in downtime, a problem is acknowledged, or dependencies mark it unreachable. The `notification` feature must be enabled.

A notification needs one or more `users` and/or `user_groups`. Users carry the custom attributes the command uses:
```
object User "icingaadmin" {
  display_name = "Icinga 2 Admin"
  enable_notifications = true
  states = [ OK, Warning, Critical ]
  types = [ Problem, Recovery ]
  email = "icinga@localhost"
}
```
If `states` and `types` are not set on the User object, all states and types are notified. Available types: Problem, Acknowledgement, Recovery, Custom, FlappingStart, FlappingEnd, DowntimeStart, DowntimeEnd, DowntimeRemoved. States: OK, Warning, Critical, Unknown.

Put shared attributes (`interval`, `command`, `states`, `types`, `period`) in a `template Notification` and import it in apply rules:
```
apply Notification "x" to Service {
  import "generic-notification"
  users = [ "noc-xy" ]
  assign where ...
}
```
Only users notified of a problem earlier receive Recovery notifications. The docs state Icinga 2 v2.10 allows a User with only Acknowledgement and/or Recovery types and no Problem, which is useful for ticket systems.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/.
Fixed: the all-states/all-types default when unset applies to the User object. No commands were run.
