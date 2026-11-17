---
id: computing-software.systems-network-administration.cisco-networking.fhrp-stp-root-alignment
name: fhrp-stp-root-alignment
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, stp-hsrp-alignment, hsrp, spanning-tree, root-bridge, distribution-layer, campus-design, suboptimal-path]
level: practitioner
status: draft
description: "Align the HSRP/VRRP active gateway with the STP root per VLAN at the distribution layer so traffic does not cross the inter-distribution link twice; includes odd/even splits."
sources:
  - https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Campus/HA_campus_DG/hacampusdg.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Aligning FHRP active with the STP root

In a looped Layer 2 access design (VLANs spanning both distribution switches), STP blocks one
access uplink. If the STP root is DIST-A but the HSRP active gateway is DIST-B, every packet goes
access -> DIST-A -> inter-distribution link -> DIST-B -> routed. The inter-dist link carries all user
traffic and becomes a bottleneck.

## Rule
For each VLAN: STP root primary = HSRP active = (optionally) the PIM DR. Secondary root = standby.

## Odd/even split for load sharing
```
! DIST-A
spanning-tree vlan 10,30,50 root primary
spanning-tree vlan 20,40,60 root secondary
interface Vlan10
 standby 10 ip 10.10.0.1
 standby 10 priority 110
 standby 10 preempt
interface Vlan20
 standby 20 ip 10.20.0.1
 standby 20 priority 90
 standby 20 preempt
! DIST-B: the mirror image
```
Use `preempt` on both so the alignment returns after a failure/recovery, with a preempt delay so
the gateway does not take over before routing has converged.

## Check alignment
```
show spanning-tree root | include VLAN0010|VLAN0020
show standby brief
```
Script it: for every VLAN compare the root bridge ID with the HSRP active address; any mismatch is
a finding. Re-check after maintenance; a reload with no preempt can leave them misaligned.

## Better: avoid the problem
- Routed access (L3 to the access switch) or VLANs confined to one access switch (loop-free U or
  V topology): no STP blocking, both uplinks forward, FHRP at access or not needed.
- StackWise Virtual / MLAG at distribution with MEC: one logical gateway, STP sees no loop.

## Gotchas
- GLBP intentionally uses both distribution switches; with a blocked STP uplink half the traffic
  still crosses the inter-dist link. Cisco guidance: avoid GLBP in looped topologies.
- VRRP has preempt on by default; HSRP does not.
- MST: alignment is per instance; map odd/even VLANs to two instances with different roots.

## Verify
- [ ] Per VLAN, STP root and FHRP active are the same switch.
- [ ] Inter-distribution link utilisation drops to failover-only levels.
