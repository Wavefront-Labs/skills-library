---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-mesh-and-wireless-backhaul
name: wifi-mesh-and-wireless-backhaul
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-mesh, wireless-backhaul, point-to-point-wifi]
level: practitioner
status: draft
description: "Design mesh or wireless uplinks with a dedicated backhaul radio, hop-count limits and clear line of sight, preferring wire where possible."
sources:
  - https://www.cwnp.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mesh and wireless backhaul

- Every wireless hop on the same radio roughly halves throughput; use a dedicated backhaul radio/band (often 5 or 6 GHz) and limit to one or two hops.
- Prefer wired uplinks to as many nodes as possible ("wired mesh").
- Point-to-point links: align antennas, size Fresnel clearance, use DFS-aware channels, and set fixed channel and width.
- Mesh nodes still need PoE or local power; document both.
- IEEE 802.11s defines standard mesh; many vendors use proprietary meshing, so mixed-vendor mesh is not generally interoperable.

## Verify
- [ ] End-to-end throughput test across the longest path meets the requirement under load.
