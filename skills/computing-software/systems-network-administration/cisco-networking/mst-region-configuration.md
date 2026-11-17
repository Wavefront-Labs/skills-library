---
id: computing-software.systems-network-administration.cisco-networking.mst-region-configuration
name: mst-region-configuration
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, spanning-tree, stp, mst, multiple-spanning-tree, 802-1s, mst-region, mst-instance, ist, cist, revision-number, pvst-simulation, mst-boundary]
level: advanced
status: docs-checked
description: "Deploy MST (802.1s) on Catalyst: region name, revision and VLAN map that must match, IST and instance roots, boundary ports, PVST+ interaction and migration advice."
sources:
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/24248-147.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9300_cg/configuring_multiple_spanning_tree_protocol.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MST region configuration

Based on Cisco document 24248 (Understand the Multiple Spanning Tree Protocol, 802.1s) and the Catalyst 9300 Layer 2 Configuration Guide, IOS XE 17.9.x, "Configuring Multiple Spanning-Tree Protocol".

MSTP uses RSTP for rapid convergence and lets many VLANs share a small number of spanning-tree instances. Both pages say that a failure in one instance does not affect the others, and that MST gives load balancing over redundant paths.

## Region definition (identical on every switch in the region)
```
spanning-tree mst configuration
 instance 1 vlan 10-20
 name region1
 revision 1
 show pending
 exit
spanning-tree mode mst
```
- Two switches are in the same region only if they have the same VLAN-to-instance map, the same revision number and the same name.
- `instance <id> vlan <range>`: instance range 0 to 4094, VLAN range 1 to 4094. The mapping is incremental: VLANs in the command are added to, or removed from, those already mapped. A VLAN belongs to one instance at a time. VLANs not mapped go to the IST (instance 0).
- `name`: up to 32 characters, case sensitive. `revision`: 0 to 65535.
- `exit` applies the changes; `show pending` displays the pending configuration first.
- `spanning-tree mode mst` also enables RSTP. Changing mode stops all instances of the old mode and restarts them, which can disrupt traffic. You cannot run MST together with PVST+ or Rapid PVST+.
- If maps differ the ports act as boundaries: the guide says that for load balancing to work all VLAN-to-instance assignments must match, otherwise all traffic flows on a single link.
- VTP does not propagate the MST configuration; configure each switch by CLI or SNMP.
- Document 24248 says the BPDU carries only the name, revision and a digest of the VLAN-to-instance table; a received digest that differs from the local one makes that port a boundary of the region.

## Instance roots and priority (9300 guide)
```
spanning-tree mst 0 root primary
spanning-tree mst 1 root secondary
spanning-tree mst 0 priority 40960
```
- `root primary` sets priority 24576 if that makes the switch root, otherwise 4096 below the lowest root priority; `root secondary` sets 28672. Instance IDs may be a single value, a range or a list. The `diameter` keyword is available only for instance 0.
- `spanning-tree mst <instance-id> priority <value>`: 0 to 61440 in steps of 4096, default 32768. The guide recommends root primary/secondary for normal use and priority only when those do not work.
- Root switches should be backbone or distribution switches, not access switches.
- Hello, forward-delay, max-age and max-hops are set on the CST (instance 0) but apply to all instances: `spanning-tree mst max-hops <hop-count>`; default max hops 20, max-age 20 s.
- Port priority: `spanning-tree mst <instance-id> port-priority <0-240, steps of 16>`, default 128. In a switch stack use `spanning-tree mst [instance-id] cost <cost>` instead.
- MST uses the long (32-bit) path-cost method: 10 Mb/s 2,000,000; 100 Mb/s 200,000; 1 Gb/s 20,000; 10 Gb/s 2,000; 100 Gb/s 200.

## IST, CIST and the boundary
- Instance 0 is the IST; all other instances are 1 to 4094 on the 9300. Only the IST sends and receives BPDUs; other instances travel as M-records inside MST BPDUs.
- Instances are local to a region: MST instance 1 in region A is independent of instance 1 in region B.
- The IST is active on every port inside the region, whether it carries VLANs mapped to it or not. Document 24248's example: VLAN 10 on the IST and VLAN 20 on instance 1 over access ports blocked VLAN 10 on a link with no apparent loop. Its preferred fix is to avoid mapping VLANs to instance 0; the alternative is to carry the IST VLANs on all links.
- Two VLANs mapped to one instance share one topology. Never prune an individual VLAN off a trunk without removing all VLANs mapped to the same instance (document 24248).
- At the region boundary only IST BPDUs go out; MSTIs follow the IST topology on boundary ports, so a boundary port blocks or forwards for all VLANs.

## Interaction with PVST+ (document 24248)
- The MST region replicates the IST BPDU on all VLANs at the boundary to simulate a PVST+ neighbour.
- Recommended: the IST root is the root for all PVST+ instances (root inside the region, with a higher priority than any other bridge).
- Rules: if the MST bridge is root it must be root for all VLANs; if the PVST+ bridge is root it must be root for all VLANs, including the CST on VLAN 1. If the MST bridge is root for the CST while the PVST+ bridge is root for one or more other VLANs, the simulation fails and the boundary port goes to root inconsistent. Investigate whether a PVST+ bridge tried to become root for some VLANs.
- 9300 guide prerequisite: for load balancing between PVST+/Rapid PVST+ and an MST cloud, all MST boundary ports must be forwarding, which they are when the IST root is the CST root.
- Not recommended: a root outside the region leaves one boundary uplink blocking for all VLANs, with no load balancing between the region's uplinks.

## Migration advice (document 24248)
- Identify point-to-point and edge (PortFast) ports; make switch-to-switch links full duplex.
- Decide how many instances you need (each is a logical topology), which VLANs map to them, and a root and backup root for each.
- Choose one name and revision for all switches; put as many switches as possible in one region.
- Avoid mapping VLANs onto instance 0. Migrate the core first, then work down to access switches. Keep the CST and IST root inside the region.

## Limits and legacy
- 9300 guide: up to 65 MST instances per region (switch stack); document 24248 states 16 (IST plus 15 MSTIs) for the platforms of its era.
- To renegotiate with neighbours after a legacy 802.1D switch is removed, use `clear spanning-tree detected-protocols`. Only the 9300 guide mentions this.
- Check one interface with `show spanning-tree mst interface <interface-id>` (shown only for link-up ports).

## Checked
Date: 2026-11-08. Read end to end: Cisco document 24248 (rev 3.0, Aug 2024). Catalyst 9300 Layer 2 Configuration Guide 17.9.x "Configuring Multiple Spanning-Tree Protocol": prerequisites, restrictions, root, regions, IST/CIST, boundary ports, RSTP overview, configure sections for region, root, secondary, port priority, priority and max-hops (read to line about 540 of the fetched text; the remaining link-type and neighbour-type sections were not used). Fetched with tools/review/fetch_pages.py.
Removed because neither page confirms them: `show spanning-tree mst configuration [digest]`, `show spanning-tree mst 1`, the `PVST_Inc` state name (24248 says root inconsistent), "adding a VLAN later changes the digest" planning advice, the 'max 16 instances' as a current platform fact (now scoped), the example priority numbers and region name, and the "make the MST root the same switch as the current PVST+ root" step (kept only as the guide's root-inside-region advice).
Method: documentation only; no commands were run.
