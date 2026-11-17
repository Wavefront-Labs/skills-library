---
id: computing-software.systems-network-administration.network-design.vxlan-evpn-fabric-basics
name: vxlan-evpn-fabric-basics
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, vxlan, evpn, vtep, vni, l2vni, l3vni, evpn-route-types, anycast-gateway, distributed-anycast-gateway, bgp-evpn, arp-suppression, symmetric-irb, spine-leaf, data-center-design]
level: advanced
status: docs-checked
description: "Design a VXLAN EVPN fabric: VTEPs and VNIs, L2 vs L3 VNIs, EVPN route types 2/3/5, distributed anycast gateway, symmetric IRB, underlay MTU and checks."
sources:
  - https://datatracker.ietf.org/doc/html/rfc7348
  - https://datatracker.ietf.org/doc/html/rfc7432
  - https://datatracker.ietf.org/doc/html/rfc9135
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VXLAN EVPN fabric basics

## Building blocks
- **VXLAN** (RFC 7348): Ethernet frames in UDP 4789, 24-bit **VNI** (16M segments).
  Encapsulated by **VTEPs** (usually leaf switches, loopback as source).
- **EVPN** (RFC 7432, BGP l2vpn evpn): control plane that advertises MAC/IP bindings and VTEP
  membership, replacing flood-and-learn.
- Underlay: routed spine-leaf (eBGP or OSPF/IS-IS), loopbacks reachable via ECMP, an **MTU that accommodates the VXLAN
  encapsulation** (RFC 7348 recommends raising MTUs across the physical network). Overlay: iBGP/eBGP EVPN sessions (spines as route reflectors or eBGP transit).

## VNI types
| Type | Maps | Purpose |
|---|---|---|
| L2VNI | one VLAN | bridging the same subnet across leaves |
| L3VNI | one VRF | routing between subnets across leaves (symmetric IRB) |

## EVPN route types to recognise
| Type | Carries | Used for |
|---|---|---|
| 2 MAC/IP advertisement | host MAC (+IP) and VNI(s) | host reachability, ARP suppression |
| 3 Inclusive multicast | VTEP joining an L2VNI | BUM replication list (ingress replication) |
| 5 IP prefix | subnets/external routes in a VRF | routing to prefixes, border leaf externals |
| 1, 4 | Ethernet segment routes | multihoming (ESI) |

## Distributed anycast gateway
Every leaf hosts the same gateway IP **and MAC** for each subnet. Hosts route at their first hop; VMs moving between racks keep the same gateway; no
FHRP needed.

## Symmetric IRB
Routed traffic: ingress leaf routes into the L3VNI, egress leaf routes out of it. Each leaf only
needs the VLANs/VNIs of its local hosts plus the VRF's L3VNI (asymmetric IRB needs every VNI
everywhere).

## Checks
Use the vendor's commands to confirm that remote VTEPs are up, each VNI is up in control-plane
mode, EVPN sessions are established and type-2 routes exist for learned hosts.
Common faults: underlay MTU too small (large packets drop while ping works), VNI-to-VLAN or
L3VNI mismatch between leaves, route-target mismatch between leaves, anycast gateway MAC inconsistent.

## Verify
- [ ] All NVE peers up; type-2 routes for test hosts visible on remote leaves.
- [ ] Host-to-host same subnet and inter-subnet across leaves both work with 1500-byte DF pings.

## Checked

- Date: 2026-10-28
- Confirmed: VXLAN uses UDP port 4789 and a 24-bit VNI (up to 16M segments) (RFC 7348); RFC 7348 recommends raising MTUs for the encapsulation; RFC 9135 defines symmetric and asymmetric IRB; RFC 7432 covers MAC/IP, inclusive multicast and Ethernet segment routes; Arista overview lists type-5 IP-prefix routes.
- Removed: the 1550/9216 MTU figures, the NX-OS anycast-gateway command, the NX-OS show-command block, the auto route-target remark.

Method: documentation only; no commands were run.
