---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-l3vpn-route-leaking
name: bgp-l3vpn-route-leaking
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, l3vpn, route-leaking, rd, route-target, import-vrf, srv6-vpn, mpls-vpn]
level: sme
status: docs-checked
description: "Configure BGP L3VPN and VRF route leaking in FRR with rd, rt vpn, label and nexthop export, import vrf shortcuts, route-maps, and SRv6 SID options."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP L3VPN and route leaking
Under a VRF's `address-family ipv4|ipv6 unicast`:
- `rd vpn export AS:NN|IP:nn`.
- `rt vpn import|export|both RTLIST...`.
- `label vpn export allocation-mode per-vrf|per-nexthop` (default per-vrf); `label vpn export (0..1048575)|auto` (export blocks if Zebra is unavailable).
- `nexthop vpn export A.B.C.D|X:X::X:X` (default self).
- `route-map vpn import|export MAP`; `import|export vpn` enables the direction.
- `import vrf VRFNAME` leaks from another VRF via the default VPN RIB with RD and RT auto-derived and not set explicitly; `import vrf route-map NAME` filters it. The shortcut is not compatible with explicit `import vpn`/`export vpn` on the two VRFs involved (the CLI refuses it). `rt vpn export` is optional: `set extcommunity rt` in the `route-map vpn export` map can supply the RT per prefix.
- `bgp retain route-target all` retains VPN prefixes not imported locally (default on, not displayed).
- Interface context: `mpls bgp forwarding`, `mpls bgp l3vpn-multi-domain-switching`.
- `set l3vpn next-hop encapsulation <gre|gretap>` in an inbound route-map accepts L3VPN next hops over GRE tunnels.

SRv6 transport: `segment-routing srv6`, `locator NAME`, `encap-behavior <H_Encaps|H_Encaps_Red>`, `srv6-only` (default when a locator is set), `sid vpn per-vrf export <(1..1048575)|auto|explicit X:X::X:X>`, `sid vpn export ...` per AF, `neighbor X:X::X:X encapsulation-srv6|encapsulation-mpls`. Show: `show bgp segment-routing srv6`, `show bgp ipv6 vpn detail`, `show bgp nexthop detail`, `show bgp vrfs`. A VRF can have at most one L3 service enabled at a time. `no srv6-only` (under `segment-routing srv6`) lets MPLS and SRv6 updates coexist.

## Checked

2026-11-09. Read the FRR BGP page sections "VRF Route Leaking" (required parameters, general configuration), "BGP-Based L3 Service over SRv6", "L3VPN SRv6 configuration", "Filtering SRv6/MPLS per neighbor", the `set l3vpn next-hop encapsulation` text and the show commands via a local text copy; every command, range and default above matches. Added the import vrf incompatibility, the route-map RT option and the no srv6-only note.
Method: documentation only; no commands were run.
