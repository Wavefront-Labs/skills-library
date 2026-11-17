---
id: computing-software.cloud-infrastructure-engineering.azure.vpn-gateway-basic-sku-and-public-ip-migration
name: vpn-gateway-basic-sku-and-public-ip-migration
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vpn-gateway, basic-sku-migration, vpn-gateway-migration, public-ip, az-skus]
level: advanced
status: docs-checked
description: "Move VPN gateways off Basic public IPs and non-AZ SKUs: the Microsoft migration tool, SKU upgrade vs delete and recreate, downtime planning and validation."
sources: ["https://learn.microsoft.com/azure/vpn-gateway/basic-public-ip-migrate-about", "https://learn.microsoft.com/azure/vpn-gateway/gateway-sku-consolidation", "https://learn.microsoft.com/azure/vpn-gateway/gateway-sku-resize"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPN gateway Basic SKU and public IP migration

**Goal:** move VPN gateways off Basic public IPs and legacy SKUs with predictable downtime.

## What is changing
- **Basic SKU public IPs** on VpnGw1-5 and legacy gateways: use the Microsoft migration tool to move to a Standard SKU public IP. With the tool the gateway IP address does not change, up to 10 minutes of downtime is expected, and the SKU moves from VpnGw1-5 to VpnGw1AZ-5AZ. The gateway subnet needs at least three free addresses and must be /27 or larger. Timelines are on the VPN Gateway What's new page.
- **Non-AZ VpnGw1-5 SKUs**: since 1 Nov 2025 new non-AZ gateways cannot be created; from Sep 2025 to Sep 2026 existing ones can be upgraded manually to the AZ SKUs. Gateways already on a Standard public IP are upgraded to Generation 2 by Microsoft in regular service updates.
- **Basic gateway SKU** is not retiring. If it has a Basic SKU public IP reference, do not use the migration tool: remove the reference instead. A Basic SKU gateway cannot be upgraded to another SKU: delete and recreate (the public IP changes).

## Decide
| From | To | Method | Downtime |
|---|---|---|---|
| Gen1 SKU | Gen1 AZ SKU | SKU upgrade (portal, PowerShell or CLI) | About 45 minutes; none within the same tier (for example VpnGw1 to VpnGw1AZ); public IP unchanged |
| Legacy SKU (Standard, High Performance) | AZ SKU | Basic IP migration tool (migrate only) | Up to 10 minutes |
| VpnGw1-5 on a Basic public IP | Standard public IP | Migration tool | Up to 10 minutes; IP unchanged |
| Basic gateway SKU | Any other SKU | Delete and recreate | Downtime; public IP changes |

## Recreate checklist (Basic SKU)
1. Export config: connections, local network gateways, shared keys, BGP settings, P2S config and root certs.
2. Notify partners: the public IP will change, so their peer IP and firewall rules must update.
3. Delete connections, then the gateway; keep `GatewaySubnet`.
4. Create the new gateway (new gateways use a Standard SKU public IP) and recreate the connections.
5. Re-download P2S client profiles.

## Verify
- [ ] `az network vnet-gateway show --query "{sku:sku.name, ips:ipConfigurations[].publicIPAddress.id}"`.
- [ ] `az network vpn-connection show --query connectionStatus` returns `Connected` for each tunnel.
- [ ] Partner confirms SAs up with the new peer IP.

## Checked
2026-10-31. Confirmed on Microsoft Learn (Basic public IP migration about, gateway SKU consolidation, upgrade a VPN gateway SKU pages): migration tool behaviour (IP unchanged, up to 10 minutes downtime, /27 and three free IPs, VpnGw1-5 to AZ SKUs), 1 Nov 2025 creation cut-off and Sep 2025 to Sep 2026 manual upgrade window, Basic SKU not retiring and the remove-reference path, Basic SKU delete-and-recreate with changed IP, SKU upgrade table and about 45 minutes. Corrected: the old text said Basic public IPs retire 30 Sep 2025 and that the migration changes the IP; the Basic gateway SKU is not retiring. Removed: Basic SKU feature list, 30-45 minute recreate figure, zone-redundant IP advice.
Method: documentation only; no commands were run.
