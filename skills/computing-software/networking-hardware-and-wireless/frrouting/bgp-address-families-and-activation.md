---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-address-families-and-activation
name: bgp-address-families-and-activation
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, address-family, activate, ipv6-unicast, safi, bgp-default]
level: practitioner
status: docs-checked
description: "Enable BGP address families in FRR with address-family blocks and neighbor activate, and control which families new neighbors get by default with bgp default commands."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP address families and activation
- `address-family ipv4 unicast` / `ipv6 unicast` blocks end with `exit-address-family`. Other families named in the docs include multicast, vpn, labeled-unicast, flowspec, `l2vpn evpn`, link-state and unreachability.
- `neighbor A.B.C.D activate` enables a neighbor for an address family. IPv4 unicast is enabled by default.
- `no bgp default ipv4-unicast` requires every address family to be enabled explicitly.
- Default-enable switches for new neighbors: `bgp default ipv4-unicast` (default on); `ipv4-multicast`, `ipv4-vpn`, `ipv4-flowspec`, `ipv6-unicast`, `ipv6-multicast`, `ipv6-vpn`, `ipv6-flowspec`, `l2vpn-evpn` (all default off).
- `network A.B.C.D/M` (or an IPv6 prefix) announces a prefix under an address family.
- `maximum-paths` can be set per AFI/SAFI.
- `bgp default show-hostname` and `bgp default show-nexthop-hostname` show hostnames in some outputs.
- `bgp default dynamic-capability` and `bgp default software-version-capability [latest-encoding]` are on by default in the datacenter profile.

Display by family: `show bgp [<ipv4|ipv6> <unicast|multicast|vpn|labeled-unicast|flowspec|unreachability> | l2vpn evpn]`; with no family the default is IPv6 unicast.

## Checked

2026-11-04. Confirmed against the FRR BGP page: address-family blocks, neighbor activate, the bgp default <family> switches and their defaults, maximum-paths per AFI/SAFI, show-hostname, dynamic and software-version capability defaults, the show bgp family forms and BGP-LS link-state family. Nothing changed.
Method: documentation only; no commands were run.
