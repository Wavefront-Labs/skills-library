---
id: computing-software.cloud-infrastructure-engineering.azure.gateway-transit-and-remote-gateways
name: gateway-transit-and-remote-gateways
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, gateway-transit, allow-gateway-transit, use-remote-gateways, vnet-peering, vpn-gateway, expressroute]
level: practitioner
status: docs-checked
description: "Share a hub VPN/ExpressRoute gateway with spokes via gateway transit: flag order, route advertisement to on-prem, limits, and common failures."
sources: ["https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-peering-gateway-transit", "https://learn.microsoft.com/azure/virtual-network/virtual-network-peering-overview#gateways-and-on-premises-connectivity", "https://learn.microsoft.com/azure/expressroute/expressroute-faqs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gateway transit and remote gateways

**Goal:** spokes reach on-prem through the hub's gateway, and on-prem learns spoke prefixes,
without a gateway per spoke.

## Configure
1. Hub VNet has the VPN or ExpressRoute gateway deployed (provisioning must be complete).
2. Hub → spoke peering: `--allow-gateway-transit true`.
3. Spoke → hub peering: `--use-remote-gateways true`.
```bash
az network vnet peering update -g rg-hub --vnet-name vnet-hub -n hub-to-spoke1 --set allowGatewayTransit=true
az network vnet peering update -g rg-spoke1 --vnet-name vnet-spoke1 -n spoke1-to-hub --set useRemoteGateways=true
```

## What happens
- By default the hub and peered spoke address spaces are advertised to on-premises. To reduce the prefix count, set `summarizedGatewayPrefixes` on the gateway virtual network (ExpressRoute FAQ).
- In the portal the same peering options cover a gateway or a Route Server in the peered virtual network.

## Limits
- ExpressRoute private peering: at most 1,000 IPv4 prefixes (and 100 IPv6) are advertised from a virtual network to on-prem on one connection, and ExpressRoute accepts 4,000 prefixes from on-prem (10,000 with Premium) — many spokes need contiguous, summarisable address blocks.

## Troubleshooting
- On-prem can't reach spoke: check the routes the gateway advertises (command below) and the on-prem firewall.
```bash
az network vnet-gateway list-advertised-routes -g rg-hub -n vpngw-hub --peer 10.255.0.1 -o table
```

## Verify
- [ ] Gateway advertised routes include each spoke prefix.
- [ ] Spoke VM effective routes include on-prem prefixes (or the intended UDR to the firewall).

## Checked
2026-10-31. Confirmed on Microsoft Learn (VPN Gateway peering gateway transit, ExpressRoute FAQ): the gateway-transit and remote-gateway peering options (including route server), default advertisement of hub and spoke address spaces, `summarizedGatewayPrefixes`, ExpressRoute prefix limits (1,000 IPv4 / 100 IPv6 advertised; 4,000 accepted, 10,000 with Premium). CLI flags checked against the CLI reference. Removed: static-VPN and P2S profile claims, one-remote-gateway limit, `RemoteVnetHasNoGateways`, route propagation and global peering claims, the PowerShell advertised-routes cmdlet.
Method: documentation only; no commands were run.
