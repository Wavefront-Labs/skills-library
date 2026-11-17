---
id: computing-software.systems-network-administration.cisco-networking.stp-timers-and-diameter
name: stp-timers-and-diameter
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, spanning-tree, stp-timers, stp-diameter, hello-time, forward-delay, max-age, rstp]
level: practitioner
status: docs-checked
description: "STP hello, forward-delay and max-age defaults and ranges, the IEEE formulas for tuning them by diameter, the root-primary diameter macro, and why only the root's timers matter."
sources:
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/19120-122.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9300_cg/configuring_spanning_tree_protocol.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STP timers and network diameter

Sources: Cisco "Understand and Tune Spanning Tree Protocol Timers" (document 19120, 802.1D only) and the Catalyst 9300 Layer 2 Configuration Guide, IOS XE 17.9.x, "Configuring Spanning Tree Protocol".

## Defaults and ranges
| Timer | Default | Range (Catalyst 9300 commands) | Meaning |
|---|---|---|---|
| hello | 2 s | 1 to 10 | interval between configuration BPDUs sent by the root |
| forward delay | 15 s | 4 to 30 | time spent in listening and learning |
| max age | 20 s | 6 to 40 | time a port waits without BPDUs before reconfiguration |

The IEEE recommends a maximum diameter of seven bridges for the default timers. Document 19120 derives them: max age = 14 (end-to-end BPDU propagation) + 6 (message age overestimate) = 20 s; forward delay = 28.5 / 2, rounded to 15 s.

## Only the root's timers count
Each BPDU carries hello, forward delay and max age, and a bridge uses the values in the BPDUs it receives, not its local configuration. Configure any change on the root bridge and on the backup root; if the root is lost, the new root imposes its own timers.

## Tune with the formulas
Document 19120's formulas, with the IEEE parameters left fixed:
```
max_age       = (4 x hello) + (2 x dia) - 2
forward_delay = ((4 x hello) + (3 x dia)) / 2
```
Its example for a diameter of 4: hello 2 gives max age 14 s and forward delay 10 s; hello 1 gives max age 10 s and forward delay 8 s. Lowering hello from 2 s to 1 s doubles the BPDUs each bridge sends and receives, which adds CPU load, notably with several VLANs and trunks. The document's caution: if you are unfamiliar with STP, changes can cause instability, CPU spikes and outages.

Diameter here is the maximum number of switches crossed between any two switches, source and destination included, never crossing a switch twice.

## Catalyst commands (9300 guide)
```
spanning-tree vlan 20-24 root primary diameter 4
spanning-tree vlan 20-24 root secondary diameter 4
spanning-tree vlan 20-24 hello-time 3
spanning-tree vlan 20,25 forward-time 18
spanning-tree vlan 20 max-age 30
```
- `root primary [diameter net-diameter]`: diameter range 2 to 7; the device sets hello, forward-delay and max-age for that diameter automatically. The guide says the switch sets its priority to 24576 if that makes it root. After using the macro the guide recommends not setting hello-time, forward-time and max-age by hand.
- `root secondary` sets priority 28672; use the same diameter as on the primary root.
- Verify with `show spanning-tree vlan <vlan-id>`.
- Document 19120 notes that the configured diameter is not displayed in the configuration or any show output.

## RSTP and MST
Document 19120 covers 802.1D only. The 9300 guide says MSTP runs on RSTP, which eliminates the forward delay and moves root and designated ports to forwarding quickly. On a point-to-point link, `spanning-tree link-type point-to-point` lets the local designated port negotiate with the remote port and change rapidly to forwarding. Rapid PVST+ is the default STP mode on the 9300.

## Checked
Date: 2026-11-08. Read end to end: Cisco document 19120 "Understand and Tune Spanning Tree Protocol Timers" (updated Feb 2023); Catalyst 9300 Layer 2 Configuration Guide 17.9.x "Configuring Spanning Tree Protocol", read by sections (bridge ID, modes, root device and secondary root, hello, forward-time, max-age, link-type, monitoring table); the rest of that long page was searched for diameter, hello-time, forward-time, max-age, link-type and show spanning-tree rather than read in full. Fetched via tools/review/fetch_pages.py.
Corrected or removed: hello range (guide says 1 to 10), the 50 s legacy convergence figure, the `hello-time 2` argument on the root macro (not in the guide's syntax), the 2 x (forward-delay - 1) >= max-age relation, the `| include` verify command, the P2p/Shr output and "sub-second" convergence claims, the BPDU CPU claims about hundreds of VLANs and MST preference, "diameter greater than 7 is a design smell", and the mixed-vendor VLAN 1 remark.
Method: documentation only; no commands were run.
