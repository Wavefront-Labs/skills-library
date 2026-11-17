---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-carrier-selection
name: cloud-carrier-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, ecosystem-roles, cloud-carrier, colocation, network-carrier, direct-connect, expressroute, interconnect]
level: practitioner
status: draft
description: "Select network carriers and colocation for private cloud connectivity: on-ramp locations, diverse paths, port speeds, SLAs, MACsec and contract terms."
sources: ["https://csrc.nist.gov/pubs/sp/500/292/final", "https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html", "https://learn.microsoft.com/azure/expressroute/expressroute-locations", "https://cloud.google.com/network-connectivity/docs/interconnect/concepts/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network carrier and colocation selection

## Context
NIST SP 500-292 names the cloud carrier as the actor providing connectivity and transport
between consumers and providers. In practice: the carrier or exchange that gets you from your
sites to Direct Connect / ExpressRoute / Cloud Interconnect locations.

## Steps
1. **List required on-ramps**: provider edge locations near your data centres and target
   regions (each provider publishes its location list). Prefer colos that host on-ramps for
   all providers you use.
2. **Dedicated vs hosted/partner**: dedicated ports (1/10/100 Gbps) in a colo where you have
   a cage; partner/hosted connections via a carrier or fabric (Equinix Fabric, Megaport) when
   you lack presence or need sub-1 Gbps.
3. **Resilience**: two locations, two devices, two carriers with diverse physical paths; ask
   for route diversity evidence (fibre maps / KMZ). Providers' maximum-resiliency models need
   separate locations.
4. **Security**: MACsec where supported on dedicated ports, or IPsec over the private link.
5. **Contract terms**: SLA and service credits, mean time to repair, cross-connect lead times,
   term and price per Mbps, egress pricing over private links vs internet.
6. **Test failover** by disabling one circuit and watching BGP converge.

## Gotchas
- Two carriers sharing the same duct or building entry is one failure domain.
- Cross-connect orders in colos often take weeks; plan the critical path.

## Verify
- [ ] Physical path diversity documented.
- [ ] Failover test completed with measured convergence time.
