---
id: computing-software.cloud-infrastructure-engineering.azure.centralised-private-endpoint-dns-in-hub-spoke
name: centralised-private-endpoint-dns-in-hub-spoke
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, private-link, central-private-dns, private-endpoint-hub-dns, private-dns-zones, dns-private-resolver, conditional-forwarding]
level: advanced
status: docs-checked
description: "Centralise private endpoint DNS for hub-spoke and on-prem: one set of privatelink zones in the connectivity subscription, Private Resolver, spoke DNS and on-prem forwarders."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/private-link-and-dns-integration-at-scale", "https://learn.microsoft.com/azure/private-link/private-endpoint-dns-integration", "https://learn.microsoft.com/azure/private-link/private-endpoint-dns"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Centralised DNS for private endpoints in hub-spoke

**Goal:** every VNet and on-prem client resolves the service names to the right private IP from one authoritative
set of zones, no matter which spoke owns the endpoint.

## Design
- One private DNS zone per privatelink namespace (for example `privatelink.blob.core.windows.net`,
  `privatelink.vaultcore.azure.net`, `privatelink.database.windows.net`) in the connectivity subscription.
- Link the zones to the VNet that hosts the DNS path (hub / resolver VNet); spokes use the hub DNS server.
- Azure DNS Private Resolver in the hub: the inbound endpoint is the DNS server for spokes and the conditional-forwarder
  target for on-prem; the Private Resolver resolves queries through Azure-provided DNS `168.63.129.16`.
- On-prem DNS: conditional forwarders for the **public** zone (for example `database.windows.net`), not the
  `privatelink` zone, pointing at the Private Resolver or an Azure-hosted DNS forwarder.

## Records
Records are created by the private endpoint's DNS zone group in the zone you attach; each DNS zone group can hold
only one private DNS zone per zone name. Centralising means granting the platform pipeline or policy that write
access rather than every spoke owner.

## Gotchas
- Some services need several zones or regional names: AKS API server `privatelink.<region>.azmk8s.io`, Azure Monitor
  (monitor, oms, ods, agentsvc and blob zones), ACR (`privatelink.azurecr.io`, no extra zone for the data endpoint
  when using Azure Private DNS zones). Take the full list from the "private endpoint DNS zone values" table.
- Forwarding a whole public service zone to the resolver makes every lookup depend on the resolver and the hybrid link.

## Verify
- [ ] From a spoke VM and from on-prem, `nslookup <account>.blob.core.windows.net` returns the private endpoint IP.
- [ ] `az network private-dns zone list --query "[].name"` in the connectivity subscription matches the required zone list.

## Checked
2026-10-31. Confirmed against Learn "Private endpoint DNS integration" and "Azure Private Endpoint private DNS zone
values": zone names, public-zone forwarder rule, Private Resolver and 168.63.129.16 behaviour, one zone per name in a
zone group, AKS/ACR/Monitor zone details. Removed: the Azure Policy initiative name, 1,000-link limit, /28 subnet
requirement, example IPs, firewall DNS proxy advice, split-brain and duplicate-zone claims, Container Apps and ADF.
Method: documentation only; no commands were run.
