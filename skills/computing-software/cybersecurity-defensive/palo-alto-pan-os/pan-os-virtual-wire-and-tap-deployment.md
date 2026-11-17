---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-virtual-wire-and-tap-deployment
name: pan-os-virtual-wire-and-tap-deployment
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [virtual-wire, pan-os, vwire, tap-mode, transparent-deployment, link-state-pass-through]
level: practitioner
status: draft
description: "Deploy PAN-OS in virtual wire or tap mode as a transparent bump in the wire, with VLAN tag filtering and link-state pass-through."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/networking/configure-interfaces/virtual-wire-interfaces"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: insert the firewall without readdressing or changing routing.

```
configure
set network interface ethernet ethernet1/3 virtual-wire
set network interface ethernet ethernet1/4 virtual-wire
set network virtual-wire VW1 interface1 ethernet1/3 interface2 ethernet1/4
set network virtual-wire VW1 link-state-pass-through yes
set zone vw-in network virtual-wire ethernet1/3
set zone vw-out network virtual-wire ethernet1/4
commit
```
Allow only specific VLANs with `tag-allowed "100-200"` on the virtual wire object. Untagged traffic uses tag 0.

Tap mode: configure one interface as `tap`, place it in a tap zone, connect it to a SPAN port. The firewall sees mirrored traffic only: it logs and generates threat events but cannot block.

Gotchas
- A virtual wire has no L3 presence, so it cannot terminate VPNs, run routing protocols or do routed NAT; use L3 or L2 mode for those.
- By default a virtual wire drops multicast; enable multicast firewalling on the wire if control-plane protocols must pass (confirm LACP and LLDP behaviour in your release).
- Without link-state pass-through, an upstream link failure is invisible to the downstream device.
- Policy for virtual wire zones uses the `virtual-wire` zone type, so interzone defaults apply between the two wire zones.

## Verify
```
show interface ethernet1/3
show session all filter ingress-interface ethernet1/3
```
Traffic should appear in the traffic log with ingress and egress interfaces on opposite ends of the wire.
