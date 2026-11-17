---
id: computing-software.networking-hardware-and-wireless.juniper-junos.ipv6-routing
name: ipv6-routing
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, ipv6, inet6, ospfv3, ndp]
level: practitioner
status: draft
description: "Configure Junos IPv6 addressing, static routes, OSPFv3, BGP inet6 and router advertisements."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IPv6 on Junos
Goal: dual-stack with IPv6 routing.

```
set interfaces xe-0/0/3 unit 0 family inet6 address 2001:db8:100::1/64
set routing-options rib inet6.0 static route ::/0 next-hop 2001:db8:100::2
set protocols ospf3 area 0.0.0.0 interface xe-0/0/3.0
set protocols router-advertisement interface xe-0/0/3.0 prefix 2001:db8:100::/64
set protocols bgp group V6PEERS family inet6 unicast
set protocols bgp group V6PEERS neighbor 2001:db8:100::2 peer-as 65002
```

```
user@host> show ipv6 neighbors
user@host> show route table inet6.0
user@host> ping inet6 2001:db8:100::2
```

- IPv6 routes live in `inet6.0`; OSPFv3 is `ospf3`; IS-IS carries IPv6 in the same process via `isis` with `topology`/multi-topology (confirm).
- Use documentation prefixes `2001:db8::/32` for labs.

Gotcha: forgetting `family inet6` on the interface or an `inet6` BGP family on the group leaves sessions up with no IPv6 NLRI. For IPv6 on lo0 filter, apply an `inet6` filter too.

Operational tip: allocate addresses with a documented plan (a /48 per site, /64 per VLAN, /127 for point-to-point links) and apply equivalent filters for IPv6 and IPv4.

## Verify
- `show route table inet6.0 protocol ospf3` is populated and `ping inet6` succeeds.
