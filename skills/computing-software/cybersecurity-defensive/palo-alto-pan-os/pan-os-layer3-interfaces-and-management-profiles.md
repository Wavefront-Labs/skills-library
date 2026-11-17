---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-layer3-interfaces-and-management-profiles
name: pan-os-layer3-interfaces-and-management-profiles
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [layer3-interfaces, pan-os, ethernet, interface-management-profile, subinterface, dhcp-client]
level: practitioner
status: draft
description: "Configure PAN-OS Layer 3 ethernet interfaces, 802.1Q subinterfaces, management profiles and bind them to zone and virtual router."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/networking/configure-interfaces/layer-3-interfaces"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: a routable L3 interface that is usable: IP, zone, virtual router, management profile.

```
configure
set network profiles interface-management-profile MP-PING ping yes
set network interface ethernet ethernet1/1 layer3 ip 192.0.2.2/24
set network interface ethernet ethernet1/1 layer3 interface-management-profile MP-PING
set network interface ethernet ethernet1/2 layer3 units ethernet1/2.100 tag 100 ip 10.100.0.1/24
set zone untrust network layer3 ethernet1/1
set zone trust network layer3 ethernet1/2.100
set network virtual-router default interface [ ethernet1/1 ethernet1/2.100 ]
commit
```

A new interface needs all three of: IP, zone, and virtual router membership. Missing any one yields a link that is up but passes nothing (no route, or no zone for policy).

Notes
- DHCP client: `set network interface ethernet ethernet1/1 layer3 dhcp-client enable yes create-default-route yes`.
- A management profile permits services (ping, ssh, https, snmp, response pages) to the firewall itself on that interface; leave it off the untrust interface unless needed.
- Subinterface tags are locally significant to the parent port; the switch port must be a trunk allowing that VLAN.

Gotchas
- An interface in the wrong zone is the usual cause of "policy not matching"; the zone drives rule lookup.
- Speed or duplex mismatch shows as input errors in `show interface ethernet1/1`.

## Verify
```
show interface ethernet1/1
show interface logical
ping source 192.0.2.2 host 192.0.2.1
```
Link state should read up/up and the zone column in `show interface logical` must be populated.
