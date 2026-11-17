---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-evpn-configuration
name: bgp-evpn-configuration
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, evpn, vxlan, vni, route-target, type-5, advertise-svi-ip, advertise-pip]
level: sme
status: docs-checked
description: "Configure BGP EVPN in FRR: l2vpn evpn address family, advertise-all-vni, L3VNI per VRF, type-5 prefix export, route targets, SVI and PIP advertisement, and the Linux VXLAN setup."
sources:
  - https://docs.frrouting.org/en/latest/evpn.html
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP EVPN
Under `router bgp ASN`:
- `address-family l2vpn evpn` then `neighbor ADDR activate`.
- `advertise-all-vni` enables EVPN for the instance.
- `advertise-svi-ip` originates type-2 routes for local SVI MAC/IP; do not combine with `advertise-default-gw`.
- `advertise-pip [ip ADDR [mac ADDR]]` enables or disables the advertise-pip feature, with optional system IP and MAC.
- In a VRF's `l2vpn evpn` family: `advertise ipv4 unicast` / `advertise ipv6 unicast` exports prefixes as type-5 routes; this requires an L3VNI.

VRF to L3VNI: `vrf NAME`, `vni N`, `exit-vrf` (as in the page's sample configuration).

Route targets: `route-target import|export|both RT` (import accepts `*:N`). `auto-route-target import|export|both [rfc8365-compatible]` with modes `add-if-no-manual` (default), `add-always`, `add-never`; automatic import RT is `*:VNI`, export is `(AS & 0xFFFF):VNI`.

Linux VXLAN (iproute2):
- Prefer a single VXLAN device: `ip link add DEV type vxlan external vnifilter ...`; map with `bridge vni add dev DEV vni VNI`.
- Bridge port: `vlan_tunnel on neigh_suppress on learning off`.
- VTEP IP on `lo`, no static `remote`.
- Anycast gateway: same MAC on all VTEPs.

Show: `show vrf [NAME|all] vni`, `show evpn mac vni VNI detail`, `show bgp l2vpn evpn ...`.

## Checked

2026-11-04. Confirmed against the FRR EVPN page and BGP page (EVPN sections): advertise-all-vni, advertise-svi-ip and advertise-default-gw caveat, route-target and auto-route-target modes and encoding, single VXLAN device options, bridge port settings, VTEP IP on lo, anycast MAC, show commands. Removed the VNI range and the claim about zebra treating the VNI as L2, and the 'off by default' wording for type-5 advertisement, none of which the pages state.
Method: documentation only; no commands were run.
