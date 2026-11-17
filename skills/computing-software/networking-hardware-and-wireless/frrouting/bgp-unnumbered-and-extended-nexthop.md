---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-unnumbered-and-extended-nexthop
name: bgp-unnumbered-and-extended-nexthop
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, bgp-unnumbered, interface-neighbor, v6only, extended-nexthop, ipv6-link-local]
level: advanced
status: docs-checked
description: "Configure FRR BGP unnumbered peers on an interface with v6only, extended-nexthop, link-local next hops and IPv6 router advertisements."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP unnumbered and extended nexthop
- `neighbor PEER interface [v6only] [peer-group NAME]` configures an unnumbered peer on an interface. By default it derives an IPv4 address from a /30 or /31 on the interface and falls back to the IPv6 link-local address; `v6only` skips IPv4 and uses link-local directly.
- `neighbor PEER interface [v6only] remote-as <internal|external|auto|ASN>` combines both in one command. Intended for point-to-point links: only one neighbor comes up on a shared Ethernet segment.
- `neighbor PEER capability extended-nexthop` negotiates extended next hop; it is automatic for IPv6 link-local peering.
- `neighbor PEER capability link-local` sends only the link-local IPv6 next hop (16 bytes); default disabled.
- `bgp ipv6-auto-ra` controls whether bgpd asks zebra to send IPv6 router advertisements; it applies to unnumbered peers and the extended-nexthop capability.
- `nexthop prefer-global` (IPv6 address-family mode) installs the global IPv6 next hop to zebra instead of the link-local one (default: link-local is installed); the BGP RIB keeps both.
- `neighbor PEER attribute-unchanged next-hop` helps with IPv6 next hops since the route-map directive to leave the next hop unchanged is available only for IPv4.
- `neighbor PEER next-hop-self [force]` sets the advertised next hop to the local address for eBGP-learned routes; `force` also covers iBGP-learned ones.

## Checked
2026-11-09. Partial read of docs.frrouting.org bgp.html (one large page): neighbor interface (v6only, remote-as forms), capability extended-nexthop and link-local, bgp ipv6-auto-ra, nexthop prefer-global, attribute-unchanged and next-hop-self. Removed: the route-map set ipv6 next-hop forms other than the prefer-global mention (not documented on this page); replaced with the documented nexthop prefer-global command.
Method: documentation only; no commands were run.
