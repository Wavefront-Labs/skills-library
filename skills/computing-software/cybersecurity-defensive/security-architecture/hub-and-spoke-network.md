---
id: computing-software.cybersecurity-defensive.security-architecture.hub-and-spoke-network
name: hub-and-spoke-network
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [hub-and-spoke-network, network-segmentation, azure-landing-zone, transit-gateway, vnet-peering, shared-services, cloud-network-design]
level: advanced
status: draft
description: "Design cloud hub-and-spoke segmentation: shared hub with firewall and egress, isolated spokes, route tables forcing inspection, no transitive spoke peering, and validation."
sources: ["https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke", "https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/welcome.html", "https://cloud.google.com/architecture/deploy-hub-spoke-vpc-network-topology"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud hub-and-spoke segmentation

## Shape
- **Hub:** firewall (Azure Firewall / NVA / AWS Network Firewall), egress NAT, VPN/ExpressRoute/Direct Connect gateways, DNS resolver, bastion.
- **Spokes:** one per workload/environment/team. No direct spoke-to-spoke path; all east-west traffic goes through the hub firewall.

## Azure
- VNet peering spoke<->hub with "use remote gateways" on the spoke and "allow gateway transit" on the hub.
- UDR on every spoke subnet: `0.0.0.0/0 -> VirtualAppliance <firewall private IP>` and a route for each other spoke prefix to the firewall. Disable BGP route propagation on spoke route tables so on-prem routes do not bypass the firewall.
- Or Azure Virtual WAN with routing intent (private + internet traffic to the secured hub).

## AWS
- Transit Gateway with separate route tables: spoke attachments associate to a "spoke" route table whose default route points to the inspection VPC attachment; the inspection VPC attachment has appliance mode enabled (symmetric flows across AZs).
- Do not propagate spoke routes into the spoke route table (that allows direct spoke-to-spoke).

## GCP
- Hub VPC with Network Connectivity Center or VPC peering (peering is non-transitive), or Shared VPC per environment; route through NVAs with custom static routes and tags.

## Gotchas
- Peering is non-transitive by design; that is the isolation property - do not "fix" it with full-mesh peering.
- Asymmetric routing through stateful firewalls drops traffic; use appliance mode (AWS) or ensure return UDRs (Azure).
- PaaS private endpoints in spokes need DNS via the hub resolver, and private endpoint routes can bypass UDRs unless network policies for private endpoints are enabled.

## Verify
- [ ] From spoke A, traceroute/connection test to spoke B shows the firewall hop and is subject to its rules.
- [ ] Effective routes on a spoke NIC show 0.0.0.0/0 to the firewall.
- [ ] Firewall logs show east-west flows.
