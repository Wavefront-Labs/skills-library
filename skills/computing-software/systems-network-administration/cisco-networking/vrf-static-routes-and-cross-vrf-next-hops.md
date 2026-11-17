---
id: computing-software.systems-network-administration.cisco-networking.vrf-static-routes-and-cross-vrf-next-hops
name: vrf-static-routes-and-cross-vrf-next-hops
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, vrf, vrf-static-route, ip-route-vrf, static-routing, route-leaking, global-next-hop]
level: practitioner
status: draft
description: "Write static routes inside VRFs, point a VRF route at a global next hop or another VRF interface, and avoid the recursion traps that break them."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/mp_l3_vpns/configuration/xe-16/mp-l3-vpns-xe-16-book/mp-bgp-mpls-vpn.html
  - https://www.cisco.com/c/en/us/support/docs/multiprotocol-label-switching-mpls/multiprotocol-label-switching-vpns-mpls-vpns/47807-routeleaking.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Static routes in VRFs and cross-VRF next hops

## Inside one VRF
```
ip route vrf CUST-A 0.0.0.0 0.0.0.0 172.16.1.1
ip route vrf CUST-A 10.50.0.0 255.255.0.0 GigabitEthernet0/2 172.16.2.2   ! interface must be in CUST-A
show ip route vrf CUST-A static
```
The next hop is resolved in the VRF's own table.

## VRF route with a global next hop
```
ip route vrf CUST-A 0.0.0.0 0.0.0.0 203.0.113.1 global
```
`global` makes the next hop resolve in the global table: classic shared internet access from a VRF.
Return traffic needs a global route back into the VRF:
```
ip route 172.16.1.0 255.255.255.0 GigabitEthernet0/2 172.16.1.2   ! exit interface in VRF CUST-A
```
A global static pointing out an interface that belongs to a VRF works on IOS only with the
interface **and** next hop specified (fully specified), because the next hop cannot be resolved
in the global table.

## VRF to another VRF
Point at the other VRF's interface plus next hop:
```
ip route vrf CUST-A 10.200.0.0 255.255.0.0 GigabitEthernet0/3 10.200.0.1   ! Gi0/3 in VRF SHARED
```
For anything beyond a few routes, use MP-BGP route-target import/export (see vrf-route-leaking).

## Gotchas
- NAT for VRF-to-internet needs `ip nat inside source ... vrf CUST-A` on the NAT rule.
- `ping vrf CUST-A <dest>` and `traceroute vrf ...`: a plain ping uses the global table and misleads.
- Statics with `global` do not appear in the global table, only in the VRF.
- Overlapping VRF prefixes cannot both be leaked into global; NAT them first.

## Verify
```
show ip route vrf CUST-A 0.0.0.0
show ip cef vrf CUST-A 0.0.0.0 detail      ! next hop resolved in global
ping vrf CUST-A 8.8.8.8 source GigabitEthernet0/2
```
- [ ] Both directions resolve (VRF -> global and global -> VRF).
