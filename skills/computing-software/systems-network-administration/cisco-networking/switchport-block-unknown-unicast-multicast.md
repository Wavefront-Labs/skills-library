---
id: computing-software.systems-network-administration.cisco-networking.switchport-block-unknown-unicast-multicast
name: switchport-block-unknown-unicast-multicast
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, switchport-block, unknown-unicast-flooding, unknown-multicast, storm-control, flooding-control]
level: practitioner
status: docs-checked
description: "Use switchport block unicast and multicast on a Catalyst 9300 to stop unknown-destination flooding out a port, and how it differs from storm control."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_port_based_traffic_control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blocking unknown unicast and multicast flooding per port

Scope: Catalyst 9300 IOS XE 17.9 (Port-Based Traffic Control chapter).

## What it does
By default the device floods packets with an unknown destination MAC address out of all ports. Port blocking stops
unknown unicast or multicast being forwarded out a given port, whether it is protected or not.
```
interface gigabitethernet1/0/1
 switchport block multicast
 switchport block unicast
```
- `switchport block multicast`: blocks unknown multicast forwarding out of the port. Only pure Layer 2 multicast
  is blocked; multicast packets that carry IPv4 or IPv6 information in the header are not.
- `switchport block unicast`: blocks unknown unicast forwarding out of the port.
- Works on a physical interface or an EtherChannel; on a port-channel it blocks on every member.
- `show interfaces [interface-id] switchport` displays port blocking and port protection settings.

## Use with protected ports
The guide's reason for the feature: unknown unicast or multicast forwarded to a protected port can be a security
issue, so combine port blocking with `switchport protected` (see the protected-ports skill).

## Related: storm control
Storm control is a separate feature: per-port thresholds (percentage, bps or pps) for broadcast, multicast or unicast,
disabled by default, set with `storm-control {broadcast | multicast | unicast} level ...` and an optional
`storm-control action {shutdown | trap}`; check it with `show storm-control [interface-id]`. Port blocking does not
rate-limit anything.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read the Catalyst 9300 17.9 Port-Based Traffic Control chapter:
Port Blocking, Blocking Flooded Traffic on an Interface, Monitoring Port Blocking and the storm-control configuration
steps (read directly). Removed as unconfirmed: the `| include Unknown` filter and "Unknown unicast blocked: enabled"
output line, the static-MAC, silent-host and uplink advice, IPv6 multicast advice, and the
ARP timeout 4 h / MAC aging 5 min figures. The command-reference page cited earlier was not needed and was dropped
from sources.
