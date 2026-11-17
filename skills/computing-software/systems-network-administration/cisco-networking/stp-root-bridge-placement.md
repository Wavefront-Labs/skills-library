---
id: computing-software.systems-network-administration.cisco-networking.stp-root-bridge-placement
name: stp-root-bridge-placement
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, spanning-tree, stp, rapid-pvst, root-bridge, stp-priority, bridge-id, spanning-tree-vlan-root-primary, extended-system-id]
level: practitioner
status: docs-checked
description: "Place the STP root deliberately on Catalyst 9300: bridge ID with extended system ID, per-VLAN priority values, root primary/secondary macros and root guard."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9300_cg/configuring_spanning_tree_protocol.html
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/10588-74.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STP root bridge placement

Based on the Catalyst 9300 Layer 2 Configuration Guide, IOS XE 17.9.x, "Configuring Spanning Tree Protocol", and Cisco document 10588 (root guard).

With all switches at the default priority (32768), the switch with the lowest MAC address in the VLAN becomes the root. The guide notes that this switch may not be the ideal root because of traffic patterns, number of forwarding interfaces or link types; raise the priority (lower the number) of the ideal switch to force a recalculation.

## Bridge ID
With PVST+ and Rapid PVST+ each VLAN has its own 8-byte bridge ID. The two most significant bytes are reallocated into a 4-bit priority and a 12-bit extended system ID equal to the VLAN ID; the other 6 bytes come from the MAC address. The bridge priority is therefore set in steps of 4096.

## Configure
```
spanning-tree mode rapid-pvst
spanning-tree vlan 10,30,50 priority 4096
spanning-tree vlan 20,40,60 priority 8192
```
- `spanning-tree vlan <vlan-id> priority <priority>`: range 0 to 61440 in increments of 4096, default 32768. The guide's valid values are 4096, 8192, 12288, 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344 and 61440; all other values are rejected. Lower is more likely to be root. The guide lists a VLAN list or range as valid.
- `spanning-tree vlan <vlan-id> root primary [diameter <2-7>]` changes the priority from 32768 to a significantly lower value; because of the extended system ID the switch sets 24576 if that makes it root. After the macro the guide recommends not setting hello-time, forward-time and max-age by hand.
- `spanning-tree vlan <vlan-id> root secondary [diameter <2-7>]` sets priority 28672. Run it on more than one switch for multiple backup roots, with the same diameter and hello values as the primary.

## Check
```
show spanning-tree vlan 10
show spanning-tree summary
show spanning-tree active
```
These are in the guide's monitoring table.

## Keeping the placement
- Cisco document 10588: with standard STP any bridge with a lower bridge ID becomes root, and priority 0 gives no guarantee against another priority-0 bridge with a lower MAC address. Root guard (`spanning-tree guard root` on an interface) keeps a port designated and puts it in root-inconsistent state when a superior BPDU arrives; enable it on all ports where the root must not appear.
- In a mixed MSTP and PVST+ network the common spanning-tree root must be inside the MST backbone.
- Platform limits in the guide: PVST+/Rapid PVST+ supports up to 300 spanning-tree instances (from IOS XE 17.2.1), MSTP up to 65.

## Checked
Date: 2026-11-08. Read: Catalyst 9300 Layer 2 Configuration Guide 17.9.x "Configuring Spanning Tree Protocol" (bridge ID and extended system ID, "How a Device or Port Becomes the Root", Configuring the Root Device, Secondary Root, priority, supported instances, interoperability, monitoring table; the long page was read by sections, not end to end) and Cisco document 10588 (read end to end). Fetched with tools/review/fetch_pages.py.
Removed because neither page confirms them: the "VLAN 10 shows 32778" illustration, "4096 below the current root", the claim the macro is a one-time non-dynamic setting, the HSRP/VRRP root-alignment section (and the dead 5234-5 source, which now redirects to an unrelated page), `show spanning-tree root` and `show standby brief`, the 61440 access-switch advice, and the topology-change window remark.
Method: documentation only; no commands were run.
