---
id: computing-software.systems-network-administration.nagios-core.notification-types-methods
name: notification-types-methods
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, notificationtype, notification-commands, notification-methods, email, sms, pager, acknowledgement, flappingstart, downtimestart]
level: practitioner
status: docs-checked
description: "Nagios Core $NOTIFICATIONTYPE$ values (PROBLEM, RECOVERY, ACKNOWLEDGEMENT, FLAPPING*, DOWNTIME*) and how notification delivery works through commands."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/notifications.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Notification types and delivery

## `$NOTIFICATIONTYPE$` values
- **PROBLEM:** entered or stayed in a problem (service WARNING/UNKNOWN/CRITICAL; host DOWN/UNREACHABLE).
- **RECOVERY:** back to OK / UP.
- **ACKNOWLEDGEMENT:** a contact acknowledged the problem in the web UI.
- **FLAPPINGSTART / FLAPPINGSTOP / FLAPPINGDISABLED**
- **DOWNTIMESTART / DOWNTIMESTOP / DOWNTIMECANCELLED:** start suppresses further notices; stop or cancel lets them resume.

Branch on this macro in your notify script so recoveries and acknowledgements are worded correctly.

## Delivery
Nagios does not send messages itself. Contacts reference notification commands (`host_notification_commands`, `service_notification_commands`) that call any script or messaging system. Quickstart installs preconfigure email commands in `commands.cfg` under `/usr/local/nagios/etc/objects/`.

The docs list external tools such as Gnokii, QuickPage and Sendpage for SMS/paging, and Festival, NAS and rplay for audio alerts.

## Related
Filters: `computing-software.systems-network-administration.nagios-core.notification-filters`. Macros valid only in notification commands: `computing-software.systems-network-administration.nagios-core.standard-macro-reference`.

## Checked

2026-11-04. Confirmed against the Notifications page: every NOTIFICATIONTYPE value and description, notification commands as the delivery mechanism, the quickstart email commands in commands.cfg, and the listed Gnokii, QuickPage, Sendpage, Festival, NAS and rplay resources. Removed an unconfirmed self-check.

Method: documentation only; no commands were run.
