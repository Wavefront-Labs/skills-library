---
id: computing-software.cloud-infrastructure-engineering.azure.azure-vnet-design
name: azure-vnet-design
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vnet, virtual-network, vnet-design, subnets, address-space, ipam, subnet-delegation, nsg, network-security-groups, application-security-groups, service-tags, user-defined-routes, udr, route-tables, azure-firewall, nat-gateway, default-outbound-access, private-endpoints, private-dns-zones, service-endpoints, vnet-peering, hub-and-spoke, virtual-wan, network-watcher, vnet-flow-logs, bastion]
level: practitioner
status: draft
description: "Design Azure VNets: address and subnet sizing incl. delegated subnets, NSG/ASG rules, UDRs to a firewall, NAT Gateway egress, Private Endpoints with private DNS, and peering rules."
sources: ["Microsoft Learn - Plan virtual networks", "Microsoft Learn - Network security groups and application security groups", "Microsoft Learn - Virtual network traffic routing", "Microsoft Learn - Default outbound access in Azure", "Microsoft Learn - Azure Private Endpoint DNS configuration", "Microsoft Learn - Hub-spoke network topology in Azure"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Azure VNet design — subnets, routes, egress and private DNS that hold up

**Goal:** a spoke VNet whose subnets fit the services that will land in them, whose
traffic goes where you think it goes (and you can prove it), and whose PaaS
dependencies resolve to private IPs. Landing-zone topology choice is in
`computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-account-landing-zone`.

## 1. Address space and subnets
- Allocate VNet ranges centrally (Azure Virtual Network Manager **IPAM** pools, or a
  spreadsheet of record) — peered VNets cannot overlap.
- Azure reserves **5 IPs per subnet** (first four and last). Smallest usable subnet /29.
- VNets are regional and span all AZs; subnets are not zonal — zone resilience comes
  from the resources, not the subnet layout (unlike AWS).
- Reserved/required subnet names and sizes (check current docs, they change):
  `GatewaySubnet` (/27 or larger), `AzureFirewallSubnet` (/26), `AzureBastionSubnet` (/26),
  `RouteServerSubnet` (/27).
- **Delegated subnets** are dedicated to one service: App Service/Functions VNet
  integration, Container Apps environments (workload profiles need at least /27; consumption-only
  needed /23), API Management, SQL Managed Instance, Azure NetApp Files. Size them for
  scale-out — e.g. App Service integration consumes one IP per instance, plus overhead during scale.
- AKS with Azure CNI Overlay keeps pod IPs out of the VNet; flat Azure CNI needs a large subnet.

## 2. NSGs and ASGs
- NSG per subnet (and optionally per NIC; both are evaluated). Priority 100-4096, lower wins.
- Use **service tags** (`AzureLoadBalancer`, `Storage.WestEurope`, `AzureMonitor`) instead
  of IP lists; use **application security groups** to write `web-asg → app-asg:8443`
  instead of IP ranges.
- Default rules allow all intra-VNet traffic (including from peered VNets via the
  `VirtualNetwork` tag). Add an explicit deny-all at e.g. priority 4000 if you want
  east-west segmentation, keeping `AzureLoadBalancer` probes allowed above it.

## 3. Routing with UDRs
- Hub-and-spoke with Azure Firewall/NVA: route table on spoke subnets with
  `0.0.0.0/0 → VirtualAppliance <firewall private IP>`, and routes for other spokes' ranges.
- Set `disableBgpRoutePropagation` on spoke route tables when the hub has an ExpressRoute/VPN
  gateway, otherwise on-prem routes learned via BGP bypass the firewall.
- Return path: the firewall subnet must route back symmetrically — asymmetric routing
  through a stateful NVA drops sessions.
- Check effective routes: `az network nic show-effective-route-table -g <RG> -n <NIC>`.

## 4. Egress
- **Default outbound access** (implicit SNAT IP) is retired for new VNets created after
  the September 2025 cut-over — new subnets are private by default. Provide explicit egress:
  **NAT Gateway** on the subnet (static IPs, 64k SNAT ports per IP, best for SNAT-heavy apps),
  or the firewall via UDR, or a Standard LB outbound rule.
- NAT Gateway is zonal; for zone resilience the current guidance is a zone-redundant
  NAT Gateway SKU (Standard V2) where available — verify availability in your region.

## 5. Private Endpoints and DNS
- Private Endpoint = a NIC in your subnet for one PaaS sub-resource (`blob`, `file`,
  `vault`, `sqlServer`). Disable public network access on the resource afterwards.
- DNS is the hard part: create **private DNS zones** (`privatelink.blob.core.windows.net`,
  …) **once, centrally** in the hub, linked to every VNet that resolves them; attach PE
  records via a DNS zone group (or a DINE policy that does it). On-prem resolves via
  **Azure DNS Private Resolver** inbound endpoint.
- Service endpoints are the older, cheaper option (traffic stays on backbone, resource
  keeps its public IP); use for storage when Private Endpoint cost or limits bite.

## 6. Peering
Peering is non-transitive. Spoke-to-spoke goes via the hub firewall (UDRs) or Virtual
Network Manager connectivity configurations. Set `allowForwardedTraffic` on the spoke
side and `useRemoteGateways`/`allowGatewayTransit` to share a hub VPN/ER gateway.

## Gotchas
- Duplicate private DNS zones per spoke → split-brain resolution; one central zone set only.
- A subnet with resources cannot change delegation; resizing a subnet in use is possible
  only if no resources conflict — plan size up front.
- NSG flow logs are being retired in favour of **VNet flow logs**; build on the latter.
- Basic SKU public IPs and Basic Load Balancer are retired (Sept 2025); use Standard.

## Verify
- [ ] VNet range recorded centrally and non-overlapping with all peers and on-prem.
- [ ] Every subnet has an NSG; delegated subnets sized for max scale-out.
- [ ] `show-effective-route-table` on a spoke NIC shows 0.0.0.0/0 to the firewall and no BGP bypass.
- [ ] Each subnet has explicit egress (NAT GW / firewall); none rely on default outbound access.
- [ ] `nslookup <account>.blob.core.windows.net` from the spoke returns a private IP; public network access disabled.
- [ ] VNet flow logs and Traffic Analytics enabled; Network Watcher connection troubleshoot confirms intended paths.
