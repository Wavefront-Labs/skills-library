---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.vlans-and-tagging
name: vlans-and-tagging
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, vlans, vlan-tagging, 802-1q]
level: practitioner
status: draft
description: "Create tagged and untagged BIG-IP VLANs on interfaces or trunks with tmsh, and verify membership and tag behaviour."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-system-initial-configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VLANs and 802.1Q tagging on BIG-IP

Create a VLAN and bind it to a physical interface or trunk:
```
tmsh create net vlan external interfaces add { 1.1 { tagged } } tag 4093
tmsh create net vlan internal interfaces add { 1.2 { untagged } }
tmsh list net vlan external all-properties
tmsh show net vlan external
```
- An interface can be untagged in only one VLAN, but tagged in many. Untagged members carry no 802.1Q header; the VLAN `tag` is then only a label (auto-assigned).
- A VLAN needs at least one self IP before it passes routed or load-balanced traffic. The VLAN alone only gives layer 2 membership.
- `tmsh modify net vlan X mtu 1500` and `failsafe enable` are VLAN-level; failsafe fails over the unit when no traffic is seen on the VLAN within the timeout (confirm on your version).
- Prefer tagging on a trunk toward the switch, and keep tag IDs identical on both HA peers: sync does not fix a mismatched VLAN tag on the switch side.
- Gotcha: after an interface is moved between VLANs, ARP entries and the MAC masquerade of floating self IPs can linger; run `tmsh delete net arp all` in a window if stale.

Verify: `tmsh show net interface` shows the interface up with traffic counters, `tmsh show net arp` shows neighbours on the VLAN, and `tcpdump -nni external:nnn` (the `:nnn` suffix prints the VLAN name) shows frames arriving. An empty ARP table with the cable up usually means the switch port tag or allowed-VLAN list is wrong.
