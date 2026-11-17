---
id: computing-software.cloud-infrastructure-engineering.azure.expressroute-circuits-peering-and-virtual-wan
name: expressroute-circuits-peering-and-virtual-wan
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, expressroute, expressroute-circuit, private-peering, microsoft-peering, expressroute-gateway, ergw-az, global-reach, fastpath, expressroute-direct, expressroute-metro, route-filters, bgp-communities, service-key, provider-circuit, maximum-resiliency, expressroute-resiliency, virtual-wan, vwan, virtual-wan-hub, secured-virtual-hub, routing-intent, hub-routing, hybrid-connectivity, global-reach-setup]
level: advanced
status: docs-checked
description: "Design ExpressRoute: circuit SKU and Direct, private vs Microsoft peering with route filters, AZ gateways, FastPath, Global Reach, resiliency; plus Virtual WAN routing intent."
sources: ["https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction", "https://learn.microsoft.com/en-us/azure/expressroute/expressroute-faqs", "https://learn.microsoft.com/en-us/azure/expressroute/expressroute-about-virtual-network-gateways", "https://learn.microsoft.com/en-us/azure/expressroute/about-fastpath", "https://learn.microsoft.com/en-us/azure/expressroute/expressroute-routing", "https://learn.microsoft.com/en-us/azure/expressroute/expressroute-bfd", "https://learn.microsoft.com/en-us/azure/expressroute/metro", "https://learn.microsoft.com/en-us/azure/virtual-wan/hub-settings", "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ExpressRoute and Virtual WAN — private connectivity that survives a peering-location loss

**Goal:** deterministic, private bandwidth to Azure with no single circuit, provider or
gateway as a point of failure, routes you control with BGP, and a hub model that scales
to many regions.

## 1. Circuit options
| Option | Bandwidth | When |
|---|---|---|
| **Provider circuit** | 50 Mbps–10 Gbps | most enterprises; provider handles L2/L3 to the Microsoft edge |
| **ExpressRoute Direct** | 10 or 100 Gbps ports | you have gear in the peering location; carve many circuits |
| **ExpressRoute Metro** | dual-homed to two peering locations in one city | multi-site redundancy from one circuit |
| Cloud exchange / point-to-point / any-to-any (IPVPN/MPLS) | provider model | MPLS integrates with your WAN |
```bash
az network express-route create -g rg-conn -n er-lon-1 --bandwidth 1000 --peering-location "London" --provider "Equinix" --sku-family MeteredData --sku-tier Premium -l uksouth
az network express-route show -g rg-conn -n er-lon-1 --query "{key:serviceKey,state:serviceProviderProvisioningState}"   # give the service key to the provider; wait for Provisioned
```
- SKU tier: **Standard** (same geopolitical region), **Premium** add-on (global connectivity, private-peering route limit 4,000 → 10,000, up to 100 VNet links instead of 10). **Local** SKU brings data to an ExpressRoute location near the Azure region; data transfer is included in the port charge.
- Every circuit is **two connections** (primary/secondary) to two Microsoft edge routers (MSEEs); Microsoft requires dual BGP sessions, so configure both.

## 2. Peerings
```bash
az network express-route peering create -g rg-conn --circuit-name er-lon-1 --peering-type AzurePrivatePeering --peer-asn 65010 \
  --primary-peer-subnet 192.168.100.0/30 --secondary-peer-subnet 192.168.100.4/30 --vlan-id 100 [--shared-key ...]
az network express-route peering create ... --peering-type MicrosoftPeering --peer-asn 65010 --primary-peer-subnet 203.0.113.0/30 --secondary-peer-subnet 203.0.113.4/30 --vlan-id 200 \
  --advertised-public-prefixes 203.0.113.0/24 --customer-asn 65010 --routing-registry-name RIPE
az network route-filter create -g rg-conn -n rf-m365; az network route-filter rule create --filter-name rf-m365 -n allow --access Allow --communities 12076:5010 12076:5020 ...
az network express-route peering update -g rg-conn --circuit-name er-lon-1 -n MicrosoftPeering --route-filter <rf-id>
```
- **Private peering**: VNets via an ExpressRoute gateway; Azure ASN 12076; you advertise
  on-prem prefixes (max 4,000; 10,000 with Premium) and receive VNet prefixes. Never advertise a
  default route unless you intend to force-tunnel every VNet.
- **Microsoft peering**: Microsoft 365/public Azure services over the circuit using your
  registered public IPs (NAT on-prem), filtered by **route filters** with BGP communities
  per service/region (e.g. UK South regional Microsoft-peering community `12076:51024`, Storage UK South `12076:52024`; service communities such as Exchange Online `12076:5010`). Service endpoints/Private Link
  mostly remove the need; still used for M365 with Microsoft's approval and for Azure PaaS public IPs when policy demands.

## 3. Gateway, FastPath, Global Reach
```bash
az network vnet-gateway create -g rg-hub -n ergw-hub --gateway-type ExpressRoute --sku ErGw2AZ --vnet vnet-hub --public-ip-addresses pip-ergw   # zone-redundant AZ SKUs; ErGwScale for a scalable gateway
az network vpn-connection create -g rg-hub -n er-cn-lon1 --vnet-gateway1 ergw-hub --express-route-circuit2 er-lon-1 --express-route-gateway-bypass true   # FastPath
az network express-route peering connection create -g rg-conn --circuit-name er-lon-1 --peering-name AzurePrivatePeering -n gr-lon-ams \
  --peer-circuit <circuit-2-id> --address-prefix <global-reach-prefix>   # Global Reach: site-to-site via Microsoft backbone (Premium for circuits in different geopolitical regions)
```
- Gateway SKUs `ErGw1AZ/2AZ/3AZ` (1/2/10 Gbps; 4/8/16 maximum circuit connections) — the gateway, not the circuit, is often the throughput cap.
- **FastPath**: traffic bypasses the gateway data plane (gateway still needed for route exchange). Needs Ultra Performance/ErGw3AZ or ErGwScale with at least 10 scale units. VNet peering and UDRs over FastPath, and Private Link (limited GA), are ExpressRoute Direct only; ILBs and PaaS in spoke VNets, and Azure Firewall in spokes, still go through the gateway.
- Spokes via hub peering `--use-remote-gateways`; the gateway advertises each spoke's prefixes to on-prem (summarise with `summarizedGatewayPrefixes` if the advertised-prefix limit is a problem).
- **Global Reach** links two circuits so on-prem sites talk through Azure's backbone (circuits in different geopolitical regions must be Premium).
- Route Server + NVA for custom BGP injection, or Virtual WAN for a managed version of all of this.

## 4. Resiliency
- **Standard**: one circuit (two links) — a peering-location outage takes you down.
- **Maximum resiliency** (Microsoft's recommendation): two circuits in two peering locations (or Metro), both connected to the gateway; BGP AS-path prepend/local pref on-prem for primary/secondary.
- A site-to-site VPN alongside (VPN and ExpressRoute can coexist on all ER gateway SKUs; give it lower BGP preference) is a last-resort failover.
- Failover test: shut one BGP session on-prem; Azure `az network express-route list-route-tables --path primary|secondary --peering-name AzurePrivatePeering` shows routes on the other; VNet→on-prem flows continue (MSEE BGP keep-alive/hold are typically 60/180 s, so detection can take up to three minutes; enable BFD and lower your edge timers).
- Monitor: `az network express-route get-stats`, metrics `BitsInPerSecond`, `BgpAvailability`, `ArpAvailability`; **Connection Monitor** (Network Watcher) end-to-end from on-prem agent to Azure VM; alerts on `BgpAvailability < 100`.

## 5. Virtual WAN
```bash
az network vwan create -g rg-conn -n vwan-corp --type Standard
az network vhub create -g rg-conn -n vhub-uks --vwan vwan-corp --address-prefix 10.100.0.0/23 -l uksouth --sku Standard
az network vhub connection create -g rg-conn --vhub-name vhub-uks -n spoke1 --remote-vnet <spoke-vnet-id>
az network express-route gateway create -g rg-conn -n ergw-vhub --virtual-hub vhub-uks --min-val 2   # scale units; plus vpn-gateway / p2s-vpn-gateway on the hub
az network vhub routing-intent create -g rg-conn --vhub vhub-uks -n ri --routing-policies '[{"name":"InternetTraffic","destinations":["Internet"],"nextHop":"<azfw-id>"},{"name":"PrivateTraffic","destinations":["PrivateTraffic"],"nextHop":"<azfw-id>"}]'
```
- Managed hub per region with ER/VPN/P2S gateways, hub-to-hub full mesh over the
  Microsoft backbone, any-to-any routing by default, **route tables** on the hub for
  isolation (e.g. prod/non-prod), and **routing intent** to force all internet/private traffic through the hub's Azure Firewall (secured hub) or an NVA (NVA in hub, SaaS firewalls).
- Choose vWAN over hand-built hub-and-spoke when you have many regions or branches, or P2S at scale.
- Limits to remember: hub address space minimum `/24` (`/23` or larger recommended), VNet connections per hub 500 minus the number of hubs (without routing intent), 2000 VM workloads per hub by default (raise via hub infrastructure units), 10,000 routes accepted per hub.

## Gotchas
- Circuit `Provisioned` but no traffic: peering not configured on **both** links, provider VLAN mismatch, or the connection to the gateway missing — `az network express-route list-arp-tables` and `list-route-tables` per path tell you where it stops.
- Stay under the private-peering prefix limit (4,000; 10,000 with Premium) — summarise.
- A default route from on-prem over private peering overrides Azure default internet egress for every connected VNet (not just the hub) — intentional force-tunnelling only.
- Gateway in the hub + firewall: UDR on `GatewaySubnet` for spoke prefixes → firewall, and disable BGP propagation on spoke route tables, or on-prem → spoke traffic bypasses inspection (asymmetric drop).
- vWAN hub address space and any spoke/on-prem overlap = silent black-holing of the overlapping range.

## Checked
2026-10-28. Confirmed on Microsoft Learn (ExpressRoute introduction, FAQ, gateways, FastPath, routing/BGP communities, BFD, Metro, Virtual WAN hub settings, subscription limits) and the az network express-route peering reference: provider bandwidths, Direct port speeds, Premium route/VNet limits, gateway throughput and connection limits, FastPath SKU rules, community values, BGP keep-alive/hold, metric names, vWAN hub minimum /24 and VNet connection limit. Corrected: vWAN hub minimum (was /23), VNet connections per hub (was ~1000), Storage UK South community, `peering update` flags. Removed: provider names, utilisation break-even, route-weight, guided-experience, billing/deletion and "public peering retired" claims.
Method: documentation only; no commands were run.

## Verify
- [ ] `az network express-route show --query "{prov:serviceProviderProvisioningState,state:circuitProvisioningState}"` → Provisioned/Enabled; `list-route-tables` on both paths lists on-prem and VNet prefixes.
- [ ] `BgpAvailability` and `ArpAvailability` metrics at 100 for both peers over 24 h.
- [ ] Failover drill: one circuit/link down → Connection Monitor shows only brief loss; traffic continues.
- [ ] vWAN: `az network vhub get-effective-routes --resource-type RouteTable --resource-id <defaultRouteTable>` shows spokes + on-prem via the expected next hops (firewall when routing intent is set).
