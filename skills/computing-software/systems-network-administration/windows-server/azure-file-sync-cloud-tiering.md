---
id: computing-software.systems-network-administration.windows-server.azure-file-sync-cloud-tiering
name: azure-file-sync-cloud-tiering
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-file-sync, cloud-tiering, volume-free-space-policy, date-policy, invoke-storagesyncfilerecall, tiered-files, offline-attribute, afs-file-recall]
level: practitioner
status: docs-checked
description: "Configure Azure File Sync cloud tiering: volume free space and date policies, recall behaviour, recall and tiering commands, and impact on backup and AV."
sources:
  - https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-cloud-tiering-overview
  - https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-how-to-manage-tiered-files
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Azure File Sync cloud tiering

Tiering replaces cold files on the server with reparse points (offline attribute) whose
data lives only in the Azure file share. Opening a tiered file recalls it transparently.

## Policies
- **Volume free space**: keep X% of the volume free; the coldest files tier first (the heatmap ranks files by the
  newest of last access, last modified and creation time). Applies at the volume level, not per directory or
  server endpoint.
- **Date policy**: tier files not accessed in N days, regardless of free space.
```powershell
Set-AzStorageSyncServerEndpoint -InputObject $ep -CloudTiering -VolumeFreeSpacePercent 20 -TierFilesOlderThanDays 60
```
- Initial download mode for new endpoints: namespace only (default when tiering is on), namespace first then
  content (default when tiering is off), or avoid tiered files (only when tiering is off). It cannot be changed after
  the endpoint is created.
- Minimum file size to tier is double the file system cluster size (8 KiB on 4 KiB clusters).
- Server endpoints on the system volume cannot use cloud tiering.

## Manual control
```powershell
Import-Module "$env:ProgramFiles\Azure\StorageSyncAgent\StorageSync.Management.ServerCmdlets.dll"
Invoke-StorageSyncFileRecall -Path '<vol>:\Shares\Finance' -ThreadCount 8   # bring back (path = server endpoint)
Invoke-StorageSyncCloudTiering -Path '<vol>:\Shares\Finance\Archive'      # tier now
Get-StorageSyncFileRecallResult
```
Find tiered files: the Attributes column in File Explorer shows `O` (offline, some or all content not on disk) and,
on Windows Server 2019 and newer, `M` (recall on data access).

## Gotchas
- With tiering on, do not run an on-premises backup of the server endpoint: tiered files are skipped, backed up as
  stubs, or recalled with egress charges. Back up the Azure file share (Azure Backup snapshots) instead, or back up
  from a server in the sync group with tiering disabled.
- Antivirus can trigger recalls. Tiered files carry `FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS`; Microsoft Defender and
  System Center Endpoint Protection skip them in on-demand scans. Ask other vendors how to skip that attribute.
- Cloud tiering does not use the NTFS last-access-time setting (off by default); the agent tracks access itself.
- Recalls started by `Invoke-StorageSyncFileRecall` are persisted to disk; user-open recalls are not persisted.

## Verify
- [ ] Portal Cloud tiering status healthy; volume free space at policy.
- [ ] Events 9003, 9016 and 9029 in `Microsoft-FileSync-Agent/Telemetry` show tiering activity (9005, 9006, 9009
  and 9059 for recalls).

## Checked
Date 2026-10-27. Documentation: cloud tiering overview, policy and manage-tiered-files pages, scale targets,
planning guide (antivirus), disaster recovery best practices, cloud tiering troubleshooting, and the Az.StorageSync
Set-AzStorageSyncServerEndpoint reference. Confirmed: policy semantics, minimum tiered file size, initial download
modes, cmdlet names and parameters, attributes, event IDs.
Method: documentation only; no commands were run.
