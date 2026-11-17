---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-static-routes-and-link-monitor
name: fortigate-static-routes-and-link-monitor
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [static-route, fortios, link-monitor, default-route, distance-priority, routing-table, ecmp]
level: practitioner
status: draft
description: "Add FortiGate static routes with distance and priority, ECMP, and link monitor failover of a default route."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: dual-ISP default routes with automatic failover.

```
config router static
    edit 1
        set dst 0.0.0.0 0.0.0.0
        set gateway 192.0.2.1
        set device "port1"
        set distance 10
        set priority 1
    next
    edit 2
        set dst 0.0.0.0 0.0.0.0
        set gateway 198.51.100.1
        set device "port2"
        set distance 10
        set priority 10
    next
end
config system link-monitor
    edit "isp1"
        set srcintf "port1"
        set server 192.0.2.1
        set protocol ping
        set interval 1000
        set failtime 5
        set update-static-route enable
    next
end
```
Equal distance with different priority means both are installed, the lower priority wins, and ECMP is used only if priorities match. Higher distance on the backup keeps it out of the table until needed.

Gotchas
- SD-WAN is the modern replacement; do not combine both on the same interfaces without understanding that SD-WAN members are routed through the sdwan zone.
- Link monitor with only one target is a false-positive risk; add a second server (`set server 192.0.2.1 203.0.113.1`).
- A static route to an interface without `gateway` on multi-access network creates ARP storms.

## Verify
```
get router info routing-table all
get router info routing-table details 198.51.100.77
diagnose sys link-monitor status
```
Failover test: disconnect port1 and confirm the default route points at port2.
