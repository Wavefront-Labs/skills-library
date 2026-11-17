---
id: computing-software.networking-hardware-and-wireless.juniper-junos.security-zones
name: security-zones
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, security-zones, srx-zones, host-inbound-traffic, screens]
level: practitioner
status: draft
description: "Define SRX security zones, assign interfaces, set host-inbound-traffic and apply screens."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SRX security zones
Goal: segment an SRX into trust boundaries.

```
set security zones security-zone trust interface ge-0/0/1.0
set security zones security-zone trust host-inbound-traffic system-services ssh
set security zones security-zone trust host-inbound-traffic system-services ping
set security zones security-zone untrust interface ge-0/0/0.0
set security zones security-zone untrust screen UNTRUST-SCREEN
set security screen ids-option UNTRUST-SCREEN icmp ping-death
set security screen ids-option UNTRUST-SCREEN tcp syn-flood alarm-threshold 1024
```

- Traffic between zones needs a policy; traffic within a zone is permitted by default only if `intra-zone` is allowed (`set security policies default-policy`). Check your release.
- `host-inbound-traffic` governs traffic to the SRX itself, per zone or per interface.
- Traffic is dropped unless an interface is in a zone.

Gotcha: putting an interface into a zone with no host-inbound services silently blocks SSH/ping and OSPF/BGP to the device itself. Add `protocols ospf` or `protocols bgp` under host-inbound too.

## Verify
- `show security zones detail` lists interfaces and services; `ping` and `ssh` to the interface work.
