---
id: computing-software.systems-network-administration.cisco-networking.vrf-route-leaking
name: vrf-route-leaking
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, vrf, vrf-lite, route-leaking, inter-vrf-routing, route-target, import-map, bgp-vrf, static-route-vrf, global-keyword, shared-services, route-replicate]
level: advanced
status: draft
description: "Leak routes between VRFs on IOS XE for shared services: static leaks with the global keyword, MP-BGP route-target import/export with route-maps, and avoiding overlap and asymmetry."
sources:
  - https://www.cisco.com/c/en/us/support/docs/multiprotocol-label-switching-mpls/multiprotocol-label-switching-vpns-mpls-vpns/47807-routeleaking.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/mp_l3_vpns/configuration/xe-16/mp-l3-vpns-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VRF route leaking

Use it when isolated VRFs need a shared service (DNS, DHCP, AD, internet edge) without merging
them. Leaking must be **bidirectional**: the service needs a route back.

## Method 1: static routes (small, simple)
VRF GUEST reaching a DNS server in the global table, and the return route:
```
ip route vrf GUEST 10.0.0.53 255.255.255.255 10.0.0.53 global   ! next hop resolved in global table
ip route 10.90.0.0 255.255.0.0 Vlan90                           ! global -> VRF via an interface in the VRF
```
The second line points the global table at an interface that belongs to the VRF (directly
connected subnet). For non-connected VRF prefixes, use BGP.

## Method 2: MP-BGP route targets (scales, policy control)
```
vrf definition SHARED
 rd 65000:100
 address-family ipv4
  route-target export 65000:100
  route-target import 65000:100
  route-target import 65000:90           ! pull GUEST routes
 exit-address-family
vrf definition GUEST
 rd 65000:90
 address-family ipv4
  route-target export 65000:90
  route-target import 65000:90
  import map ONLY-DNS                     ! only take selected SHARED routes
  route-target import 65000:100
 exit-address-family
!
ip prefix-list DNS-SERVERS permit 10.0.0.53/32
route-map ONLY-DNS permit 10
 match ip address prefix-list DNS-SERVERS
!
router bgp 65000
 address-family ipv4 vrf GUEST
  redistribute connected
  redistribute ospf 90
 address-family ipv4 vrf SHARED
  redistribute connected
```
BGP is needed even on a single box with no neighbours: it is the engine that copies routes
between VRF tables. Global-to-VRF leaking uses `route-replicate` (IOS XE) or
`import ipv4 unicast map` in the VRF address family.

## Rules
- No overlapping prefixes between VRFs that leak to each other.
- Firewalls between VRFs are often better than leaking (inspection, logging); leaking bypasses
  any segmentation policy.
- Check hardware: inter-VRF forwarding may be done in software on some platforms.

## Verify
```
show ip route vrf GUEST 10.0.0.53     ! shows "(SHARED)" / via BGP imported
show bgp vpnv4 unicast all
ping vrf GUEST 10.0.0.53 source Vlan90
```
- [ ] Each side has a route to the other; only intended prefixes leaked.
