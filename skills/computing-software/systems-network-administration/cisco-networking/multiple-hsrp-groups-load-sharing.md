---
id: computing-software.systems-network-administration.cisco-networking.multiple-hsrp-groups-load-sharing
name: multiple-hsrp-groups-load-sharing
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, fhrp, hsrp, mhsrp, hsrp-load-sharing, multiple-hsrp-groups, stp-root-alignment]
level: practitioner
status: draft
description: "Share load across two gateways with multiple HSRP groups (MHSRP) per VLAN or per subnet, aligned with STP roots, and verify each router is active for its half."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/hot-standby-router-protocol-hsrp/9234-hsrpguidetoc.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipapp_fhrp/configuration/xe-16/fhp-xe-16-book/fhp-hsrp-mgo.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multiple HSRP groups for load sharing (MHSRP)

## Idea
HSRP has one active router per group. To use both routers, make R1 active for some groups and
R2 for others.

## Per-VLAN split (common campus design)
```
! R1: active for odd VLANs
interface Vlan10
 standby version 2
 standby 10 ip 10.10.0.1
 standby 10 priority 110
 standby 10 preempt
interface Vlan11
 standby 11 ip 10.11.0.1
 standby 11 priority 90
 standby 11 preempt
! R2: mirror image (90 on Vlan10, 110 on Vlan11)
```
Align STP: R1 is root for VLAN 10, R2 root for VLAN 11, so L2 and L3 paths match (see fhrp-stp-root-alignment).

## Two groups on one subnet
```
interface Vlan20
 standby 1 ip 10.20.0.1
 standby 1 priority 110
 standby 1 preempt
 standby 2 ip 10.20.0.2
 standby 2 preempt
```
Hand half the hosts gateway .1 and half .2 (two DHCP pools/scopes). Clunky; GLBP or a routed
access design is often better if you need per-host balancing in one subnet.

## Gotchas
- Preempt on both routers or failback never happens. Add `standby X preempt delay minimum 60`
  so a reloading router waits for its routing to converge.
- Track uplinks (`standby 10 track 1 decrement 30`) on each group, not just one.
- Each group uses its own virtual MAC (v2: 0000.0C9F.Fxxx); check MAC table scale on large estates.

## Verify
```
show standby brief
P indicates configured to preempt.
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Vl10        10   110 P Active  local           10.10.0.3       10.10.0.1
Vl11        11   90  P Standby 10.11.0.3       local           10.11.0.1
```
- [ ] Each router is Active for its intended half.
