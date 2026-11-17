---
id: computing-software.cloud-infrastructure-engineering.azure.service-tags-as-route-address-prefixes
name: service-tags-as-route-address-prefixes
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, routing, service-tag-routes, udr, route-tables, firewall-bypass]
level: practitioner
status: docs-checked
description: "Use service tags as UDR address prefixes to send specific Azure service traffic around or to a firewall: syntax, next hop types and precedence against explicit prefixes."
sources: ["https://learn.microsoft.com/azure/virtual-network/virtual-networks-udr-overview#service-tags-for-user-defined-routes", "https://learn.microsoft.com/azure/virtual-network/service-tags-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service tags as route address prefixes

**Goal:** route traffic to an Azure service by tag (self-updating), instead of maintaining many IP prefixes.

## Example: send Azure Monitor and Backup traffic straight out
```bash
az network route-table route create -g rg -n to-azuremonitor --route-table-name rt-app \
  --address-prefix AzureMonitor --next-hop-type Internet
az network route-table route create -g rg -n to-backup-weu --route-table-name rt-app \
  --address-prefix AzureBackup.WestEurope --next-hop-type Internet
az network route-table route create -g rg -n default-to-fw --route-table-name rt-app \
  --address-prefix 0.0.0.0/0 --next-hop-type VirtualAppliance --next-hop-ip-address <firewall-private-ip>
```
Next hop types used here: `Internet`, `VirtualAppliance` (needs a next hop IP), `VirtualNetworkGateway` (supported only for VPN gateways) and `None` (traffic is dropped).

## Precedence
- If a route with an explicit IP prefix and a route with a service tag match exactly, the explicit prefix wins.
- When several service tag routes match, they are evaluated in order: regional tags (for example `Storage.EastUS`),
  top-level tags, `AzureCloud` regional tags, then the `AzureCloud` tag.
- Longest prefix match still decides between different prefix lengths.

## Gotchas
- Bypassing the firewall means no inspection or logging there for that traffic: document the risk acceptance.
- Not every tag can be used in UDRs; check the "usable in" columns on the service tags page.
- A `0.0.0.0/0` route with a virtual appliance or gateway next hop sends traffic for Azure service public IPs there too.

## Verify
- [ ] `az network watcher show-next-hop` to an Azure Monitor address returns `Internet`; other destinations return the firewall IP.

## Checked
2026-10-31. Confirmed against Learn "Virtual network traffic routing" (service tags for UDRs, exact-match rule and
precedence order, next hop types incl. the gateway restriction, 0.0.0.0/0 behaviour) and the service tags overview. Removed: route-table service-tag
route count limit, Windows KMS and AKS use cases, Bicep snippet and private endpoint statement.
Method: documentation only; no commands were run.
