---
id: computing-software.cloud-infrastructure-engineering.azure.on-premises-dns-for-private-endpoints-via-conditional-forwarders
name: on-premises-dns-for-private-endpoints-via-conditional-forwarders
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, private-endpoint, on-premises-dns, conditional-forwarder, dns-private-resolver, privatelink]
level: practitioner
status: docs-checked
description: "Make on-premises clients resolve Azure private endpoints: conditional forwarders for public zones to a DNS Private Resolver or Azure DNS forwarder, and zone names."
sources: ["https://learn.microsoft.com/azure/private-link/private-endpoint-dns-integration", "https://learn.microsoft.com/azure/private-link/private-endpoint-dns"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-premises DNS for private endpoints

**Goal:** an on-prem client resolves `mystorage.blob.core.windows.net` to the private endpoint IP over ExpressRoute/VPN.

## Architecture
On-prem DNS -> conditional forwarder -> DNS Private Resolver (or a DNS forwarder in Azure) -> Azure-provided DNS
`168.63.129.16` -> private DNS zones linked to that VNet.

## Forward the public zone, not the privatelink zone
The conditional forwarding must target the public DNS zone, for example `database.windows.net` instead of
`privatelink.database.windows.net`. Forwarders for common services (from the Learn zone-values table):

| Service | Forward zone |
|---|---|
| Blob / ADLS Gen2 | `blob.core.windows.net`, `dfs.core.windows.net` |
| Azure SQL Database | `database.windows.net` |
| Key Vault | `vault.azure.net`, `vaultcore.azure.net` |
| Container Registry | `azurecr.io` (+ `<region>.data.azurecr.io`) |
| App Service / Functions | `azurewebsites.net`, `scm.azurewebsites.net` |
Use the full table for other services.

## Windows DNS example
```powershell
Add-DnsServerConditionalForwarderZone -Name "blob.core.windows.net" -MasterServers <resolver-inbound-ip-1>,<resolver-inbound-ip-2> -ReplicationScope Forest
```

## Gotchas
- The forwarder target must be reachable from the on-prem DNS servers through firewalls.
- Flush client caches (`ipconfig /flushdns`) after changes.

## Verify
- [ ] `nslookup mystorage.blob.core.windows.net <onprem-dns>` returns the private IP.

## Checked
2026-10-31. Confirmed against Learn "Private endpoint DNS integration" (public-zone forwarder rule, Private Resolver and
168.63.129.16 role) and "Azure Private Endpoint private DNS zone values" (zone names listed above). Removed: BIND
example, claims about unreachable 168.63.129.16, NXDOMAIN for third-party resources, UDP/TCP 53 port statement and
example IPs (not stated on the pages read).
Method: documentation only; no commands were run.
