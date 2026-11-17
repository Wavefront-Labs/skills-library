---
id: computing-software.systems-network-administration.windows-server.azure-file-sync-deployment
name: azure-file-sync-deployment
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-file-sync, sync-group, server-endpoint, cloud-endpoint, storage-sync-service, register-azstoragesyncserver, azure-files]
level: practitioner
status: docs-checked
description: "Deploy Azure File Sync: Storage Sync Service, sync group with cloud endpoint, install and register the agent, add server endpoints and check initial sync."
sources:
  - https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-deployment-guide
  - https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-planning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploy Azure File Sync

## Azure side
1. Storage account (StorageV2) in the same region as the Storage Sync Service, with an Azure file share in it
   (provisioned v2 is recommended for new deployments). The account must allow storage account key access, SMB 3.1.1,
   NTLM v2 authentication and AES-128-GCM encryption.
2. Storage Sync Service resource (one per distinct group of servers; keep their number small).
3. Sync group: one cloud endpoint (the Azure file share).
```powershell
New-AzStorageSyncService -ResourceGroupName rg-files -Name sss-files -Location westeurope
New-AzStorageSyncGroup -ParentObject $sss -Name Finance
New-AzStorageSyncCloudEndpoint -ParentObject $sg -Name cloud -StorageAccountResourceId $sa.Id -AzureFileShareName finance
```

## Server side
- Windows Server 2016, 2019, 2022 or 2025 (Full or Core), .NET Framework 4.7.2 or later, local NTFS volumes. A
  server endpoint on the system volume cannot use cloud tiering.
- Install the Azure File Sync agent (MSI), disable IE ESC during registration on Desktop
  Experience, sign in and register (`ServerRegistration.exe`, or PowerShell with the Az.StorageSync module):
```powershell
Register-AzStorageSyncServer -ParentObject $sss
New-AzStorageSyncServerEndpoint -ParentObject $sg -Name FS01-Finance -ServerResourceId $server.ResourceId `
  -ServerLocalPath '<vol>:\Shares\Finance' -CloudTiering -VolumeFreeSpacePercent 20
```
- Outbound HTTPS 443 to Azure (service tags `StorageSyncService`, `Storage`, `AzureResourceManager`,
  `AzureActiveDirectory`); proxy via `Set-StorageSyncProxyConfiguration`.

## Topology rules
- One sync group = exactly one cloud endpoint + server endpoints (limits: 100 per sync group, 30 per server).
- A server registers to one Storage Sync Service. Several server endpoints can share a volume if their paths do not
  overlap and each is in its own sync group; endpoints cannot be nested.
- DFS-R: replace it with Azure File Sync in most cases. If both run side by side, disable cloud tiering on volumes
  with DFS-R folders, do not use DFS-R read-only folders, and overlap only one server endpoint with a DFS-R location.

## Verify
- [ ] Portal: server endpoint health green, sync activity shows uploads.
- [ ] Event 9102 in `Microsoft-FileSync-Agent/Telemetry` shows `PerItemErrorCount` 0 for completed sessions.

## Checked
Date 2026-10-27. Documentation: Azure File Sync deployment guide, planning guide, scale targets, networking overview,
server endpoint creation, Az.StorageSync cmdlet references. Confirmed: storage account kind and settings, cmdlet
names and parameters, supported OS and .NET, tiering and system volume rule, scale limits, DFS-R rules, service tags.
Method: documentation only; no commands were run.
