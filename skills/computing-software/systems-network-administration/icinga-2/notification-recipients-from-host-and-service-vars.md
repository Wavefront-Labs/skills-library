---
id: computing-software.systems-network-administration.icinga-2.notification-recipients-from-host-and-service-vars
name: notification-recipients-from-host-and-service-vars
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, notifications, vars-notification, apply-notification, typeof, user-groups, mail, sms]
level: advanced
status: docs-checked
description: Store notification users and groups in host or service vars.notification and apply notifications from them, with typeof safety checks.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# notification recipients from host and service vars
A common pattern keeps users and groups on the host or service, not on the Notification object:
```
object Host "icinga2-agent1.localdomain" {
  vars.notification["mail"] = {
    groups = [ "icingaadmins" ]
    users = [ "icingaadmin" ]
  }
  vars.notification["sms"] = {
    users = [ "icingaadmin" ]
  }
}
```
Then one apply rule per channel copies the nested keys:
```
apply Notification "mail-host-notification" to Host {
  users = host.vars.notification.mail.users
  user_groups = host.vars.notification.mail.groups
  assign where host.vars.notification.mail && typeof(host.vars.notification.mail) == Dictionary
}
```
The `typeof(...) == Dictionary` check guards validation from failing if someone sets e.g. `vars.notification.mail = "yes"`.

To make errors easier to debug, add a safety condition using `log(LogCritical, "config", ...)` when `len(host.vars.notification.mail.users) == 0` and no groups are set. This fails immediately during config validation and names the host; the script debugger gives deeper insight.

For services, inherit from the service first, then the host, then a default user:
```
if (service.vars.notification.mail.users) {
  users = service.vars.notification.mail.users
} else if (host.vars.notification.mail.users) {
  users = host.vars.notification.mail.users
} else {
  users = [ "icingaadmin" ]
}
```
Use `assign where` that accepts the dictionary on either the host or the service.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the Notifications: Users from Host/Service section of the Icinga 2 Monitoring Basics chapter (03-monitoring-basics.md from the Icinga/icinga2 repository, the source of the cited page). Confirmed the host vars.notification example, the mail and sms apply rules, the typeof guard and its failure case, the LogCritical safety condition failing config validation, the script debugger pointer, the service inheritance with default user, and the combined assign where. Nothing was removed. No commands were run.
