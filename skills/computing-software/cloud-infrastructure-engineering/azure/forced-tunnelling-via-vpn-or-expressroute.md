---
id: computing-software.cloud-infrastructure-engineering.azure.forced-tunnelling-via-vpn-or-expressroute
name: forced-tunnelling-via-vpn-or-expressroute
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, forced-tunnelling, forced-tunneling, default-route-advertisement, expressroute, vpn-gateway, azure-firewall-management-nic]
level: advanced
status: docs-checked
description: "Send Azure internet egress back on-prem: BGP 0.0.0.0/0 over ExpressRoute/VPN, default site on route-based VPN, Azure Firewall management NIC, and services that break."
sources: ["https://learn.microsoft.com/azure/vpn-gateway/site-to-site-tunneling", "https://learn.microsoft.com/azure/firewall/forced-tunneling", "https://learn.microsoft.com/azure/expressroute/expressroute-routing#advertising-default-routes", "https://learn.microsoft.com/en-us/azure/firewall/management-nic", "https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-forced-tunneling-rm", "https://learn.microsoft.com/en-us/cli/azure/network/vnet-gateway"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Forced tunnelling via VPN or ExpressRoute

**Goal:** internet-bound traffic from Azure exits through on-prem inspection (firewall, proxy) when policy demands, without
breaking Azure platform dependencies.

## Methods
1. **BGP**: advertise `0.0.0.0/0` from on-premises over a VPN gateway S2S tunnel (BGP) or, for ExpressRoute, over **private peering
   only** (default routes on Microsoft peering must be filtered out). Advertising a default route into private peering blocks the
   internet path from Azure: your corporate edge must route to and from the internet.
2. **Default Site** on a route-based VPN gateway, no BGP needed: assign a local network gateway as the Default Site. The page does
   it in PowerShell (`Set-AzVirtualNetworkGatewayDefaultSite`; it cannot be set in the portal). The CLI reference also lists
   `az network vnet-gateway update --gateway-default-site <local-network-gateway>`. The on-premises VPN device must use `0.0.0.0/0`
   as traffic selectors. Without a Default Site (or BGP default route), internet traffic goes direct for all subnets.
3. **Exceptions per subnet**: with either VPN method, a UDR `0.0.0.0/0` with next hop type `Internet` on a subnet (the page does
   Frontend) sends that subnet's internet traffic straight out instead of on-prem.

## Azure Firewall with forced tunnelling
- Needs the **Management NIC**: management traffic uses `AzureFirewallManagementSubnet` (minimum /26) and its own public IP.
  Standard and Premium firewalls must enable it at creation, or an existing firewall must be stopped (deallocated) and started
  again with the management subnet and IP (the private IP may change); Basic firewalls and secured-hub firewalls always have it.
- The management subnet gets a system route table whose only route is a default route to the Internet, with *Propagate gateway
  routes* disabled. Avoid attaching your own route table; if you must, keep a default route to the Internet.
- On `AzureFirewallSubnet`, add a default route with the VPN gateway (or an NVA) as next hop, or enable *Propagate gateway routes*
  to learn the on-prem routes via BGP.
- Internet-bound traffic is SNATed to a firewall private IP in AzureFirewallSubnet, hiding the source from the on-prem
  firewall. Adding `0.0.0.0/0` as a private IP range turns SNAT off for all destinations (the firewall can then never egress directly).
- Split tunnelling: route tables on AzureFirewallSubnet can send selected traffic (the page's example is KMS activation) to the Internet.

## What breaks
- Advertising a default route over ExpressRoute breaks Windows and other VM licence (KMS) activation; Microsoft documents a UDR
  workaround ("use user defined routes to enable KMS activation").
- DNAT is not supported on a firewall with forced tunnelling (asymmetric routing), except firewalls with a Management NIC.
- Bastion IP-based connection does not work with forced tunnelling or a default route over ExpressRoute (Bastion needs internet access).

## Verify
- [ ] Gateway or subnet effective routes show `0.0.0.0/0` pointing where you designed (gateway, firewall or Internet for exceptions).
- [ ] A VM's internet-bound traffic is seen by the on-prem inspection device, and activation workarounds are in place.

## Checked

2026-11-07. Re-read in full: S2S forced tunneling (Default Site) article, About forced tunneling for S2S, Azure Firewall forced tunneling,
Azure Firewall Management NIC. From the ExpressRoute routing page I read only the "Advertising default routes" section (page is 19k characters).
In the `az network vnet-gateway` reference I only checked that `update` lists `--gateway-default-site`.
- Removed (no page states them): the table of App Gateway v2, SQL MI, APIM and ASE routing, private-endpoint hairpin advice, "UDR to VirtualNetworkGateway only works with default site", the claim that disabling propagation removes all BGP routes, the `curl ifconfig.me` verification, "Firewall SNATs private traffic per config".
- Corrected: firewall route-table detail now follows the Management NIC page.
- Added: the Bastion IP-connect limitation (Bastion IP-based connection page, read this batch).

Method: documentation only; no commands were run.
