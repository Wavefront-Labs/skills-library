---
id: computing-software.cloud-infrastructure-engineering.azure.disable-bgp-route-propagation-on-route-tables
name: disable-bgp-route-propagation-on-route-tables
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, udr, disable-bgp-propagation, bgp-route-propagation, route-tables, gateway-routes, effective-routes]
level: practitioner
status: gated
description: "Decide where to disable gateway (BGP) route propagation on route tables in hub-spoke designs, what it removes, and how to verify with effective routes."
sources: ["https://learn.microsoft.com/azure/virtual-network/virtual-networks-udr-overview#border-gateway-protocol", "https://learn.microsoft.com/azure/virtual-network/manage-route-table", "https://learn.microsoft.com/azure/firewall/tutorial-hybrid-portal"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disable BGP route propagation

**Goal:** subnets that must send on-prem traffic through a firewall don't learn direct
on-prem routes from the gateway, while subnets that need them still have them.

## What the setting does
Route table property `disableBgpRoutePropagation` (portal: *Propagate gateway routes = No*).
When **disabled**, subnets associated with the route table do **not** receive routes learned by
VPN/ExpressRoute gateways (BGP or static local network gateway prefixes) — including a BGP
default route. System routes (VNet, peering) and your UDRs still apply.

## Where to disable / keep
| Subnet | Propagation | Why |
|---|---|---|
| Spoke workload subnets (with firewall) | **Disable** | On-prem prefixes must go via firewall UDR |
| GatewaySubnet route table | **Keep** | Gateway needs its routes (gated: unconfirmed, source is paywalled or blocked) |
| AzureFirewallSubnet | Keep (unless forced tunnel design says otherwise) | Firewall needs on-prem routes to forward |
| Hub shared services without inspection | Keep | Direct on-prem access |

```bash
az network route-table update -g rg-net -n rt-spoke --disable-bgp-route-propagation true
```
Bicep: `properties: { disableBgpRoutePropagation: true, routes: [...] }`.

## Virtual WAN equivalent
Virtual WAN uses its own hub route tables; check the Virtual WAN routing documentation (not verified here).

## Verify with effective routes
```bash
az network nic show-effective-route-table -g rg-app -n nic-app1 -o table
```
Disabled propagation: no `VirtualNetworkGateway` source routes; only `Default` and `User` entries.
Enabled: entries with Source `VirtualNetworkGateway` for on-prem prefixes.

## Gotchas
- Disabling propagation with no UDR for on-prem prefixes = spokes lose on-prem connectivity entirely (if not covered by 0.0.0.0/0 → firewall).
- A route table setting applies to every subnet associated with it; use one table per subnet type.

## Verify
- [ ] Effective routes for a spoke NIC show on-prem prefixes only as User routes to the firewall.
- [ ] Ping/tcp to an on-prem host succeeds and appears in firewall logs.

## Checked
2026-10-28. Confirmed on the Learn UDR overview and manage-route-table pages: the portal option Propagate gateway routes and its effect on subnets connected to a VPN gateway, and the `az network route-table update` / effective-route commands (check_commands). Gated: the per-subnet recommendation table (GatewaySubnet and AzureFirewallSubnet rows) is design guidance not stated on the fetched pages. Removed: the vWAN claim, running-VM-only effective routes, minutes-to-apply timing, the App Gateway row.
Method: documentation only; no commands were run.
