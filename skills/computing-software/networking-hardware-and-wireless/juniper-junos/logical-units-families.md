---
id: computing-software.networking-hardware-and-wireless.juniper-junos.logical-units-families
name: logical-units-families
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, logical-units, unit, family-inet, family-inet6]
level: practitioner
status: draft
description: "Configure Junos logical interfaces (units), family inet/inet6/ethernet-switching, and VLAN-tagged subinterfaces."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logical units and address families
Goal: put an IP address or VLAN on a physical port the Junos way.

```
set interfaces xe-0/0/3 description "to core1"
set interfaces xe-0/0/3 unit 0 family inet address 198.51.100.1/30
set interfaces xe-0/0/3 unit 0 family inet6 address 2001:db8:100::1/64
set interfaces xe-0/0/4 vlan-tagging
set interfaces xe-0/0/4 unit 100 vlan-id 100
set interfaces xe-0/0/4 unit 100 family inet address 192.0.2.1/24
set interfaces lo0 unit 0 family inet address 10.255.0.1/32
```

- Every address belongs to a logical unit under a family. `unit 0` is the default.
- Switching ports use `family ethernet-switching` (no IP) and an `irb` or `vlan` L3 interface per VLAN.
- `vlan-tagging` is needed for tagged subinterfaces; `flexible-vlan-tagging` allows mixed.

Gotcha: an address configured on the physical interface name does not exist; it must be under `unit N family X`. Also an interface with no unit has no family and drops IP traffic silently.

## Verify
- `show interfaces xe-0/0/3.0 terse` shows `inet 198.51.100.1/30`.
- `ping 198.51.100.2 count 3` from the host succeeds.
