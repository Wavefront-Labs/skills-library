---
id: computing-software.cloud-infrastructure-engineering.azure.service-tags-usage-and-downloadable-ranges
name: service-tags-usage-and-downloadable-ranges
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, service-tags, service-tag-ranges, service-tag-discovery, nsg, firewall-allowlist, regional-service-tags]
level: practitioner
status: docs-checked
description: "Use Azure service tags in NSGs, firewalls and UDRs, and export ranges via the Service Tag Discovery API or the weekly JSON for on-prem firewalls, tracking changeNumber."
sources: ["https://learn.microsoft.com/azure/virtual-network/service-tags-overview", "https://learn.microsoft.com/rest/api/virtualnetwork/service-tags/list"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service tags and downloadable ranges

**Goal:** allow traffic to/from Azure services without hand-maintained IP lists, and feed non-Azure firewalls with
current ranges.

## In Azure resources
- NSG source/destination and Azure Firewall rules can use tags such as `Storage.WestEurope`, `AzureMonitor`,
  `AzureActiveDirectory`, `GatewayManager` (inbound management traffic for VPN Gateway and Application Gateway).
- Prefer regional tags (`Storage.WestEurope`) over the global one: narrower.
- Microsoft maintains the prefixes behind a tag.
- The tables on the overview page show direction, and whether each tag is usable in NSG and firewall rules; check
  them, because not every tag supports every use.

## For on-prem / third-party firewalls
```bash
az network list-service-tags --location westeurope --query "values[?name=='AzureKeyVault.WestEurope'].properties.addressPrefixes[]" -o tsv
```
- REST: `GET /subscriptions/{subscriptionId}/providers/Microsoft.Network/locations/{location}/serviceTags?api-version=...`
  (use the version shown on the Learn reference page).
- The downloadable JSON files (one per cloud, linked from the overview page) are updated and published weekly.
- The API can lag: new tag data takes up to four weeks to propagate to the API in all regions, so API results may
  differ from the JSON download.
- Compare `changeNumber` between publications: each tag (for example `Storage.WestUS`) has its own, and the top-level
  number rises when any tag changes.
- Newly added IP addresses are not used in Azure for at least one week, which is your window to update firewalls.

## Gotchas
- `AzureCloud` is all datacenter public IP addresses (and excludes IPv6): allowing it is close to allowing the internet.
- `AzureDevOps` is an inbound-direction tag, so it does not help outbound allowlisting.
- Tags identify a service's public ranges, not your resource; combine with private endpoints or service endpoints.

## Verify
- [ ] NSG rules use regional tags where available.
- [ ] On-prem firewall objects updated within a week of a `changeNumber` bump.

## Checked
2026-10-31. Confirmed against Learn "Virtual network service tags" and the Service Tags - List REST reference: tag
direction/support tables, AzureCloud scope, weekly JSON, changeNumber semantics, one-week rule, four-week API lag,
REST path. Removed: the download ID 56519 (the download page is not readable), a fixed api-version, GatewayManager
port range, `X-Azure-FDID` guidance, KMS and AzureMonitor use-case rows, and UDR next-hop statements.
Method: documentation only; no commands were run.
