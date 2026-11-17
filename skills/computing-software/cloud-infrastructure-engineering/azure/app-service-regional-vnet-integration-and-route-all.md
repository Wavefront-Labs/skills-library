---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-regional-vnet-integration-and-route-all
name: app-service-regional-vnet-integration-and-route-all
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service-networking, vnet-integration, regional-vnet-integration, route-all, vnet-route-all, outbound-traffic]
level: practitioner
status: docs-checked
description: "Integrate App Service and Functions with a VNet for outbound traffic: delegated subnet sizing, route-all, DNS for private endpoints, NSG/UDR behaviour and troubleshooting."
sources: ["https://learn.microsoft.com/azure/app-service/overview-vnet-integration", "https://learn.microsoft.com/azure/app-service/configure-vnet-integration-enable", "https://learn.microsoft.com/azure/app-service/configure-vnet-integration-routing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Service regional VNet integration and route-all

**Goal:** the app's **outbound** calls reach private endpoints, on-prem and peered VNets, and
optionally all egress goes through the hub firewall.

## Subnet
- Dedicated subnet delegated to `Microsoft.Web/serverFarms`; multi-plan subnet join lets several plans in one subscription share a subnet (minimum /26).
- Size: each plan instance uses an IP, and platform upgrades need extra IPs, so allocate double your planned maximum scale. A **/26** (64 addresses) covers the maximum scale of one multitenant plan; the portal requires at least /27 when it creates the subnet, and a pre-existing /28 can be used.
- Subnet size can't be changed while in use — plan for maximum scale.

## Enable
```bash
az network vnet subnet create -g rg-net --vnet-name vnet-spoke -n snet-app-int --address-prefixes 10.20.4.0/26 --delegations Microsoft.Web/serverFarms
az webapp vnet-integration add -g rg -n app-orders --vnet <vnet-id> --subnet snet-app-int
az webapp config set -g rg -n app-orders --vnet-route-all-enabled true
```
Route-all (`outboundVnetRouting.allTraffic`; the older `vnetRouteAllEnabled` property is the legacy form) sends **all**
outbound traffic into the VNet, so NSGs and UDRs (e.g. 0.0.0.0/0 → firewall) apply. Without it,
only RFC1918 destinations go through the VNet. `outboundVnetRouting.allTraffic` also covers configuration traffic (image pulls, content share, backup, managed identity token requests); `outboundVnetRouting.applicationTraffic` routes only application traffic.

## DNS
The app uses the VNet's DNS servers when integrated. For private endpoints, the VNet must
resolve `privatelink.*` zones (linked private DNS zones or custom DNS forwarding to 168.63.129.16 / Private Resolver).
Override per app with the `dnsConfiguration.dnsServers` site property (up to five servers); the `WEBSITE_DNS_SERVER` app setting still works.

## What it does not do
- Not inbound: use private endpoints or access restrictions for inbound.
- Doesn't give a stable outbound IP by itself; add a **NAT gateway** on the integration subnet (with route-all) for a static egress IP.

## Troubleshooting
Kudu console (SSH/PowerShell):
```bash
tcpping sql-orders.database.windows.net:1433
nameresolver sql-orders.database.windows.net     # should return 10.x private IP
```
Common failures: private DNS zone not linked to the integration VNet; UDR to firewall without firewall rules for the app's dependencies (Key Vault, Storage, Entra login endpoints); NSG on the integration subnet blocking outbound 443.

## Gotchas
- VNet integration requires a Basic, Standard, Premium v2/v3/v4 or Elastic Premium plan; Free and Shared don't support it.

## Verify
- [ ] `az webapp show -g rg -n app-orders --query "{subnet:virtualNetworkSubnetId, routeAll:vnetRouteAllEnabled}"`.
- [ ] `nameresolver` returns private IPs for private-endpoint dependencies; firewall logs show the app's egress when route-all is on.

## Checked
2026-10-27. Confirmed on Microsoft Learn: overview-vnet-integration (/26 covers maximum scale, double the IPs, /27 portal minimum, /28 existing subnet,
multi-plan subnet join /26, pricing tiers that support it, dnsConfiguration.dnsServers up to five, WEBSITE_DNS_SERVER still usable),
configure-vnet-integration-routing (outboundVnetRouting.allTraffic and applicationTraffic and what each covers), and the CLI reference for
`az webapp vnet-integration` and `az webapp config` (--vnet-route-all-enabled).
Removed: `imagePullTraffic`/`contentShareTraffic` property names, "/27 is the floor", the Hybrid Connections and Functions Consumption statements.

Method: documentation only; no commands were run.
