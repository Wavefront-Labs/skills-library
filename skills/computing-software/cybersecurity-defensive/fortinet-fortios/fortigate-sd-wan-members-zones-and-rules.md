---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-sd-wan-members-zones-and-rules
name: fortigate-sd-wan-members-zones-and-rules
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [sd-wan, fortios, sdwan-zone, sdwan-rule, sdwan-member, steering-rules, load-balance]
level: practitioner
status: draft
description: "Create a FortiGate SD-WAN zone with members and steering rules, and update routes and policies to use it."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: use several WAN links with application-aware steering.

```
config system sdwan
    set status enable
    config zone
        edit "virtual-wan-link"
        next
    end
    config members
        edit 1
            set interface "port1"
            set gateway 192.0.2.1
            set cost 0
        next
        edit 2
            set interface "port2"
            set gateway 198.51.100.1
            set cost 10
        next
    end
    config service
        edit 1
            set name "voice"
            set mode sla
            set dst "all"
            set internet-service enable
            set internet-service-name "Microsoft-Teams"
            set health-check "hc1"
            set priority-members 1 2
        next
    end
end
config router static
    edit 1
        set sdwan-zone "virtual-wan-link"
        set gateway 192.0.2.1
    next
end
```
After enabling SD-WAN, firewall policies must reference the `virtual-wan-link` zone, not member interfaces; remove static routes and policies tied to the member interfaces first.

Gotchas
- Modes: priority, sla, best-quality, load-balance, manual; pick per business traffic.
- The implicit rule (default) uses routing-table source IP hash; add explicit rules for important traffic.
- Rules match on the first packet; for HTTPS apps, classification may take a few packets, so use internet-service (IP DB) matching where possible.

## Verify
```
diagnose sys sdwan member
diagnose sys sdwan service
diagnose sys sdwan health-check
```
Rule `voice` selects the intended member per SLA status.
