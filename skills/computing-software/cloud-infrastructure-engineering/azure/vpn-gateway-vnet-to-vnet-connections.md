---
id: computing-software.cloud-infrastructure-engineering.azure.vpn-gateway-vnet-to-vnet-connections
name: vpn-gateway-vnet-to-vnet-connections
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vpn-gateway, vnet-to-vnet, vnet2vnet, ipsec, cross-subscription, cross-region, bgp, vnet-peering-alternative]
level: practitioner
status: docs-checked
description: "Connect two VNets with VPN gateways (VNet-to-VNet): same or different subscription and tenant, BGP, address-space behaviour, and when peering or site-to-site fits better."
sources: ["https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-howto-vnet-vnet-resource-manager-portal", "https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-vnet-vnet-rm-ps", "https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-bgp-resource-manager-ps", "https://learn.microsoft.com/en-us/cli/azure/network/vpn-connection"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VPN Gateway VNet-to-VNet connections

**Goal:** an IPsec/IKE tunnel between two Azure VNets through their VPN gateways.

## 1. Choosing
- VNet-to-VNet works like a site-to-site IPsec connection, but the local network gateway address space is created and populated automatically and is not visible, so you can't edit it. If one VNet's address space changes, the other routes to the update automatically.
- If you want extra address spaces on the local network gateway, or plan to add connections later and need to adjust it, build it with the site-to-site steps instead (create local network gateways manually; address space changes then need manual updates).
- VNet peering uses no VPN gateway and has different constraints and pricing; the PowerShell article points to it as an alternative.
- The connection doesn't include the point-to-site client pool address space. For P2S transit between the VNets use a site-to-site connection between the gateways, or peering.
- Address ranges of the VNets (and any local networks) must not overlap, or the connection won't work properly.

## 2. Build
Both VNets need a `GatewaySubnet` (/27 or larger recommended) and a route-based VPN gateway; AZ SKUs are recommended. No NSG on the gateway subnet: it is not supported and can stop the gateway working. A gateway can take 45 minutes or more to create.
```bash
az network vnet-gateway create -g rg-a -n vgw-a --vnet vnet-a --public-ip-addresses pip-vgw-a --gateway-type Vpn --vpn-type RouteBased --sku VpnGw2AZ --asn 65010 --no-wait
az network vnet-gateway create -g rg-b -n vgw-b --vnet vnet-b --public-ip-addresses pip-vgw-b --gateway-type Vpn --vpn-type RouteBased --sku VpnGw2AZ --asn 65020 --no-wait
# one connection per direction, same shared key; add --enable-bgp on both when using BGP
az network vpn-connection create -g rg-a -n cn-a-to-b --vnet-gateway1 vgw-a --vnet-gateway2 <vgw-b-resource-id> --shared-key <key> --enable-bgp
az network vpn-connection create -g rg-b -n cn-b-to-a --vnet-gateway1 vgw-b --vnet-gateway2 <vgw-a-resource-id> --shared-key <key> --enable-bgp
```
`--vnet-gateway2` is documented as the destination gateway for a `Vnet2Vnet` connection. The BGP article's CLI section creates both directions the same way, with `--enable-bgp`, `--shared-key` and full resource IDs.
- A bidirectional link is two separate connection resources. The portal's "Establish bidirectional connectivity" creates both; if you skip it, a reverse connection must be created from the other gateway later.
- The shared key must be exactly the same on both connections.
- The portal sets IKE protocol IKEv2 in its example.

## 3. Different subscriptions and tenants
- The portal connects only VNets in the same subscription (different resource groups and regions are fine). Use PowerShell or CLI across subscriptions.
- The PowerShell article covers different subscriptions in the same tenant and also different tenants; the subscriptions don't need to be in the same tenant. It uses `New-AzVirtualNetworkGatewayConnection ... -ConnectionType Vnet2Vnet` in separate sessions per subscription, with the other gateway built as an object from its ID, and `Connect-AzAccount -TenantID` for each tenant before its commands. The cross-tenant PowerShell steps were read but not run.

## 4. BGP
- Use a route-based gateway; BGP is not supported on policy-based gateways or the Basic SKU.
- Use different ASNs for connected BGP peers. The default 65515 is reserved by Azure; the article's examples use 65010 and 65020. Don't use ASNs reserved by Azure or IANA.
- Enable BGP on both connections. Without BGP, routing is limited to the two connected VNets and gives no transit to a third network such as an on-premises site connected to one of them.
- Azure assigns one BGP peer IP from GatewaySubnet to an active-standby gateway and two to an active-active one.

## Gotchas
- A gateway's public IP changes only when the gateway is deleted and re-created, not on resize, reset or maintenance.
- Peering a spoke to the hub gateway side: see the peering and S2S skills for gateway transit settings.

## Verify
- [ ] In the portal, gateway, Connections: Status shows Connected; opening a connection shows Data in and Data out once traffic flows.
- [ ] With BGP, `az network vnet-gateway list-bgp-peer-status -g rg-a -n vgw-a` shows the peer and `list-learned-routes` shows the other VNet's prefixes.

## Checked

2026-11-07. Read in full: the VNet-to-VNet portal article, the PowerShell article (same-subscription, cross-subscription and cross-tenant sections), and the BGP article (prerequisites, considerations and the VNet-to-VNet parts). The `az network vpn-connection` reference was searched for `--vnet-gateway2`, `--enable-bgp` and `--shared-key`, not read end to end. Commands were not run.
Corrected: the cross-tenant recipe is wrong in the old draft. The PowerShell article supports cross-tenant `Vnet2Vnet` connections directly; the local-network-gateway workaround is removed. Removed: peering-vs-encryption advice (virtual network encryption), "ideally AZ" aside beyond the portal text, throughput and address-space-update gotchas, `shared-key reset` advice, `connectionStatus` and `test-connectivity` verify steps, the claim that the peer's address space is learned from the gateway, and the 30 to 45 minute figure (the articles say 45 minutes or more). Added the NSG restriction, P2S pool note and local-network-gateway visibility.

Method: documentation only; no commands were run.
