---
id: computing-software.systems-network-administration.network-design.vxlan-bum-replication
name: vxlan-bum-replication
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, dc-fabric, ingress-replication, bum-traffic, vxlan-multicast, evpn-type-3, arp-suppression]
level: practitioner
status: docs-checked
description: "Choose how a VXLAN fabric carries broadcast, unknown unicast and multicast: ingress replication via EVPN inclusive multicast vs underlay multicast, and suppression features."
sources:
  - https://www.rfc-editor.org/rfc/rfc8365
  - https://www.rfc-editor.org/rfc/rfc7432
  - https://www.cisco.com/c/en/us/td/docs/dcn/nx-os/nexus9000/103x/configuration/vxlan/cisco-nexus-9000-series-nx-os-vxlan-configuration-guide-release-103x.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BUM replication in VXLAN

BUM = broadcast, unknown unicast, multicast. Each VNI needs a way to deliver BUM frames to all
VTEPs that host it.

## Ingress (head-end) replication
- Source VTEP sends a unicast copy to each remote VTEP in the VNI.
- With EVPN, the flood list is built from the **Inclusive Multicast Ethernet Tag route** (RFC 7432 section 7.3);
  no static peer lists.
- Pros: no underlay multicast, simple; suits modest VTEP counts per VNI.
- Cons: source VTEP and its uplinks carry N copies; heavy BUM traffic across many VTEPs hurts.

## Underlay multicast
- Each VNI maps to a multicast group; VTEPs join via PIM (RFC 8365 names PIM-SM, PIM-SSM and BIDIR-PIM); the
  underlay replicates.
- Pros: efficient at large scale and for heavy BUM/multicast apps.
- Cons: PIM, RPs, group planning and troubleshooting skills in the underlay.

## Reduce BUM first
- **ARP/ND suppression**: VTEPs answer ARP from EVPN type-2 MAC/IP entries.
- Disable unknown-unicast flooding where hosts are learned via EVPN (silent hosts may break).
- Tenant multicast: use IGMP snooping and the optimised-multicast features your platform supports.
- Keep L2 domains small; route at the leaf (distributed anycast gateway).

## Verify
- [ ] the flood list holds all expected VTEPs per VNI; a broadcast test reaches hosts on every leaf; BUM rate baselined.

## Checked

- Date: 2026-10-28
- Confirmed: RFC 7348 section 4.2 maps broadcast to multicast; RFC 7432 Inclusive Multicast Ethernet Tag route and ARP/ND section; RFC 8365 describes ingress replication and PIM-SM/SSM/BIDIR.
- Removed: route type number, VTEP-count thresholds, OISM and type 6-8 routes, the NX-OS config sketch and show commands.

Method: documentation only; no commands were run.
