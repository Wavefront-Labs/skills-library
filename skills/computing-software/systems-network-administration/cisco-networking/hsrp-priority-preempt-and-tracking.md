---
id: computing-software.systems-network-administration.cisco-networking.hsrp-priority-preempt-and-tracking
name: hsrp-priority-preempt-and-tracking
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, fhrp, hsrp, hsrp-priority, hsrp-preempt, interface-tracking, hsrp-timers, virtual-ip]
level: practitioner
status: docs-checked
description: "Make the HSRP active router deterministic on IOS: priority, preempt with delay, tracked-interface decrements, and how they interact during failover."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/hot-standby-router-protocol-hsrp/9234-hsrpguidetoc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HSRP priority, preempt and tracking

## Model
A set of routers presents one virtual router (virtual IP and MAC) to the LAN. One is Active and forwards; another is
Standby and takes over if the Active fails. After election only the Active and Standby send periodic HSRP messages.
Several groups can coexist on a LAN, each with its own state and timers. HSRP version 1 uses virtual MAC
`0000.0c07.acNN` (NN = group number) on Ethernet.

## Pair (configuration pattern from the Cisco page)
```
interface ethernet0
 ip address 10.1.1.1 255.255.255.0
 standby 1 ip 10.1.1.3
 standby 1 priority 110
 standby 1 preempt delay minimum 10
 standby 1 track serial0 10
```
Peer: its own interface address, same group and virtual IP, a lower priority (the Cisco example pair uses 105 and
100) and `preempt` as well. The page documents the form `standby <group> track <interface> <decrement>`, and says
`standby <group> track <object>` can be used instead on versions where the interface form is not available. If no
group number is given, the group is 0.

## How the numbers work
- Priority decides first, then the interface IP address; higher wins in both cases.
- **Preemption** lets the highest-priority router become Active immediately. It sends a coup message; a lower-priority
  Active that receives a coup (or a hello from a higher-priority Active) goes to Speak state and sends a resign
  message. Without `preempt`, a recovered primary does not take over.
- **Preempt delay** postpones preemption so the router can populate its routing table before becoming Active. From
  IOS 12.0(9) the delay starts when preemption is first attempted, not at reload.
- **Interface tracking** lowers the priority when the tracked interface's line protocol goes down; another router
  with preempt and a higher resulting priority then becomes Active. Decrements are cumulative: with two tracked
  interfaces and the default decrement of 10, priority 110 becomes 100 and then 90. Choose the decrement so the
  primary falls below the standby (the page's 110 with a decrement of 10 reaches 100 after one failure).
- Authentication is a shared clear-text key in the HSRP packets (`standby authentication <string>`).

## Verify (not run here; confirm on your release)
- [ ] Both routers agree on group, virtual IP and key; one Active, one Standby.
- [ ] Shut the tracked interface on the primary: its priority drops by the decrement and the standby takes over; after
  restoring it and the preempt delay, the primary becomes Active again.
- [ ] `debug standby terse` omits hello and advertisement packets if you need to watch transitions.

## Checked
Date: 2026-11-08. Read in full: Cisco "Understand the Hot Standby Router Protocol Features and Functionality"
(document 9234, updated September 2023). The second cited page (HSRP configuration guide, 404) was dropped.
Confirmed: HSRP model and message behaviour, MAC format, priority then IP tie-break, preemption and coup/resign, preempt
delay semantics, interface tracking behaviour, default decrement 10 and cumulative decrements, `debug standby terse`,
clear-text authentication.
Removed: `standby version 2`, `timers msec` values, "default timers 3/10", MD5 key-string authentication, the BFD
alternative, `show standby`/`show track` commands, the STP-root design note, `%HA_EM`/`%HSRP-5-STATECHANGE`
messages and the hold-time claim (none on the page).
Method: documentation only; no commands were run.
