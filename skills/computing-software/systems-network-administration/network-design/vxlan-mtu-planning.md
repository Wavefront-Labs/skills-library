---
id: computing-software.systems-network-administration.network-design.vxlan-mtu-planning
name: vxlan-mtu-planning
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, dc-fabric, vxlan-mtu, jumbo-frames, encapsulation-overhead, evpn]
level: practitioner
status: verified
description: "Plan MTU for VXLAN fabrics: 50/54-byte overhead, underlay jumbo MTU everywhere, host MTU choices, DCI and cloud tunnels, and how to test it end to end."
sources:
  - https://www.rfc-editor.org/rfc/rfc7348
  - https://www.cisco.com/c/en/us/td/docs/dcn/nx-os/nexus9000/103x/configuration/vxlan/cisco-nexus-9000-series-nx-os-vxlan-configuration-guide-release-103x.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VXLAN MTU planning

## Overhead (RFC 7348)
The inner Ethernet frame (14-byte header plus the host MTU) is the UDP payload, so the underlay needs
inner frame + VXLAN 8 + UDP 8 + outer IPv4 20: **50 bytes more than the host IP MTU** (70 with an IPv6
outer header). The outer Ethernet header (14, or 18 with an 802.1Q tag) is on top of that and does not
count in the IP MTU. Checked with scapy: an inner 1500-byte IP packet becomes a 1564-byte frame
including the outer Ethernet header.

So a host MTU 1500 needs underlay IP MTU >= 1550; host jumbo 9000 needs >= 9050. RFC 7348 states that
VTEPs MUST NOT fragment VXLAN packets.

## Plan
| Layer | Setting |
|---|---|
| Underlay interfaces (leaf-spine, spine-superspine) | the platform maximum (commonly 9216 on data-centre switches; check yours) everywhere |
| Overlay SVIs / anycast gateways | 9000 or 1500 by host policy (must be <= underlay - 50) |
| Hosts | 1500 default; 9000 for storage/vMotion VLANs if every hop supports it |
| DCI / WAN tunnels | often limited to 1500: clamp MSS or keep hosts at 1500 for stretched VLANs |
| Cloud (AWS: 9001 jumbo inside the VPC on supporting instance types, 1500 over an internet gateway or VPN; Azure VMs default to 1500) | match the smallest |

Oversize VXLAN packets are not fragmented by VTEPs (RFC 7348), so they are dropped when the path is
too small. OSPF carries the interface MTU in Database Description packets (RFC 2328) and a mismatch
stops adjacencies reaching Full; BGP sessions can stall when large updates hit a smaller hop.

## Test
```
# from a host in VLAN 10 to a host on another leaf
ping -M do -s 1472 10.10.0.20   # 1500 works
ping -M do -s 8972 10.10.0.20   # 9000 if jumbo hosts
```
Underlay checks use the same DF ping from your platform's source-interface option at host MTU + 50
(vendor syntax differs; take it from the platform documentation).

## Verify
- [ ] Underlay ping between all VTEP loopbacks at (host MTU + 50) with DF passes; host-level DF pings at host MTU pass across leaves and DCI.
