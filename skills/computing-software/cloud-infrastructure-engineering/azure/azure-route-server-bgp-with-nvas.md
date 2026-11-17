---
id: computing-software.cloud-infrastructure-engineering.azure.azure-route-server-bgp-with-nvas
name: azure-route-server-bgp-with-nvas
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, route-server, azure-route-server, bgp, nva, branch-to-branch, sd-wan]
level: advanced
status: docs-checked
description: "Deploy Azure Route Server so NVAs (SD-WAN, firewalls) exchange routes with the VNet via BGP: subnet, peering setup, branch-to-branch, route limits and failure modes."
sources: ["https://learn.microsoft.com/azure/route-server/overview", "https://learn.microsoft.com/azure/route-server/quickstart-create-route-server-cli", "https://learn.microsoft.com/azure/route-server/route-server-faq", "https://learn.microsoft.com/azure/route-server/expressroute-vpn-support", "https://learn.microsoft.com/en-us/cli/azure/network/routeserver"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Azure Route Server

**Goal:** an NVA's routes are programmed into the VNet (and peered spokes) dynamically via BGP,
so you do not maintain UDRs for them.

## Deploy
```bash
az group create --name 'myResourceGroup' --location 'eastus'
az network vnet create --resource-group 'myResourceGroup' --name 'myVirtualNetwork' --subnet-name 'RouteServerSubnet' --subnet-prefixes '10.0.1.0/26'
subnetId=$(az network vnet subnet show --name 'RouteServerSubnet' --resource-group 'myResourceGroup' --vnet-name 'myVirtualNetwork' --query id -o tsv)
az network public-ip create --resource-group 'myResourceGroup' --name 'RouteServerIP' --sku Standard --version 'IPv4'
az network routeserver create --name 'myRouteServer' --resource-group 'myResourceGroup' --hosted-subnet $subnetId --public-ip-address 'RouteServerIP'
az network routeserver peering create --name 'myNVA' --peer-ip '10.0.0.4' --peer-asn '65001' --routeserver 'myRouteServer' --resource-group 'myResourceGroup'
az network routeserver show --resource-group 'myResourceGroup' --name 'myRouteServer'
```
The quickstart says creation can take up to 30 minutes. `show` returns `virtualRouterAsn` (65515 in the quickstart output) and
`virtualRouterIps` (two IPs). Peer the NVA with **both** IPs: the FAQ says each NVA must peer with both Route Server instances and
advertise the same routes to both. The NVA must support multi-hop eBGP and its ASN must differ from the Route Server's. The peer
name is only an identifier. Route Server needs a Standard public IP for its management connectivity.

## Behaviour
- Routes learned from NVAs are programmed into the route tables of VMs in the VNet and in peered VNets. For a peered spoke, enable
  *Use the remote virtual network's gateway or Route Server* on the spoke's peering.
- Route Server advertises the VNet prefixes (and peered VNet address spaces) to the NVAs.
- Not in the data path: traffic goes directly between the VM and the NVA.
- Same prefix from several NVAs with the same AS-path length: Route Server programs multiple next hops (ECMP). If one NVA sends a
  shorter AS path, only its route is programmed. A route whose AS_PATH already contains 65515 is rejected (loop prevention).
- AS path and BGP communities are propagated intact. Keepalive timer is 60 seconds and hold timer 180 seconds. Only 16-bit ASNs are supported.
- ASNs reserved by Azure (cannot be used on the NVA) include 8074, 8075, 12076, 65515, 65517, 65518, 65519 and 65520.
- A virtual network peering created between hub and spoke triggers a BGP soft reset (route refresh); an NVA without route-refresh
  support gets a hard reset, which may disrupt traffic through it.
- No IPv6 support: deploying Route Server in a VNet that has an IPv6 address space breaks its IPv6 traffic.

## Branch-to-branch (with VPN/ExpressRoute gateways)
`az network routeserver update --resource-group myResourceGroup --name myRouteServer --allow-b2b-traffic true` makes Route
Server exchange routes between NVAs and the ExpressRoute/VPN gateways (off by default). Requirements and limits from the docs:
- Gateways must be in the same VNet as Route Server. A VPN gateway must be active-active with ASN 65515 (BGP on the VPN gateway is not required).
- Transit is only ExpressRoute to site-to-site VPN, not point-to-site; ExpressRoute circuit-to-circuit is not supported.
- Creating or deleting a Route Server in a VNet with a gateway causes downtime (FAQ: about 10 minutes; deployment may take 30-60 minutes).
- Routes advertised from VNet address space and Route Server toward an ExpressRoute circuit must not exceed 1,000 with branch-to-branch on.
- Avoid the Azure reserved community 65517:65517 on routes from on-premises.
- NVA-advertised routes are not passed from one Route Server to another through an ExpressRoute MSEE.

## Limits / gotchas
- Limits per deployment (overview and FAQ): 16 BGP peers; each peer may advertise 4,000 routes (the count is current routes plus
  routes in the incoming update, and over the limit the BGP session is dropped); 50,000 VMs; 500 VNets; 10,000 total prefixes.
- Default capacity is two routing infrastructure units, supporting 4,000 connected VMs; add units in increments of 1,000 VMs.
- Advertising 0.0.0.0/0 from an NVA sends internet-bound traffic via that NVA (overview example) - only with intent.
- System routes for the VNet, peerings and service endpoints win over BGP routes even when the BGP route is more specific, so
  Route Server cannot steer intra-VNet subnet traffic; keep UDRs (or an HA-ports load balancer) for that.
- `RouteServerSubnet` is a dedicated subnet of at least /26 (quickstart); no UDR and no NSG on it. Only one Route Server per VNet.
- A spoke VNet connected to a Virtual WAN hub cannot have a Route Server.
- When the same prefix is learned over ExpressRoute, VPN and SD-WAN, ExpressRoute wins by default; `--hub-routing-preference`
  accepts `ASPath`, `ExpressRoute` or `VpnGateway`.

## Verify
- [ ] `az network routeserver peering list-learned-routes -g MyResourceGroup --routeserver MyRouteServer -n MyRouteServerPeer` lists the NVA prefixes.
- [ ] `az network routeserver show` reports `provisioningState` Succeeded.

## Checked

2026-11-07. Re-read in full: Route Server overview, FAQ, ExpressRoute and VPN support, CLI quickstart. For the `az network routeserver`
CLI reference (35k characters) I only read the filtered lines for create, update, peering create and list-learned-routes (flags, enums, examples), not the whole page.
- Corrected: subnet size is /26 minimum (was /27); deploy commands now follow the quickstart (`vnet create --subnet-prefixes`), dropping `vnet subnet create` and `--query` form that no page showed.
- Trimmed: the "multi-hop eBGP only" note kept; the "vWAN use hub BGP peering instead" advice (pages only say a Route Server can't be in a Virtual WAN-connected spoke); the invented Verify steps (effective-route source, withdrawal timing).
- Added from the pages: limits table, reserved ASNs, timers, branch-to-branch conditions.
- Not read: the linked Troubleshoot, route maps and routing preference pages.

Method: documentation only; no commands were run.
