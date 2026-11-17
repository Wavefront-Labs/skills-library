---
id: computing-software.networking-hardware-and-wireless.sd-wan.sdwan-topology-hub-spoke-mesh
name: sdwan-topology-hub-spoke-mesh
category: computing-software
field: networking-hardware-and-wireless
product: sd-wan
tags: [sdwan-topology, hub-and-spoke-vs-mesh, regional-hubs, sdwan-topology]
level: practitioner
status: draft
description: "Pick topology per traffic pattern: hub-and-spoke for data-centre-centric, dynamic full mesh for site-to-site, regional hubs at scale."
sources:
  - https://www.cisco.com/
  - https://www.mef.net/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Topology

- Hub-and-spoke: simple policy, central inspection; adds latency for spoke-to-spoke.
- Full or on-demand mesh: direct spoke-to-spoke tunnels when traffic exists (dynamic tunnels); scales better than static full mesh.
- Regional hubs: reduce latency across continents; plan hub capacity and failover between hubs.
- Direct internet access at branches with local breakout vs backhauling to a hub for inspection: weigh security stack placement and latency.
- Limits of tunnels per edge platform matter; check scale numbers.

## Verify
- [ ] Traceroute between two spokes follows the intended path and tunnel count is within the platform limits.
