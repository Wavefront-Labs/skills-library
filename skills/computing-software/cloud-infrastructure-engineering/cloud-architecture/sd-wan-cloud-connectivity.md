---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.sd-wan-cloud-connectivity
name: sd-wan-cloud-connectivity
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, network-topology, sd-wan, branch-connectivity, virtual-wan, cloud-wan, network-virtual-appliance]
level: practitioner
status: draft
description: "Connect branches to cloud with SD-WAN: cloud hub integration (Virtual WAN, Cloud WAN, NCC), NVA placement, routing, local breakout, segmentation and resilience."
sources: ["https://learn.microsoft.com/azure/virtual-wan/sd-wan-connectivity-architecture", "https://docs.aws.amazon.com/network-manager/latest/cloudwan/what-is-cloudwan.html", "https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SD-WAN and branch connectivity to cloud

## Steps
1. **Choose the integration model**:
   - SD-WAN virtual appliances in a cloud hub (Azure Virtual WAN partner NVA in the hub, AWS
     Transit Gateway Connect with GRE + BGP, Google NCC router appliance spokes).
   - IPsec from SD-WAN edges to native VPN gateways (simpler, lower throughput per tunnel).
   - Provider backbone as the WAN (Virtual WAN any-to-any, Cloud WAN global network).
2. **Place cloud hubs** in the regions nearest branch clusters; dual appliances per hub.
3. **Routing**: BGP between SD-WAN and cloud routers; summarise branch prefixes; watch route
   limits (e.g. TGW and Virtual WAN route-table caps); avoid asymmetric paths through firewalls.
4. **Local internet breakout** for SaaS (Microsoft 365, etc.) at the branch with SSE/SASE
   inspection instead of backhauling to a hub.
5. **Segmentation**: map SD-WAN segments/VRFs to cloud route tables or segments (Cloud WAN
   segments, Virtual WAN custom route tables).
6. **Resilience**: dual WAN links per branch, dual tunnels per hub, application-aware path
   selection; test link failover.

## Gotchas
- GRE/IPsec tunnel throughput limits per tunnel; use ECMP across tunnels.
- Overlapping branch IP ranges block clean routing; fix IPAM first.

## Verify
- [ ] BGP sessions redundant; failover test results recorded.
- [ ] SaaS breakout and segmentation verified per branch type.
