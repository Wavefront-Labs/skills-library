---
id: computing-software.networking-hardware-and-wireless.arista-eos.bgp-unnumbered-rfc5549
name: bgp-unnumbered-rfc5549
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, extended-nexthop, bgp-unnumbered, rfc5549, ipv6-nexthop]
level: practitioner
status: draft
description: "Run IPv4 BGP over IPv6 link-local sessions on EOS using extended next-hop encoding (RFC 5549) for unnumbered fabrics."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BGP unnumbered with extended next-hop
Goal: avoid per-link IPv4 addressing in a leaf-spine underlay.

```
ip routing ipv6 interfaces
interface Ethernet1
   no switchport
   ipv6 enable
router bgp 65101
   neighbor interface Ethernet1 peer-group SPINES remote-as 65100
   address-family ipv4
      neighbor SPINES activate
      neighbor SPINES next-hop address-family ipv6 originate
```

Also keep a unique loopback per switch for router-id and VTEP:
```
interface Loopback0
   ip address 10.255.0.11/32
```

```
show ip bgp summary
show ipv6 neighbors
show ip route 10.255.0.1
```

- Needs `ip routing ipv6 interfaces` (confirm the exact command for your release); platform support varies (confirm).
- The route's next hop is shown as an IPv6 link-local address resolved through the interface.

Gotcha: the other end must support the capability; sessions that establish without IPv4 next-hops installed usually miss `ip routing ipv6 interfaces`.

Operational tip: even with unnumbered links, keep unique loopbacks as router IDs and VTEP addresses, and advertise them via `network` or a route-map so every leaf can reach every other leaf loopback.

## Verify
- Routes show next hop via `Ethernet1` and `ping 10.255.0.1 source 10.255.0.11` succeeds.
