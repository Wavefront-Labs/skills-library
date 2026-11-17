---
id: computing-software.systems-network-administration.cisco-networking.vrf-lite-configuration
name: vrf-lite-configuration
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, vrf, vrf-lite, vrf-definition, vrf-forwarding, address-family, path-isolation, vrf-aware, ping-vrf, show-ip-route-vrf, management-vrf, mgmt-vrf, routing-context]
level: practitioner
status: draft
description: "Isolate routing tables with VRF-lite on IOS XE: vrf definition, moving interfaces in, per-VRF routing, VRF-aware ping/traceroute/show/copy, and the management VRF on Catalyst."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/rtng/b_179_rtng_9300_cg/configuring_vrf_lite.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/mp_l3_vpns/configuration/xe-16/mp-l3-vpns-xe-16-book/mp-vrf-lite.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VRF-lite configuration

A VRF is a separate routing and forwarding table on the same device. VRF-lite = VRFs without
MPLS: each VRF is carried hop by hop on its own subinterface/VLAN.

## Define and assign
```
vrf definition GUEST
 rd 65000:90                    ! optional for VRF-lite, required by some features
 address-family ipv4
 exit-address-family
 address-family ipv6
 exit-address-family
!
interface Vlan90
 vrf forwarding GUEST           ! REMOVES the IP address: re-enter it after
 ip address 10.90.0.1 255.255.0.0
!
interface Te1/1/1.90            ! or a dedicated VLAN SVI/trunk VLAN toward the next hop
 encapsulation dot1Q 90
 vrf forwarding GUEST
 ip address 172.31.90.1 255.255.255.252
!
router ospf 90 vrf GUEST
 network 10.90.0.0 0.0.255.255 area 0
 network 172.31.90.0 0.0.0.3 area 0
ip route vrf GUEST 0.0.0.0 0.0.0.0 172.31.90.2
```
Older syntax `ip vrf NAME` / `ip vrf forwarding` is IPv4-only; prefer `vrf definition`.

## VRF-aware operations
Everything defaults to the global table; add `vrf` explicitly:
```
show ip route vrf GUEST
show ip arp vrf GUEST
show ip interface brief vrf GUEST
ping vrf GUEST 10.90.0.50
traceroute vrf GUEST 8.8.8.8
show ip ospf 90 neighbor
copy tftp: flash: vrf Mgmt-vrf      ! or 'ip tftp source-interface' in that VRF
ssh -vrf Mgmt-vrf -l admin 10.0.0.5
```

## Management VRF on Catalyst
Catalyst 9000 has `Mgmt-vrf` built in, bound to the out-of-band `GigabitEthernet0/0`. Services
must be pointed at it: `ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 <OOB-GW>`, `ntp server vrf
Mgmt-vrf`, `logging host <IP> vrf Mgmt-vrf`, `ip http client source-interface Gi0/0`,
`snmp-server host <IP> vrf Mgmt-vrf ...`, and `ip ssh source-interface`/`vty access-class ... vrf-also`
where needed (an `access-class` on VTY without `vrf-also` blocks SSH arriving in a VRF).

## Gotchas
- DHCP relay across VRFs needs `ip helper-address vrf <server-vrf> <ip>` or `global`.
- Routing processes are per VRF for OSPF (`router ospf N vrf X`); BGP uses `address-family ipv4 vrf X`.
- Overlapping addresses between VRFs are fine; NAT and services must be VRF-aware.

## Verify
- [ ] `show vrf` lists the interfaces in each VRF.
- [ ] Global table has no routes for the VRF prefixes and vice versa.
- [ ] Management services (NTP, syslog, AAA) work from Mgmt-vrf.
