---
id: computing-software.systems-network-administration.windows-server.azure-file-sync-networking-and-private-endpoints
name: azure-file-sync-networking-and-private-endpoints
category: computing-software
field: systems-network-administration
product: windows-server
tags: [azure-file-sync, afs-private-endpoint, private-endpoint, proxy, firewall-rules]
level: advanced
status: docs-checked
description: "Network Azure File Sync: required endpoints, service tags, proxy settings, private endpoints for the storage account and sync service, and DNS for them."
sources:
  - https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-networking-overview
  - https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-firewall-and-proxy
  - https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-networking-endpoints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure File Sync networking and private endpoints

The agent talks HTTPS 443 to two things: the **Storage Sync Service** (management, sync orchestration) and the
**storage account** (file data). Both can be private.

## Public path (simplest)
Allow outbound 443 to the service tags `StorageSyncService`, `Storage`, `AzureResourceManager` and
`AzureActiveDirectory`, or to the FQDNs in the firewall doc: `*.afs.azure.net` (sync service only), `*.one.microsoft.com`
(broader, so prefer the regional `<region>01.afs.azure.net` URLs if you need to narrow it), `*.core.windows.net`,
`management.azure.com`, `login.microsoftonline.com`, `login.windows.net`, `graph.microsoft.com`, the Microsoft PKI/OCSP
URLs and the Microsoft Update domains listed there. The service tag IP ranges are published weekly (Service Tag
Discovery API / Download Center JSON).

## Proxy
App-specific proxy settings need agent 4.0.1.0 or newer (machine-wide proxy settings also work):
```powershell
Import-Module "$env:ProgramFiles\Azure\StorageSyncAgent\StorageSync.Management.ServerCmdlets.dll"
Set-StorageSyncProxyConfiguration -Address <proxy-url> -Port <port> -ProxyCredential (Get-Credential)
Get-StorageSyncProxyConfiguration     # blank result = none configured
Remove-StorageSyncProxyConfiguration
```

## Private endpoints
1. Storage account: private endpoint for the file service in a VNet reachable from on-premises (VPN/ExpressRoute).
2. Storage Sync Service: private endpoint (resource type `Microsoft.StorageSync/storageSyncServices`).
3. Create the private endpoints before restricting public access, or sync stops. Sync service public endpoint:
   set `incomingTrafficPolicy` to `AllowVirtualNetworksOnly` (`-IncomingTrafficPolicy` on `New-AzStorageSyncService`;
   `AllowAllTraffic` re-enables it); service endpoints are not supported for it. On the storage account firewall,
   tick "Allow trusted Microsoft services to access this resource" so Azure File Sync can reach it.
4. DNS: the private DNS zones are `privatelink.file.core.windows.net` and `privatelink.afs.azure.net`; on-premises DNS
   must resolve `<account>.file.core.windows.net` and the sync service hostnames (for example
   `<name>management.<region>.afs.azure.net`) to the private endpoint IPs, typically by forwarding to Azure.

## Test
```powershell
Test-StorageSyncNetworkConnectivity
Resolve-DnsName <account>.file.core.windows.net
```
Run the cmdlet after registration; it tests each endpoint specific to the server.

## Verify
- [ ] Connectivity test passes; the storage FQDN resolves to the private endpoint address from the server.

## Checked
Date 2026-10-27. Documentation: Azure File Sync networking overview, firewall and proxy settings, and network
endpoints pages, Az.StorageSync New-AzStorageSyncService reference. Confirmed: service tags, FQDN list, proxy cmdlets
and agent version, private DNS zone names, incomingTrafficPolicy values, trusted-services setting, test cmdlet.
Method: documentation only; no commands were run.
