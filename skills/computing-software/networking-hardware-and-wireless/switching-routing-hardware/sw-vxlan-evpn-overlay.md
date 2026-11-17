---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-vxlan-evpn-overlay
name: sw-vxlan-evpn-overlay
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [vxlan-evpn, vtep-vni, evpn-type-2-5]
level: advanced
status: draft
description: "Explain VXLAN VTEPs, VNIs and the BGP EVPN control plane (type-2 MAC/IP, type-5 prefix) for tenant L2 and L3 overlays."
sources:
  - https://www.rfc-editor.org/rfc/rfc7348
  - https://www.rfc-editor.org/rfc/rfc7432
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VXLAN with EVPN

- VXLAN encapsulates L2 frames in UDP (destination port 4789) with a 24-bit VNI, allowing roughly 16 million segments. The VTEP is the encapsulating/decapsulating endpoint.
- EVPN (BGP address family) distributes MAC/IP reachability (route type 2), IP prefixes (type 5), and inclusive multicast (type 3) instead of flood-and-learn.
- Anycast gateway: every leaf answers as the same default gateway for a VLAN/VNI; symmetric IRB routes between VNIs via an L3 VNI.
- Overhead: about 50 bytes; raise underlay MTU by at least that much.
- Multi-homing with EVPN Ethernet segments (ESI) replaces MLAG in some designs.

## Verify
- [ ] BGP EVPN table shows type-2 routes for attached hosts and VTEP peers are up.
