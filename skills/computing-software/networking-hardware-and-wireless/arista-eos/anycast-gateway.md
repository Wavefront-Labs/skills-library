---
id: computing-software.networking-hardware-and-wireless.arista-eos.anycast-gateway
name: anycast-gateway
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, virtual-router, ip-virtual-router, varp, anycast]
level: practitioner
status: draft
description: "Configure EOS VARP / virtual router address so every leaf shares a gateway IP and MAC."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Anycast gateway with VARP
Goal: distributed default gateway for hosts.

```
ip virtual-router mac-address 00:1c:73:00:00:99
interface Vlan100
   vrf TENANT-A
   ip address virtual 192.0.2.1/24
```

or per-switch real addresses with a shared virtual:
```
interface Vlan100
   ip address 192.0.2.2/24
   ip virtual-router address 192.0.2.1
```

```
show ip virtual-router
show arp vrf TENANT-A
```

- The virtual MAC is set once globally and is the same on all leaves (it is a locally administered address from the Arista docs example).
- `ip address virtual` uses a single shared address on every leaf (EVPN design) with no per-switch IP.
- Not the same protocol as VRRP; no election.

Gotcha: A mismatched virtual MAC between leaves causes ARP flapping. Hosts must not use the physical SVI IP as gateway.

Operational tip: verify gateway behaviour from a host by checking that its ARP table shows the virtual MAC and that traffic still flows after you take one leaf down.

## Verify
- `show ip virtual-router` lists the virtual IP and `show arp` entries use the virtual MAC.
