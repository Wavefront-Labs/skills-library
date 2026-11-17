---
id: computing-software.systems-network-administration.cisco-networking.port-channel-config-inheritance
name: port-channel-config-inheritance
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, etherchannel, port-channel-inheritance, port-channel, member-consistency, suspended-port, lacp]
level: practitioner
status: docs-checked
description: "How Catalyst 9300 EtherChannel members take their settings from the first port and the port-channel, which settings must match, and why mismatched members are suspended."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9300_cg/configuring_etherchannels.html
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/etherchannel/12023-4.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Port-channel configuration and member consistency

Based on the Catalyst 9300 Layer 2 Configuration Guide, IOS XE 17.9.x, "Configuring EtherChannels".

## How settings reach members
- An EtherChannel is a channel group plus a port-channel interface. Configuration changes applied to the port-channel interface apply to all physical ports bound to it; changes applied to a physical port affect only that port.
- For Layer 2 ports, `channel-group` dynamically creates the port-channel interface. You can instead create it first with `interface port-channel <n>` and then bind ports with `channel-group`.
- When a group is first created, all ports follow the parameters set for the first port added. If you later change any of these, change them on all ports in the group:
  - allowed-VLAN list
  - spanning-tree path cost for each VLAN
  - spanning-tree port priority for each VLAN
  - spanning-tree PortFast setting

## Must be consistent
- All ports at the same speed and duplex.
- Layer 2: same VLAN for all ports, or all trunks. Ports with different native VLANs cannot form a channel.
- Trunks: the same allowed VLAN range on all ports, otherwise the ports do not form an EtherChannel even in PAgP auto or desirable mode.
- Spanning-tree path cost alone does not make ports incompatible.
- Not both PAgP and LACP in one group; not more than one channel group per port.
- You cannot use Layer 2 configuration on a Layer 3 port.

## When something does not match
- The guide says that on misconfiguration of a port mode or VLAN mask, ports are suspended, and that incompatible `on`-mode ports are suspended.
- Use `show etherchannel summary`: `s` suspended, `I` stand-alone, `P` bundled.
- Compare `show running-config interface <member>` for each member and the far end.

## Verify
- `show etherchannel summary` shows every member `(P)`.
- Member interface configuration matches except for things like description.

## Checked
Date: 2026-11-08. Read end to end: Catalyst 9300 Layer 2 Configuration Guide 17.9.x "Configuring EtherChannels" (fetched via tools/review/fetch_pages.py): Channel Groups and Port-Channel Interfaces, Restrictions, EtherChannel Configuration Guidelines (first-port parameters list), Layer 2 guidelines, "How to Configure EtherChannels" intro, summary flag legend. Cisco document 12023 was read; its PAgP section (same VLAN or trunk, same speed and duplex) agrees.
Removed because unconfirmed: the `%EC-5-CANNOT_BUNDLE2` syslog text, the claim that member changes after bundling are rejected, the default-interface/shutdown "safe workflow", MTU and flow-control as match conditions, the "inherits from Po10" fix, and the Nexus `show port-channel compatibility-parameters` remark.
Method: documentation only; no commands were run.
