---
id: computing-software.systems-network-administration.windows-server.hybrid-dns-azure-private-resolver
name: hybrid-dns-azure-private-resolver
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-dns-server, azure-private-dns, dns-private-resolver, conditional-forwarder, private-endpoint, privatelink, 168-63-129-16, hybrid-name-resolution, forwarding-ruleset]
level: practitioner
status: gated
description: "Hybrid name resolution between Windows DNS and Azure: private DNS zones for private endpoints, DNS Private Resolver inbound/outbound endpoints, and conditional forwarders."
sources:
  - https://learn.microsoft.com/en-us/azure/dns/dns-private-resolver-overview
  - https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns-integration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid DNS: Windows DNS with Azure Private DNS and Private Resolver

## The problem
Azure private endpoints (storage, SQL, Key Vault) resolve via Azure **private DNS zones**
(`privatelink.blob.core.windows.net`) linked to VNets. On-prem clients asking Windows DNS get
the public IP unless you forward those zones into Azure.

## Pieces
- **Azure-provided DNS** `168.63.129.16`: reachable only from inside an Azure VNet.
- **DNS Private Resolver**: an Azure-managed resolver with an **inbound endpoint** (private IP
  on-prem can forward to) and an **outbound endpoint** + **forwarding ruleset** (Azure VNets
  forward selected domains to on-prem DNS).

## On-prem to Azure (Windows DNS)
Create conditional forwarders on DCs/DNS servers for the **public** service suffix (not the
`privatelink` name) pointing at the resolver's inbound endpoint IP:
```powershell
'blob.core.windows.net','database.windows.net' | ForEach-Object {   # add the public suffix of each private-link service you use
  Add-DnsServerConditionalForwarderZone -Name $_ -MasterServers 10.100.0.4 -ReplicationScope Forest }
```
Learn is explicit that the conditional forwarder must target the recommended public DNS zone forwarder (for example
`database.windows.net`, not `privatelink.database.windows.net`).

## Azure to on-prem
Outbound endpoint + ruleset: rule `ad.example.com.` -> on-prem DC IPs; link the ruleset to the VNets that need it. Or point VNet DNS at DCs in Azure which forward to the Azure-provided DNS service (168.63.129.16).

## Verify
```powershell
Resolve-DnsName mystorage.blob.core.windows.net -Server dc01    # should return the private endpoint IP address
```
- [ ] On-prem resolves private endpoint names to private IPs.
- [ ] Azure VMs resolve `ad.example.com` names.

## Checked
2026-10-28. Confirmed on Learn (DNS Private Resolver overview and private endpoint DNS integration): Azure-provided DNS 168.63.129.16,
inbound endpoint as the on-prem forwarder target, outbound endpoint with forwarding ruleset, conditional forwarding to the
public zone name rather than privatelink. Removed as unconfirmed: vaultcore/file suffix list entries, port 53 detail,
CNAME-chain explanation, replacement-of-forwarder-VMs claim. Add-DnsServerConditionalForwarderZone is not on the fetched
pages; it is the Windows DNS Server cmdlet (see its module reference before use) (gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
