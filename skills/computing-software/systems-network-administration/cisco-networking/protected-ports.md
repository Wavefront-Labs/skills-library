---
id: computing-software.systems-network-administration.cisco-networking.protected-ports
name: protected-ports
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, protected-port, switchport-protected, pvlan-edge, host-isolation, private-vlan]
level: practitioner
status: docs-checked
description: "Isolate hosts on the same Catalyst 9300 with switchport protected: what it blocks, stack and EtherChannel behaviour, port blocking, and when private VLANs fit better."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_port_based_traffic_control.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/vlan/b_179_vlan_9300_cg/configuring_private_vlans.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protected ports

Scope: Catalyst 9300 IOS XE 17.9 (Port-Based Traffic Control chapter).

## Behaviour
- A protected port does not forward unicast, multicast or broadcast to any other protected port. Only control
  traffic such as PIM packets (processed by the CPU) passes between them. Data between protected ports must go
  through a Layer 3 device.
- Forwarding between a protected port and a non-protected port is normal.
- A stack counts as one logical device: no Layer 2 forwarding between protected ports anywhere in the stack, on the
  same or different members.
- Applies to a physical interface or an EtherChannel; on a port-channel it applies to all member ports.
- No ports are protected by default.

```
interface gigabitethernet1/0/1
 switchport protected
```
`show interfaces [interface-id] switchport` shows port protection and port blocking settings.

## Port blocking (related)
By default unknown-destination unicast and multicast are flooded out all ports. Unknown multicast and unicast
flooding to a protected port can be a security issue, so a port (protected or not) can be stopped from flooding them
out with `switchport block multicast` and `switchport block unicast`. For multicast it blocks only pure Layer 2
packets; multicast packets with IPv4 or IPv6 information in the header are not blocked. See the
switchport-block-unknown-unicast-multicast skill.

## Alternative: private VLANs
Private VLANs are the other Layer 2 isolation feature in the same release: ports in an isolated VLAN cannot
communicate with each other at Layer 2, and ports in a community VLAN can communicate with each other but not with
other communities (Private VLANs chapter).

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read the Catalyst 9300 17.9 Port-Based Traffic Control chapter:
Protected Ports, Protected Ports Guidelines, Port Blocking, Configuring a Protected Port, Monitoring Protected Ports,
Blocking Flooded Traffic and Monitoring Port Blocking (read directly). Read the isolated and community definitions in
the Private VLANs chapter (found by search, not the whole chapter). Removed as unconfirmed: the "unprotected trunk lets
protected ports on different switches talk" scope claim, "unknown unicast still flooded to protected ports from
unprotected ports", ARP-blocking, `ip local-proxy-arp` / SVI hairpin advice, "not supported on some port types", the
`| include Protected` filter and the ping verify step.
