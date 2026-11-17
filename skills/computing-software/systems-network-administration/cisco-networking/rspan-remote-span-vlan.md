---
id: computing-software.systems-network-administration.cisco-networking.rspan-remote-span-vlan
name: rspan-remote-span-vlan
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, rspan, remote-span, monitor-session, port-mirroring, span]
level: practitioner
status: docs-checked
description: "Mirror traffic from one Catalyst 9300 to an analyser on another with RSPAN: dedicated remote-span VLAN, source and destination sessions, restrictions and pitfalls."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/nmgmt/b_179_nmgmt_9300_cg/configuring_span_and_rspan.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RSPAN

Scope: Catalyst 9300 IOS XE 17.9 configuration guide (Configuring SPAN and RSPAN).

An RSPAN source session relabels mirrored packets with the RSPAN VLAN ID and sends them over normal trunks. The
destination session strips the tag and presents all RSPAN VLAN packets (except Layer 2 control packets) on the
destination port. Configure the RSPAN VLAN before the source and destination sessions.

## RSPAN VLAN (every participating device)
```
vlan 901
 remote-span
```
- Valid IDs are 2 to 1001 and 1006 to 4094; not VLAN 1 or 1002-1005. Use the same RSPAN VLAN for the session on all
  devices, and do not assign access ports to it (access ports on an RSPAN VLAN go inactive).
- Traffic in the RSPAN VLAN is always flooded and no MAC learning occurs on it.
- If the ID is below 1005 and VTP is enabled, VTP can propagate it; for extended-range IDs configure the VLAN on the
  source, destination and every intermediate device. With VTP pruning, RSPAN traffic is pruned on trunks.
- It is recommended not to make the RSPAN VLAN the native VLAN. It is configured only on trunk ports.

## Source switch
```
monitor session 1 source interface gigabitethernet1/0/10 both
monitor session 1 destination remote vlan 901
```
## Destination switch
```
monitor session 1 source remote vlan 901
monitor session 1 destination interface gigabitethernet1/0/48
```
An RSPAN source session cannot have a local destination port; a destination session cannot have a local source
port; the same RSPAN VLAN cannot be used by a source and a destination session on one device (or stack).

## Pitfalls
- Each monitored packet is sent twice, so a busy source adds load to the trunks carrying the RSPAN VLAN.
- RSPAN does not monitor BPDUs or other Layer 2 protocols, and does not capture DHCP-inject packets.
- RSPAN traffic is forwarded over trunk ports carrying the RSPAN VLAN.
- Limits are shared with local SPAN: 66 sessions per device, at most 8 source sessions.
- `no monitor session N` (or `remote`) removes the session; entering commands does not clear earlier parameters.
- Filtering: `monitor session N filter vlan ...` on an RSPAN source limits trunk VLANs; an output ACL can be applied
  to the RSPAN VLAN on the source device.

## Check
`show monitor` displays the current SPAN, RSPAN, FSPAN or FRSPAN configuration.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read the Catalyst 9300 17.9 "Configuring SPAN and RSPAN" chapter:
Restrictions (SPAN and RSPAN), RSPAN Configuration Guidelines, Configuring a VLAN as an RSPAN VLAN (including "What to
do next"), the RSPAN source and destination session steps (command forms) and the monitoring table. Added from the
guide: valid VLAN ID range and reserved IDs, session limits (66, at most 8 source), the source/destination session
restrictions. Removed as unconfirmed: `show vlan remote-span` and `show interfaces trunk | include` checks, "mirror one
direction or filter" advice, the "cannot cross routed links (use ERSPAN)" line and the "prune it from trunks" advice
(VTP pruning is described only as automatic when enabled).
