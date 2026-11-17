---
id: computing-software.networking-hardware-and-wireless.arista-eos.ospf
name: ospf
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, ospf, ospfv2, ospf-area, router-ospf]
level: practitioner
status: draft
description: "Configure EOS OSPF with router-id, areas, point-to-point links and passive interfaces, and verify neighbors."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OSPF
Goal: run OSPF for a small underlay.

```
router ospf 1
   router-id 10.255.0.1
   passive-interface default
   no passive-interface Ethernet1
   max-lsa 12000
interface Ethernet1
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
   ip ospf authentication message-digest
   ip ospf message-digest-key 1 sha256 7 <encrypted-placeholder>
interface Loopback0
   ip address 10.255.0.1/32
   ip ospf area 0.0.0.0
```

```
show ip ospf neighbor
show ip ospf interface brief
show ip ospf database
```

- Enable per interface (`ip ospf area`) or via `network` statements under `router ospf`.
- Point-to-point avoids DR election on links between routers.
- `redistribute connected route-map X` as needed.

Gotcha: stuck in `EXSTART` points to MTU mismatch; the EOS interface MTU and routed MTU on both sides must match. Check `show interfaces ... | include MTU`.

Operational tip: use a reference bandwidth appropriate for 100G links (`auto-cost reference-bandwidth 100000`) on all routers, or costs collapse and all fast links look equal.

## Verify
- `show ip ospf neighbor` shows `FULL`; `show ip route ospf` lists the learned prefixes.
