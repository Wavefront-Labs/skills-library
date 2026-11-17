---
id: computing-software.systems-network-administration.icinga-2.notification-commands-and-mail-scripts
name: notification-commands-and-mail-scripts
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, notificationcommand, mail-host-notification, mail-service-notification, scripts, mta]
level: practitioner
status: docs-checked
description: Use Icinga 2 NotificationCommand objects and the shipped mail-host and mail-service notification scripts, their arguments, and the MTA requirement.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# notification commands and mail scripts
NotificationCommand objects define how notifications reach external interfaces (email, XMPP, IRC and others) and are referenced by a Notification's `command` attribute. The `notification` feature must be enabled.

The docs advise putting logic in a shell script in `/etc/icinga2/scripts` and having the NotificationCommand call it. A fresh install ships two example scripts, `mail-host-notification.sh` and `mail-service-notification.sh`, wired to NotificationCommand objects `mail-host-notification` and `mail-service-notification` that define default argument values (overridable locally). They need the `mail` binary on the master, which in turn needs a local MTA such as Postfix, Exim or Sendmail.

Required arguments and their defaults (host version):
- `notification_date` = `$icinga.long_date_time$`
- `notification_hostname` = `$host.name$`
- `notification_hostdisplayname` = `$host.display_name$`
- `notification_hostoutput` = `$host.output$`
- `notification_useremail` = `$user.email$`
- `notification_hoststate` = `$host.state$`
- `notification_type` = `$notification.type$`

The service version adds `notification_servicename`, `notification_servicedisplayname`, `notification_serviceoutput` and `notification_servicestate`.

Optional: `notification_hostnotes`, `notification_address`, `notification_address6`, `notification_author`, `notification_comment`, `notification_from` (needs GNU mailutils on Debian/Ubuntu), `notification_icingaweb2url`, and `notification_logtosyslog` (true logs to syslog for debugging; default false).

Users must define every custom attribute the command uses, such as `email`.

## Checked

2026-11-04. Confirmed against the Icinga 2 monitoring basics chapter: NotificationCommand, mail scripts, required and optional arguments with default macros, notification_logtosyslog.

Method: documentation only; no commands were run.
