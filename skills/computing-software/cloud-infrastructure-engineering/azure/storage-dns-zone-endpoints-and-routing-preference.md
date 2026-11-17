---
id: computing-software.cloud-infrastructure-engineering.azure.storage-dns-zone-endpoints-and-routing-preference
name: storage-dns-zone-endpoints-and-routing-preference
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, storage-accounts, dns-zone-endpoints, routing-preference, internet-routing, storage-endpoints, account-limits]
level: practitioner
status: docs-checked
description: "Choose storage account endpoint types: standard vs Azure DNS zone endpoints for large account counts, and Microsoft vs internet routing preference for egress cost."
sources: ["https://learn.microsoft.com/azure/storage/common/storage-account-overview", "https://learn.microsoft.com/azure/storage/common/azurednszone-endpoints-retirement-faq", "https://learn.microsoft.com/azure/storage/common/network-routing-preference", "https://learn.microsoft.com/azure/storage/common/storage-account-create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage endpoints and routing preference

**Goal:** pick the endpoint and routing options at creation time. Note: Azure DNS zone endpoints are a preview feature that Microsoft says enters retirement in March 2027; prefer Standard endpoints.

## Standard vs Azure DNS zone endpoints
- **Standard** (recommended): `<account>.blob.core.windows.net`. By default up to **250** storage accounts per region per subscription
  (up to 1000 with a quota increase).
- **Azure DNS zone endpoints (preview, entering retirement in March 2027)**: `<account>.z<N>.blob.storage.azure.net` (zone identifier z1 to z9 or z10 to z50) - allows up to
  **5,000** accounts per region per subscription. Microsoft asks customers to move to Standard endpoints by April 1, 2027; existing accounts are not deleted, but the ability to create new ones is being removed. Set at creation:
```bash
az storage account create -g rg -n stmanytenant01 -l westeurope --sku Standard_LRS --kind StorageV2 \
  --dns-endpoint-type AzureDnsZone
az storage account show -g rg -n stmanytenant01 --query primaryEndpoints
```
- Always read endpoints from the account properties; never construct hostnames in code (the zone is assigned dynamically).
- To find accounts that use DNS zone endpoints, use the Azure Resource Graph query in the retirement FAQ.

## Routing preference (internet egress)
- **Microsoft network routing** (default): traffic is routed to the public endpoint over the Microsoft global network, optimised for performance.
- **Internet routing**: traffic leaves the Microsoft global network at the earliest opportunity to the transit ISP, which lowers networking costs.
Configure the default routing choice and whether to publish route-specific endpoints in the portal or with PowerShell or the CLI (see the routing preference article for the current commands).
Publishing route-specific endpoints adds hostnames like `<account>-internetrouting.blob.core.windows.net` so clients
can choose per request.

## Gotchas
- Routing preference applies to traffic to the public endpoint; check the article's limitations and supported configurations before relying on it.
- Firewalls and allow-lists keyed on hostnames must include route-specific endpoints if used.

## Verify
- [ ] `primaryEndpoints` show the expected hostname pattern; egress meter in cost analysis reflects the chosen routing.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/common/storage-account-overview, azurednszone-endpoints-retirement-faq, network-routing-preference, storage-account-create): 250 accounts per region default and 1000 with a quota increase (the skill said 500), Azure DNS zone endpoints are a preview that enters retirement in March 2027 (move by April 1, 2027), 5,000 account limit, endpoint format with z1-z9 or z10-z50 zone identifier, `--dns-endpoint-type AzureDnsZone`, Microsoft versus Internet routing behaviour, `-internetrouting` endpoint naming. Removed the unconfirmed `az storage account update --routing-choice` flags and the private DNS zone remark.

Method: documentation only; no commands were run.
