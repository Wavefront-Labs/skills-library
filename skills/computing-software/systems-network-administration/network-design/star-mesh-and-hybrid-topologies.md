---
id: computing-software.systems-network-administration.network-design.star-mesh-and-hybrid-topologies
name: star-mesh-and-hybrid-topologies
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, star-topology, mesh-topology, hybrid-topology, partial-mesh, hub-and-spoke]
level: practitioner
status: gated
description: "Choose star, full mesh, partial mesh, ring or hybrid topologies for LAN and WAN: link counts, failure behaviour, cost, and where each fits in a real design."
sources:
  - https://www.comptia.org/certifications/network
  - https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Campus/campover.html
  - https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/WAN_and_MAN/DMVPDG.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Star, mesh and hybrid topologies

## Comparison
| Topology | Links for n nodes | Failure of one link | Typical use |
|---|---|---|---|
| Star / hub-and-spoke | n - 1 | that spoke isolated (unless dual-homed) | access switches to distribution, branches to a DC hub |
| Full mesh | n(n-1)/2 | rerouted directly | core routers (small n), dynamic spoke-to-spoke tunnels |
| Partial mesh | between | rerouted via other paths | WAN cores, regional hubs |
| Ring | n | traffic goes the other way | metro fibre, industrial |
| Bus | shared medium | segment down | legacy coax, CAN bus |

Full mesh grows quadratically: 10 sites = 45 links/tunnels; 50 sites = 1225. That is why WANs use
hubs plus dynamic spoke-to-spoke (DMVPN, SD-WAN) instead of static meshes (gated: unconfirmed, source is paywalled or blocked).

## Hybrid designs (what real networks are)
- Campus: star of access switches to a redundant pair (each access switch dual-homed = "dual star").
- Spine-leaf: every leaf to every spine (a full bipartite mesh), no leaf-leaf or spine-spine links.
- WAN: hub-and-spoke for management and DC traffic plus on-demand spoke-to-spoke tunnels.

## Choosing
1. What must survive a single link or node failure? Single-homed stars do not.
2. Traffic pattern: north-south to a DC suits a star; any-to-any suits mesh.
3. Cost of links (fibre runs, circuits) vs cost of downtime.
4. Convergence and operational complexity: rings need a ring protocol; meshes need a routing
   design that limits flooding.

## Verify
- [ ] Topology diagram marks every single point of failure and the decision to accept or remove it.

## Checked

- Date: 2026-10-28
- Confirmed: The link-count formulas and examples were checked by arithmetic: star n-1, full mesh n(n-1)/2 (10 sites = 45, 50 sites = 1225), ring n.
- Removed: ring-protocol names.
- Gated: the DMVPN and SD-WAN spoke-to-spoke statement (Cisco DMVPN page had no matching text).
Method: documentation only; no commands were run.
