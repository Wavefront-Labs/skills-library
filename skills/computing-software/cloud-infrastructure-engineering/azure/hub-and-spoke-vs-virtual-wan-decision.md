---
id: computing-software.cloud-infrastructure-engineering.azure.hub-and-spoke-vs-virtual-wan-decision
name: hub-and-spoke-vs-virtual-wan-decision
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, hub-and-spoke, hub-spoke-design, topology-choice, virtual-wan, vwan, network-topology]
level: advanced
status: docs-checked
description: "Choose between customer-managed hub-and-spoke VNets and Azure Virtual WAN using CAF criteria: scale, branches, routing control, NVAs, cost and operational model."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/define-an-azure-network-topology", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/virtual-wan-network-topology", "https://learn.microsoft.com/azure/virtual-wan/virtual-wan-about"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hub-and-spoke vs Virtual WAN

**Goal:** pick the topology once, with documented reasons, because migrating later is a
multi-month project.

## Decision table
| Criterion | Hub-and-spoke (VNet hub) | Virtual WAN |
|---|---|---|
| Regions | Few | Many regions, global transit |
| Branches (S2S/SD-WAN) | Fewer | Many; integrated SD-WAN partners |
| Routing control | Full (UDRs, Route Server, any NVA design) | Managed routing, less granular |
| Operations | You manage routes, gateways, peering | Microsoft-managed hub |
| Cost | Pay per component | Hub and data-processing fees; see the pricing page |
| Limits to watch | Peering and route-table limits (Azure limits page) | Virtual WAN limits |

## Rules of thumb (CAF)
- Choose **Virtual WAN** for global, branch-heavy estates, many regions with full-mesh needs, or when the team wants managed routing.
- Choose **hub-and-spoke** when you need custom routing, unsupported NVAs, fine-grained control, or few regions; it's also easier to understand for small teams.
- Both are supported by the ALZ accelerator (choose at Phase 0).

## Questions to ask
1. How many regions in 3 years? How many branch sites?
2. Do we need non-partner NVAs in the transit path?
3. Is east-west inspection mandatory, and at what throughput?
4. Does the team have BGP/UDR expertise for 24/7 ops?
5. ExpressRoute Global Reach vs vWAN transit for site-to-site via Azure?

## Migration note
Hub-and-spoke → vWAN: build vWAN hubs in parallel, move spokes connection by connection (remove
peering, add hub connection), cut gateways last. Plan IP readdressing if hub prefixes overlap
the vWAN hub ranges.

## Gotchas
- vWAN hub address space can't overlap any spoke or on-prem range; check the Virtual WAN hub docs for the required prefix size.

## Verify
- [ ] Architecture decision record lists criteria scores and the chosen topology.
- [ ] Address plan reserves hub ranges for the chosen design in every region.

## Checked
2026-10-28. Confirmed against the CAF network topology pages: the trade-off between customer-managed hub-and-spoke and Virtual WAN, and that ExpressRoute and VPN options exist in both. The remaining table rows are qualitative.
Removed (not confirmed): region and branch counts, the 500-peering and one-secured-hub limits, NVA partner rule, `connectivity_type`, /23 and /22 hub sizes, routing intent and private DNS placement claims.

Method: documentation only; no commands were run.
