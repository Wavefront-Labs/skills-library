---
id: computing-software.systems-network-administration.cisco-networking.easy-virtual-network-evn
name: easy-virtual-network-evn
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, easy-virtual-network, evn, vnet-trunk, vrf-lite, path-isolation, vnet-tag, campus-virtualization]
level: practitioner
status: draft
description: "Simplify VRF-Lite path isolation with Cisco Easy Virtual Network: vnet tags, vnet trunk interfaces, per-VRF routing over one trunk, and its platform limits."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/evn/configuration/xe-16/evn-xe-16-book/evn-overview.html
  - https://www.cisco.com/c/en/us/products/collateral/ios-nx-os-software/easy-virtual-network-evn/whitepaper_c11-638769.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Easy Virtual Network (EVN)

## What it solves
VRF-Lite across a campus needs a subinterface (or SVI) and an IP subnet per VRF per link: with
5 VRFs and 40 links that is 200 subinterfaces. EVN uses one **vnet trunk** per link and tags
VRF traffic with a vnet tag (802.1Q under the hood); per-VRF subinterfaces are created implicitly.

## Config
```
vrf definition RED
 vnet tag 101
 address-family ipv4
vrf definition BLUE
 vnet tag 102
 address-family ipv4
interface GigabitEthernet0/1
 vnet trunk                             ! all VRFs with vnet tags carried; or 'vnet trunk list VNETS'
 ip address 10.0.12.1 255.255.255.252   ! same IP reused per VRF on the trunk
 ip ospf 1 area 0
router ospf 101 vrf RED
router ospf 102 vrf BLUE
```
Per-VRF overrides on the trunk:
```
interface GigabitEthernet0/1
 vnet name RED
  ip ospf cost 50
```
Edge interfaces are normal `vrf forwarding RED` interfaces.

## Features
- Route replication between VRFs (`route-replicate` under address-family) for shared services
  without BGP.
- `routing-context vrf RED` changes the CLI context so `show ip route` etc. apply to RED.

## Limits
- Supported on specific IOS/IOS XE router and Catalyst platforms and releases; Catalyst 9000
  support is limited. Check the feature navigator before designing around it.
- Both ends must run EVN with matching vnet tags (1-4094) and the same IPs reused per VRF.
- Many designs now use SD-Access (LISP/VXLAN) or BGP EVPN instead.

## Verify
```
show vnet trunk
show vnet tag
show ip route vrf RED
show ip ospf 101 neighbor
```
