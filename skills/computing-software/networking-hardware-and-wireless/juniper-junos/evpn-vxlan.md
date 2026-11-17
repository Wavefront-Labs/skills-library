---
id: computing-software.networking-hardware-and-wireless.juniper-junos.evpn-vxlan
name: evpn-vxlan
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, evpn-vxlan, vxlan, evpn, overlay]
level: practitioner
status: draft
description: "Configure a Junos leaf with EVPN-VXLAN: underlay, overlay iBGP/eBGP EVPN, VLAN to VNI mapping and VTEP source."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EVPN-VXLAN fabric basics
Goal: bring up an EVPN-VXLAN leaf.

```
set protocols bgp group UNDERLAY type external
set protocols bgp group UNDERLAY export LOOPBACK
set protocols bgp group OVERLAY type internal
set protocols bgp group OVERLAY local-address 10.255.0.11
set protocols bgp group OVERLAY family evpn signaling
set protocols bgp group OVERLAY neighbor 10.255.0.1
set switch-options vtep-source-interface lo0.0
set switch-options route-distinguisher 10.255.0.11:1
set switch-options vrf-target target:65000:1
set protocols evpn encapsulation vxlan
set protocols evpn extended-vni-list all
set vlans USERS vlan-id 100
set vlans USERS vxlan vni 10100
```

- Underlay (eBGP or OSPF) provides loopback reachability; overlay carries EVPN routes.
- Syntax differs between QFX (ELS) and MX/vMX, and between releases: confirm on your platform.
- MTU must carry the 50-byte VXLAN overhead.

Gotcha: overlay session up but no MACs means missing `extended-vni-list` or mismatched route targets.

## Verify
- `show evpn database`, `show ethernet-switching vxlan-tunnel-end-point remote`, and `show bgp summary` show EVPN routes learned.
