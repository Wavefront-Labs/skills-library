---
id: computing-software.systems-network-administration.cisco-networking.layer-2-traceroute
name: layer-2-traceroute
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, l2-traceroute, traceroute-mac, cdp, mac-address-table, switching, troubleshooting]
level: practitioner
status: docs-checked
description: "Trace the Layer 2 path between two hosts across Catalyst switches with traceroute mac and traceroute mac ip, including the CDP and single-VLAN prerequisites."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/command_reference/b_179_9300_cr/system_management_commands.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layer 2 traceroute

IP traceroute stops at the default gateway; inside a VLAN you need the switch-by-switch path.
Catalyst switches can trace it with the `traceroute mac` commands (Catalyst 9300, IOS XE 17.9;
introduced 16.5.1a).

## Commands
```
traceroute mac [interface <id>] <src-mac> [interface <id>] <dst-mac> [vlan <1-4094>] [detail]
traceroute mac ip {<src-ip> | <src-host>} {<dst-ip> | <dst-host>} [detail]
```
Examples:
```
traceroute mac 0000.0201.0601 0000.0201.0201
traceroute mac 0000.0201.0601 0000.0201.0201 detail
traceroute mac ip 2.2.66.66 2.2.22.22 detail
```
Sample output from the guide:
```
Source 0000.0201.0601 found on con6[WS-C3750E-24PD] (2.2.6.6)
con6 (2.2.6.6) :Gi0/0/1 => Gi0/0/3
con5 (2.2.5.5) : Gi0/0/3 => Gi0/0/1
con1 (2.2.1.1) : Gi0/0/1 => Gi0/0/2
con2 (2.2.2.2) : Gi0/0/2 => Gi0/0/1
Destination 0000.0201.0201 found on con2[WS-C3550-24] (2.2.2.2)
Layer 2 trace completed
```

## Prerequisites and limits (from the command reference)
- CDP must be enabled on all devices in the network; do not disable it.
- The path is shown only when source and destination MACs are in the same VLAN. If the MAC is in
  multiple VLANs, give the `vlan` keyword or the path is not identified.
- Unicast only: a multicast source or destination MAC gives an error.
- Maximum of ten hops identified in the path.
- A device in the path that does not support Layer 2 traceroute: the switch keeps sending trace
  queries and lets them time out.
- Not supported where several devices hang off one port through hubs (more than one CDP neighbour
  on a port); the path is not identified and an error appears. Not supported in Token Ring VLANs.
- `traceroute mac ip`: the IPs must be in the same subnet. The switch uses ARP to get the MAC and
  VLAN; with no ARP entry it sends an ARP query, and if that fails the path is not identified.
- Layer 2 traceroute is enabled by default and listens on UDP port 2228.

## Error output in the guide
| Output | Cause |
|---|---|
| `Error:Source Mac address not found.` | switch cannot find the source MAC |
| `Error:Source and destination macs are on different vlans.` | different VLANs |
| `Error:Mac found on multiple vlans.` | MAC in several VLANs, no `vlan` given |
| `Invalid destination mac address` | multicast destination |
| `Arp failed for destination <ip>.` | ARP could not resolve (`mac ip` form) |
Failed traces end `Layer2 trace terminated.` (wording was "aborted" before 17.5.1).

## Manual equivalent
```
show mac address-table address 0050.56aa.0002
show cdp neighbors Te1/1/1 detail
! log in to that neighbour, repeat until the port is an access port
```

## Verify
- [ ] Trace shows the expected uplinks; compare with the STP forwarding path
  (`show spanning-tree vlan 20`).

## Checked
2026-11-08. Confirmed against the Catalyst 9300 17.9 System Management Command Reference
(`traceroute mac`, `traceroute mac ip`): syntax, CDP requirement, VLAN, unicast and subnet limits,
ten-hop maximum, hub/multiple-CDP-neighbour limit, example outputs, UDP port 2228 default and the
17.5.1 "terminated" wording change. Removed unsupported claims: the "ping first" and SVI
prerequisites, the IP-reachability-between-switches prerequisite, the invented
"Unknown/multiple neighbors" and "Device has multiple CDP neighbours" messages, the EtherChannel
row and the CDP-on-edge-ports note. The old configuration guide URL 404s.
Method: documentation only; no commands were run.
