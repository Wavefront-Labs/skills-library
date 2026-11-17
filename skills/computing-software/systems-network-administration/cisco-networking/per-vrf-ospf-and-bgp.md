---
id: computing-software.systems-network-administration.cisco-networking.per-vrf-ospf-and-bgp
name: per-vrf-ospf-and-bgp
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, vrf, vrf-routing-protocols, ospf-vrf, bgp-vrf, address-family-ipv4-vrf, capability-vrf-lite, vrf-lite]
level: practitioner
status: draft
description: "Run OSPF and BGP per VRF on IOS XE: process-per-VRF OSPF, BGP address-family ipv4 vrf, router IDs, capability vrf-lite and verification commands."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/configuration/xe-16/iro-xe-16-book/iro-vrf-lite.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/mp_l3_vpns/configuration/xe-16/mp-l3-vpns-xe-16-book/mp-bgp-mpls-vpn.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Per-VRF OSPF and BGP

## OSPF: one process per VRF
```
router ospf 101 vrf RED
 router-id 10.255.101.1
 capability vrf-lite                   ! needed on CE-style VRF-Lite routers (see below)
 passive-interface default
 no passive-interface GigabitEthernet0/1.101
interface GigabitEthernet0/1.101
 encapsulation dot1Q 101
 vrf forwarding RED
 ip address 10.101.12.1 255.255.255.252
 ip ospf 101 area 0
```
- Each VRF needs its own OSPF process number; the interface must be in the VRF **before** you add the IP and OSPF.
- `capability vrf-lite`: an OSPF process in a VRF assumes it is a PE and suppresses the DN-bit/
  down-bit loop checks for routes from MPLS VPN; without the capability on VRF-Lite routers, type
  3/5 LSAs with the DN bit set may not be installed. Use it on VRF-Lite (non-MPLS) designs.
- Router ID per process: set it explicitly (VRF loopbacks) to avoid duplicates.

## BGP: one process, address-family per VRF
```
router bgp 65010
 bgp router-id 10.255.0.1
 address-family ipv4 vrf RED
  bgp router-id 10.255.101.1           ! optional per-VRF RID
  neighbor 10.101.12.2 remote-as 65020
  neighbor 10.101.12.2 activate
  redistribute connected route-map RED-CONN
 address-family ipv4 vrf BLUE
  neighbor 10.102.12.2 remote-as 65020
  neighbor 10.102.12.2 activate
```
Per-VRF BGP needs an RD on the VRF on many IOS releases even without MPLS (`rd 65010:101`).

## Verify
```
show ip ospf 101 neighbor
show ip route vrf RED ospf
show bgp vpnv4 unicast vrf RED summary      ! or show ip bgp vpnv4 vrf RED summary
show ip bgp vpnv4 vrf RED neighbors 10.101.12.2
show ip protocols vrf RED
```
- [ ] Each VRF table only contains its own routes; neighbours up in each VRF.
