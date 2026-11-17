---
id: computing-software.systems-network-administration.cisco-networking.layer-3-etherchannel
name: layer-3-etherchannel
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, etherchannel, port-channel, lacp, layer-3-etherchannel, routed-port-channel, no-switchport, channel-group, routed-port]
level: practitioner
status: docs-checked
description: "Build a Layer 3 EtherChannel on Catalyst 9300 (IOS XE 17.9): no switchport then channel-group, the IP address on the Port-channel, min-links, and RU summary flags."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9300_cg/configuring_etherchannels.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layer 3 EtherChannel

Based on the Catalyst 9300 Layer 2 Configuration Guide, IOS XE 17.9.x, "Configuring EtherChannels".

## Configure
The guide's procedure and example for ports on a Layer 3 EtherChannel (members as routed ports, LACP active):
```
interface range gigabitethernet2/0/1 -2
 no ip address
 no switchport
 channel-group 5 mode active
```
- `no switchport` puts the port in Layer 3 mode; the guide lists it before `channel-group`.
- `channel-group` dynamically creates the port-channel interface. Alternatively create it first with `interface port-channel <n>` followed by `no switchport`, then assign members with `channel-group`.
- Assign the Layer 3 address to the port-channel logical interface, not to the physical ports.
- Port-channel numbers run 1 to 128.
- For a PAgP EtherChannel, up to eight ports of the same type and speed per group; for LACP, up to 16 Ethernet ports of the same type, up to eight active and up to eight in standby.
- `port-channel min-links <2-8>` on the port-channel interface sets how many member ports must be up and bundled for the port channel to come up.
- For a Layer 3 cross-stack channel (members on different stack switches), the `auto` and `desirable` PAgP keywords are not supported; the guide's cross-stack example uses LACP active.

## Restrictions to know
- You cannot use Layer 2 configurations on a Layer 3 port.
- Auto-LAG is not supported on Layer 3 interfaces or Layer 3 EtherChannels.
- Multicast on an EtherChannel: member port selection is software based for Layer 2 and Layer 3 multicast routes, so all traffic of one group uses the same physical member; multicast load may not spread evenly.
- A port shut down with `shutdown` is treated as a link failure and traffic moves to the remaining members.
- Configure all ports in the channel with the same speed and duplex.

## Verify
```
show etherchannel summary
show lacp neighbor
```
- `Po5(RU)`: `R` is Layer 3, `U` in use; members show `(P)` when bundled.
- Pull one member in a window and confirm the bundle stays up; test `min-links` if configured.

## Checked
Date: 2026-11-08. Read end to end: Catalyst 9300 Layer 2 Configuration Guide 17.9.x "Configuring EtherChannels" (fetched via tools/review/fetch_pages.py): Channel Groups and Port-Channel Interfaces, Layer 3 EtherChannel Configuration Guidelines, "Configuring Layer 3 EtherChannels" steps, min-links, Auto-LAG guidelines, Restrictions, Layer 3 examples, and the flag legend in the Auto-LAG sample output.
Removed because the page does not confirm them: sub-second failover and "no routing reconvergence", OSPF point-to-point and /31 addressing, the claim that a Layer 2-first Port-channel fails with mismatch errors and the rebuild recipe, the L3 Port-channel vs ECMP comparison table (CEF hash, BFD, bandwidth metrics), MTU matching, the `mode on` blackhole claim, and the SVI-over-Layer 2 Port-channel remark.
Method: documentation only; no commands were run.
