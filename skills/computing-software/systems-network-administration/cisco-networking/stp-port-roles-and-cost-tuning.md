---
id: computing-software.systems-network-administration.cisco-networking.stp-port-roles-and-cost-tuning
name: stp-port-roles-and-cost-tuning
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, spanning-tree, stp, rapid-pvst, rstp, stp-port-roles, stp-port-cost, root-port, designated-port, alternate-port, backup-port, port-priority, link-type]
level: practitioner
status: docs-checked
description: "RSTP port roles and states, and how Catalyst 9300 spanning-tree cost and port-priority steer which interface forwards, plus RSTP link types and edge ports."
sources:
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/24062-146.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9300_cg/configuring_spanning_tree_protocol.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STP port roles and cost tuning

Sources: Cisco document 24062 (Understand Rapid Spanning Tree Protocol, 802.1w) and the Catalyst 9300 Layer 2 Configuration Guide, IOS XE 17.9.x, "Configuring Spanning Tree Protocol".

## Roles and states (RSTP)
| Role | What it is |
|---|---|
| Root | the port that receives the best BPDU on a bridge, closest to the root in path cost; the root bridge is the only bridge with none |
| Designated | the port that can send the best BPDU on its segment |
| Alternate | blocked port that receives more useful BPDUs from another bridge; it can replace the root port if that fails |
| Backup | blocked port that receives more useful BPDUs from the same bridge; redundant connectivity to the same segment, no alternative path to the root |

RSTP has three states. 802.1D disabled, blocking and listening merge into discarding; learning and forwarding remain. Role and state are decoupled, so a port can be designated and still discarding for a moment.

## What decides between ports (9300 guide)
- If a loop occurs, spanning tree uses port priority to choose the interface to forward. If priorities are equal, the interface with the lowest interface number forwards and the others are blocked.
- Likewise for path cost: lower cost is chosen first; equal cost falls back to the lowest interface number. The default cost is derived from the interface's media speed.
- In a switch stack, assign lower cost values to the interfaces you want chosen rather than adjusting port priority.
- The long path cost method is the default on the 9300.
- Prefer moving the root first: the guide's root-port example is changing port priority so a Gigabit link, not a 10/100 link, is the root port.

## Steering (interface configuration)
```
interface GigabitEthernet1/0/1
 spanning-tree cost 250
 spanning-tree vlan 10,12-15,20 cost 300
 spanning-tree port-priority 0
 spanning-tree vlan 20-25 port-priority 0
```
- Cost range 1 to 200000000.
- Port priority range 0 to 240 in increments of 16, default 128; lower is higher priority; other values are rejected.
- Both commands exist per interface and per VLAN (the `vlan` forms).

## RSTP link type and edge ports
- Rapid transition to forwarding happens only on edge ports and point-to-point links. Link type is derived from duplex: full duplex is point-to-point, half duplex is shared. Override with `spanning-tree link-type point-to-point` on the interface.
- The proposal/agreement handshake needs point-to-point links. If a designated discarding port gets no agreement after proposing (remote bridge not RSTP, or remote port blocking), it falls back to the 802.1D listening and learning sequence.
- Edge port corresponds to PortFast; an edge port that receives a BPDU loses edge status.

## Read it
```
show spanning-tree vlan <vlan-id>
show spanning-tree interface <interface-id>
show spanning-tree detail
show spanning-tree active
```
`show spanning-tree interface` shows only ports in a link-up operative state; otherwise use `show running-config`.

## Checked
Date: 2026-11-08. Read end to end: Cisco document 24062 (RSTP, rev 2.0 Feb 2023). Catalyst 9300 Layer 2 Configuration Guide 17.9.x "Configuring Spanning Tree Protocol": port priority and cost sections, link-type step, "Port Priority Versus Path Cost", modes and monitoring table, read by sections and by search for port-priority, cost and pathcost rather than end to end. Fetched with tools/review/fetch_pages.py.
Removed because neither page confirms them: the root-port tie-breaker list (neighbour's bridge ID, priority, port number) and the claim that local port-priority only affects the neighbour, the short/long cost table and its numbers, `spanning-tree pathcost method long`, the Disabled role row, the `P2p/Edge/Shr` column description, `show spanning-tree vlan 10 blockedports`, and the "pathcost method long on all switches" verify item.
Method: documentation only; no commands were run.
