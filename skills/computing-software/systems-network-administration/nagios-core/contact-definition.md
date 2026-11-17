---
id: computing-software.systems-network-administration.nagios-core.contact-definition
name: contact-definition
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, contact-definition, define-contact, contactgroup, notification-commands, can-submit-commands, minimum-importance, host-notification-options]
level: practitioner
status: docs-checked
description: "Define Nagios Core contacts: notification enabled flags, periods, option letters, notification commands, email/pager/address fields and can_submit_commands."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectdefinitions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contact definition

`alias` defaults to `contact_name` if omitted.

Directives
- `host_notifications_enabled`, `service_notifications_enabled`: 0/1.
- `host_notification_period`, `service_notification_period`: time periods (can model on-call hours).
- `host_notification_options`: `d,u,r,f,s,n`. `service_notification_options`: `w,u,c,r,f,s,n`.
- `host_notification_commands`, `service_notification_commands`: comma-separated command names.
- `email` (`$CONTACTEMAIL$`), `pager` (`$CONTACTPAGER$`), `address1`-`address6` (`$CONTACTADDRESSn$`).
- `can_submit_commands`: 1 lets the contact send external commands from the CGIs.
- `minimum_importance` (default 0): see notification filters.
- `contactgroups`; `retain_*` need `retain_state_information`.

```
define contact {
    contact_name                    jdoe
    alias                           John Doe
    host_notifications_enabled      1
    service_notifications_enabled   1
    service_notification_period     24x7
    host_notification_period        24x7
    service_notification_options    w,u,c,r
    host_notification_options       d,u,r
    service_notification_commands   notify-by-email
    host_notification_commands      host-notify-by-email
    email                           jdoe@example.com
}
```

Name matching: the CGI login name must equal `contact_name` for the user to see their objects.

## Checked

2026-11-04. Confirmed against the Contact Definition section of the object definitions page: all directives, notification option letters for hosts (d,u,r,f,s,n) and services (w,u,c,r,f,s,n), minimum_importance default 0, address1 to address6, can_submit_commands, retain_* needing retain_state_information, and CGI name matching on the CGI authentication page. Removed the unverifiable 'only contact_name is required' statement.

Method: documentation only; no commands were run.
