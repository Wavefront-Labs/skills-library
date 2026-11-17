---
id: computing-software.cloud-infrastructure-engineering.azure.private-dns-fallback-to-internet-nxdomain-redirect
name: private-dns-fallback-to-internet-nxdomain-redirect
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, private-dns-zones, nxdomain-redirect, fallback-to-internet, private-link, cross-tenant-resources]
level: practitioner
status: docs-checked
description: "Stop privatelink zones breaking access to resources you don't own: enable fallback to internet (NxDomainRedirect) on private DNS zone VNet links and know when to use it."
sources: ["https://learn.microsoft.com/azure/dns/private-dns-fallback", "https://learn.microsoft.com/azure/private-link/private-endpoint-dns", "https://learn.microsoft.com/cli/azure/network/private-dns/link/vnet"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private DNS fallback to internet

**Goal:** your VNet can still reach a partner's (or another tenant's) storage account publicly even though your
`privatelink.blob.core.windows.net` zone has no record for it.

## The problem
Public name `partnerst.blob.core.windows.net` CNAMEs to `partnerst.privatelink.blob.core.windows.net`. Because your
VNet is linked to a private zone named `privatelink.blob.core.windows.net`, Azure DNS answers from that zone - which
has no `partnerst` record - and returns **NXDOMAIN**. Access fails.

## The fix: resolution policy on the VNet link
```bash
az network private-dns link vnet update -g rg-dns -z privatelink.blob.core.windows.net -n link-hub \
  --resolution-policy NxDomainRedirect
az network private-dns link vnet show -g rg-dns -z privatelink.blob.core.windows.net -n link-hub
```
With `NxDomainRedirect`, when the private zone has no matching record, Azure DNS retries public resolution and
returns the public answer.

## When to use
- Hub-wide privatelink zones where workloads also call third-party or other-tenant PaaS endpoints with private
  endpoints of their own.
- Transitional periods while private endpoints are rolled out resource by resource.

## When not to rely on it
- For your **own** resources that should be private: a missing record silently falls back to public, and the
  service firewall then rejects the connection (or, worse, succeeds if public access is open). Keep DINE policy creating
  records for your private endpoints, and alert on public access.

## Gotchas
- Applies to Private Link zones and is enabled per virtual network link.

## Verify
- [ ] `nslookup partnerst.blob.core.windows.net` from the VNet returns a public IP; your own private-endpoint accounts still resolve to private IPs.

## Checked
2026-10-28. Confirmed on the private-dns-fallback page and the `az network private-dns link vnet` reference: `--resolution-policy {Default, NxDomainRedirect}`, fallback enabled at the virtual network link, NXDOMAIN behaviour for Private Link zones.
Removed (not confirmed): the `--query resolutionPolicy` output name, the on-premises resolver and conditional forwarder gotchas.

Method: documentation only; no commands were run.
