---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-schedules-and-custom-services
name: fortigate-schedules-and-custom-services
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [firewall-schedule, fortios, recurring-schedule, onetime-schedule, custom-service, service-group, tcp-portrange]
level: practitioner
status: draft
description: "Create FortiGate recurring and one-time schedules and custom service objects with port ranges and groups."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: policies that apply at certain times and to named services.

```
config firewall schedule recurring
    edit "office-hours"
        set start 08:00
        set end 18:00
        set day monday tuesday wednesday thursday friday
    next
end
config firewall schedule onetime
    edit "maint-2026-11-10"
        set start 22:00 2026/11/10
        set end 02:00 2026/11/11
    next
end
config firewall service custom
    edit "ERP-9443"
        set tcp-portrange 9443
        set category "Business"
    next
end
config firewall service group
    edit "WEB-ADMIN"
        set member "HTTPS" "ERP-9443"
    next
end
```
Use the schedule in a policy with `set schedule "office-hours"`. A recurring schedule with an end earlier than the start spans midnight.

Gotchas
- Time zone follows the FortiGate setting; check NTP.
- Sessions that began inside a schedule window may stay up after it ends unless `set schedule-timeout enable` is set in global settings (confirm name).
- Predefined services should be used before custom ones for ICMP and DNS to retain protocol options.

## Verify
```
show firewall schedule recurring
get firewall service custom
diagnose firewall iprope lookup 10.1.0.5 12345 10.1.2.15 9443 tcp port2
```
