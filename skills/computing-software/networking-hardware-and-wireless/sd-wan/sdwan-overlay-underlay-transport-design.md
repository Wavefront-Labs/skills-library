---
id: computing-software.networking-hardware-and-wireless.sd-wan.sdwan-overlay-underlay-transport-design
name: sdwan-overlay-underlay-transport-design
category: computing-software
field: networking-hardware-and-wireless
product: sd-wan
tags: [sdwan-overlay-underlay, sdwan-transports, sdwan-color-tloc]
level: practitioner
status: draft
description: "Design SD-WAN transports: mix MPLS and internet circuits, assign transport roles, size circuits and handle NAT traversal."
sources:
  - https://www.mef.net/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Overlay and underlay

- Underlay: the physical WAN circuits (MPLS, broadband, DIA, LTE/5G). Overlay: encrypted tunnels between SD-WAN edges built over them.
- Label transports (colours/links) so policies can steer by type (e.g. MPLS for voice, internet for bulk).
- Behind NAT, edges use STUN-like discovery and UDP encapsulation; symmetric NAT on both ends can prevent direct tunnels, so use hubs or relay.
- Dual-circuit sites: use two different carriers and last-mile paths where possible; check diversity.
- Size circuits for tunnel overhead (IPsec adds roughly 50-70 bytes) and adjust MSS/MTU.

## Verify
- [ ] All expected tunnels are up per transport colour and path MTU tests pass without fragmentation.
