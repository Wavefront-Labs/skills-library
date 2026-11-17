---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.inter-region-connectivity
name: inter-region-connectivity
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, network-topology, inter-region-connectivity, transit-gateway-peering, global-vnet-peering, cloud-wan, virtual-wan, cross-region-routing]
level: practitioner
status: draft
description: "Connect regions for DR and multi-region apps: inter-region peering, global transit (Cloud WAN, Virtual WAN, global VPC), routing, encryption, latency and data transfer cost."
sources: ["https://docs.aws.amazon.com/vpc/latest/tgw/tgw-peering.html", "https://docs.aws.amazon.com/network-manager/latest/cloudwan/what-is-cloudwan.html", "https://learn.microsoft.com/azure/virtual-wan/virtual-wan-about", "https://cloud.google.com/vpc/docs/vpc"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inter-region connectivity

## Options
| Provider | Options |
|---|---|
| AWS | Inter-region VPC peering, Transit Gateway peering (static routes), AWS Cloud WAN (policy-based global network with dynamic routing) |
| Azure | Global VNet peering, Virtual WAN with multiple hubs (hub-to-hub automatic), hub-and-spoke per region with peered hubs |
| Google Cloud | VPC networks are global (subnets regional) - inter-region routing is native; NCC for hybrid |

## Design steps
1. Decide what must talk across regions: replication traffic, management, DR failover paths,
   service-to-service calls (minimise these; prefer region-local).
2. Non-overlapping CIDRs per region from the IP plan.
3. Choose topology: few regions -> peering of regional hubs; many regions/segments ->
   Cloud WAN / Virtual WAN with segmentation.
4. Inspection: decide whether inter-region traffic goes through firewalls (cost/latency) or relies
   on provider encryption (AWS encrypts inter-region traffic on its backbone; check each provider).
5. Routing: avoid asymmetric routes with regional firewalls; document failover routing.
6. Cost: inter-region data transfer is charged per GB both ways in many cases; estimate replication volume.

## Gotchas
- TGW peering does not propagate routes dynamically; static routes need maintenance.
- Cross-region chatty calls add tens to hundreds of ms per call.
- DR region connectivity untested until disaster.

## Verify
- [ ] Latency and throughput measured between regions.
- [ ] DR path tested with primary region isolated.
