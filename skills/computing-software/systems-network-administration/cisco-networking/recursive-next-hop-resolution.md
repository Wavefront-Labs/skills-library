---
id: computing-software.systems-network-administration.cisco-networking.recursive-next-hop-resolution
name: recursive-next-hop-resolution
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, recursive-lookup, next-hop, cef, bgp-next-hop, routing-table, show-ip-route]
level: practitioner
status: draft
description: "Trace how IOS resolves recursive next hops (static and BGP) to an outgoing interface, spot recursion failures and loops, and pin resolution with fully specified routes."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/107582-bgp-recursion.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_pi/configuration/xe-16/iri-xe-16-book/iri-ip-static-route.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recursive next-hop resolution

A route whose next hop is not directly connected must be resolved by another lookup, possibly
several. CEF precomputes this, but you need to understand it to debug blackholes.

## Follow the chain
```
show ip route 203.0.113.0
!  Routing entry for 203.0.113.0/24
!  Known via "bgp 65001", distance 200
!    * 192.0.2.2, from 192.0.2.2       <- BGP next hop (iBGP loopback)
show ip route 192.0.2.2
!    * 10.0.12.2, via GigabitEthernet0/1   <- resolved via OSPF
show ip cef 203.0.113.10 detail
!  recursive via 192.0.2.2
!    nexthop 10.0.12.2 GigabitEthernet0/1
```
CEF shows the final adjacency. If `show ip cef` says `unresolved` or `drop`, the chain is broken.

## Typical failures
| Symptom | Cause |
|---|---|
| BGP route in table but not best, `(inaccessible)` in `show ip bgp` | next hop has no route; add `next-hop-self` or advertise the link |
| Route flaps every few seconds | recursive routing: next hop resolved through the route itself (e.g. GRE tunnel destination learned over the tunnel) |
| Static default via 203.0.113.1 stays when the ISP link is down | next hop still resolvable via another route (often a less specific one) |
| `%ADJ-3-RESOLVE_REQ` or incomplete ARP | next hop IP not answering ARP on the resolved interface |

## Pin resolution
- Fully specified static: `ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/1 203.0.113.1` resolves only
  out that interface; if it goes down the route is withdrawn.
- BGP: `bgp nexthop route-map` / `bgp nexthop trigger delay` control which routes may resolve next
  hops (e.g. forbid resolution via the default route).
- Static: `ip route static adjust-time` and `ip route ... track` for liveness.

## Gotchas
- A default route can resolve any next hop; that hides failures. Many designs prevent BGP next-hop
  resolution through 0/0.
- Recursion depth is limited; long chains of statics pointing at statics are fragile and hard to
  read. Keep one level.
- IPv6 static routes to link-local next hops must include the interface.

## Verify
- [ ] `show ip cef <prefix> detail` shows the intended egress interface and adjacency.
- [ ] Shutting the primary path withdraws the dependent routes rather than blackholing.
