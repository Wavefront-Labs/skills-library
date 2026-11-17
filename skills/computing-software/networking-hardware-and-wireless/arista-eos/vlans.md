---
id: computing-software.networking-hardware-and-wireless.arista-eos.vlans
name: vlans
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, vlans, vlan-database, trunk-allowed, switchport-trunk]
level: practitioner
status: draft
description: "Create EOS VLANs, access and trunk ports, native VLAN and allowed lists, and SVIs."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VLANs and trunks
Goal: configure layer 2 segmentation.

```
vlan 100
   name USERS
vlan 200
   name SERVERS
interface Ethernet48
   switchport mode trunk
   switchport trunk allowed vlan 100,200
   switchport trunk native vlan 999
interface Vlan100
   ip address 192.0.2.1/24
```

```
show vlan
show interfaces trunk
show mac address-table vlan 100
```

- VLANs must exist (or be created implicitly) before use; SVIs need the VLAN in the database and at least one active port.
- `switchport trunk allowed vlan add 300` appends rather than replacing the list.
- Use `no switchport trunk native vlan` to remove the native VLAN on a trunk.

Gotcha: `switchport trunk allowed vlan 100` replaces the whole list; forgetting `add` removes VLANs on a live trunk. Use configuration sessions with a timer.

Operational tip: keep a single VLAN naming convention and a list of which trunks carry which VLANs; pruning unused VLANs from trunks reduces flooding and limits blast radius of a broadcast problem.

## Verify
- `show interfaces trunk` lists the allowed VLANs; `show mac address-table vlan 100` shows learned MACs.
