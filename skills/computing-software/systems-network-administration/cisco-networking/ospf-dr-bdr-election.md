---
id: computing-software.systems-network-administration.cisco-networking.ospf-dr-bdr-election
name: ospf-dr-bdr-election
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ospf, dr-bdr, ospf-priority, designated-router, drother, router-id, type-2-lsa]
level: practitioner
status: docs-checked
description: "How OSPF DR/BDR election works on multi-access segments (priority, router ID, no preemption), how to steer it with ip ospf priority, and how to read show ip ospf interface."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/13689-17.html
  - https://www.rfc-editor.org/rfc/rfc2328
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPF DR/BDR election

On a broadcast network a DR and BDR are elected. DR and BDR establish adjacencies with all other routers; a DROTHER
establishes adjacencies only with the DR and the BDR. The DR multicasts Link State Updates to AllSPFRouters, other
routers send updates and acknowledgements to AllDRouters (accepted only by the DR and Backup), and the network-LSA
(type 2) for the segment is originated by the DR (RFC 2328).

## Election rules (RFC 2328 section 9.4 and the Cisco page)
1. The router with the highest Router Priority wins; a router with priority 0 is ineligible to become DR or BDR.
   Priority is an 8-bit field, default 1, set per interface.
2. A tie goes to the highest Router ID.
3. The election is deliberately sticky: when an interface comes up and a DR already exists, the router accepts that
   DR regardless of its own priority. This makes the DR hard to predict but changes it less often.
4. Hysteresis: no new BDR is chosen until the old BDR has taken over the DR role.
5. The DR need not have the highest priority, the BDR need not have the second highest, and the same router is never
   both for its own calculation. If only one router is eligible it becomes DR and there is no BDR.
6. When the DR changes, the network node in the area graph is replaced and the network and its routers originate
   new LSAs, which is why stability matters.

## Steering it
The Cisco page names `ip ospf priority <number>` (interface command) for the priority, `router-id <32-bit-ip>` under
`router ospf <process-id>` to fix the router ID, and `ip ospf network {broadcast | non-broadcast | point-to-multipoint
[non-broadcast] | point-to-point}` to change network type. The Cisco page says a DR and BDR are elected under the BROADCAST
network type, and that all routers on a link need matching network types to become neighbours.
```
interface Vlan10
 ip ospf priority 255        ! intended DR
interface Vlan11
 ip ospf priority 0          ! never DR/BDR
router ospf 1
 router-id 10.255.0.1
```
Router ID selection without a configured one: the highest loopback address, otherwise the highest interface address,
fixed until OSPF restarts or the ID is changed manually.
Because of rules 3 and 4, a new priority does not displace a sitting DR. Plan priorities before bringing a segment up,
and treat any forced re-election as a disruptive change in a window.

## Reading it (show ip ospf interface)
Fields: State (DR, BDR, DROTHER, Waiting, Point-to-Point), Priority, Designated Router (ID) and interface address,
Backup Designated router, Timer intervals (Hello default 10 s on broadcast and point-to-point, 30 s on NBMA;
Dead four times Hello; Wait equals Dead), Neighbor Count and Adjacent neighbor count. "Waiting" means the interface
is waiting out the wait timer before declaring the DR; it is normal in NBMA.
```
show ip ospf interface <interface>
```

## Checked
Checked 2026-11-08 against the Cisco "What Does the show ip ospf interface Command Reveal" page (priority, router ID,
network types, timers, states) and RFC 2328 (election description, section 9.4 hysteresis, DR role, network-LSA).
Removed: `clear ip ospf process` and interface-bounce advice, DMVPN/Frame Relay hub advice, the 2WAY/DROTHER and
FULL/DR neighbour display claims, and the `show ip protocols` check, none stated on those pages.
Method: documentation only; no commands were run.
