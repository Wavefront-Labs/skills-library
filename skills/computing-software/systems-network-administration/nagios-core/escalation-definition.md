---
id: computing-software.systems-network-administration.nagios-core.escalation-definition
name: escalation-definition
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, serviceescalation, hostescalation, escalation-options, escalation-period, define-serviceescalation, define-hostescalation]
level: practitioner
status: docs-checked
description: "Write Nagios Core serviceescalation and hostescalation objects: directives, escalation_options letters, required contacts, and inheritance of blank fields."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectdefinitions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Escalation objects

Directives for both: `host_name`, `hostgroup_name`, (`service_description` for services), `contacts`, `contact_groups`, `first_notification`, `last_notification`, `notification_interval`, `escalation_period`, `escalation_options`.

- At least one contact or contact group is required.
- `last_notification 0` = never ends.
- `notification_interval 0` = send the first escalated notice, then no more problem notices until recovery.
- `escalation_period` omitted = always valid.
- For service escalations, blank optional directives inherit from the service object (stated on the page for service escalations only).
- `escalation_options`: service `r,w,u,c`; host `r,d,u`. Omitted = all states.

```
define serviceescalation {
    host_name              nt-3
    service_description    Processor Load
    first_notification     4
    last_notification      0
    notification_interval  30
    contact_groups         all-nt-admins,themanagers
}
define hostescalation {
    host_name              router-34
    first_notification     5
    last_notification      8
    notification_interval  60
    contact_groups         all-router-admins
}
```

Wildcard targeting: `computing-software.systems-network-administration.nagios-core.wildcards-and-exclusion`. Semantics: `computing-software.systems-network-administration.nagios-core.notification-escalations`.

## Checked

2026-11-04. Confirmed against the Service Escalation and Host Escalation sections of the object definitions page: directive lists, at least one contact or contact group, last_notification 0, notification_interval 0, escalation_period default, escalation_options letters (service r,w,u,c; host r,d,u) and both examples. Narrowed the inheritance statement to the case the page documents.

Method: documentation only; no commands were run.
