---
id: computing-software.systems-network-administration.windows-server.azure-file-sync-troubleshooting
name: azure-file-sync-troubleshooting
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-file-sync, afs-sync-errors, per-item-errors, file-recall, filesyncsvc, debug-storagesyncserver, troubleshooting]
level: advanced
status: docs-checked
description: "Troubleshoot Azure File Sync: per-item sync errors, server endpoint health, recall failures, agent logs, Debug-StorageSyncServer and common HRESULTs."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/azure/azure-storage/files/file-sync/file-sync-troubleshoot-sync-errors
  - https://learn.microsoft.com/en-us/troubleshoot/azure/azure-storage/files/file-sync/file-sync-troubleshoot-cloud-tiering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshoot Azure File Sync errors and recall

## Where to look
- Portal: server endpoint health, "Files not syncing" with per-item error codes.
- Event logs (Event Viewer, Applications and Services Logs, Microsoft, FileSync, Agent): `Telemetry` (event 9102 =
  completed sync session, 9302 = progress of the current session with `TotalItemCount`, `AppliedItemCount`,
  `PerItemErrorCount`) and `ItemResults` (one event per file or directory that failed to sync).
- Agent self-test (merges AFSDiag, FileSyncErrorsReport and the connectivity test):
```powershell
Import-Module "$env:ProgramFiles\Azure\StorageSyncAgent\StorageSync.Management.ServerCmdlets.dll"
Debug-StorageSyncServer -Diagnose
Debug-StorageSyncServer -TestNetworkConnectivity
Debug-StorageSyncServer -FileSyncErrorsReport
Debug-StorageSyncServer -AFSDiag -OutputDirectory <output-dir> -KernelModeTraceLevel Verbose -UserModeTraceLevel Verbose
```
- Service: `FileSyncSvc`.

## Common per-item errors (ItemResults)
| HRESULT | Error string | Meaning | Action |
|---|---|---|---|
| 0x80c80207 | ECS_E_SYNC_CONSTRAINT_CONFLICT | change waits for a dependent folder to sync | transient; support ticket if it lasts days |
| 0x80c80065 | ECS_E_DATA_TRANSFER_BLOCKED | file caused persistent errors, blocked until the retry interval | none; retried after 24 h |
| 0x80c8031a | ECS_E_NOT_ENOUGH_LOCAL_STORAGE | server endpoint volume low on disk space | free space (remediation required) |
| 0x80c8300f | ECS_E_REPLICA_NOT_READY | service not yet ready to sync this server endpoint | none; typical while a new cloud endpoint's content is scanned (can exceed 24 h) |
| 0x80c8603e | ECS_E_AZURE_STORAGE_SHARE_SIZE_LIMIT_REACHED | Azure file share limit reached | raise the share size/quota (remediation required) |
| 0x80c80019 | ECS_E_SYNC_INVALID_PATH | problem with the server endpoint path | path must exist, be on a local NTFS volume, not a reparse point or existing endpoint |
| 0x80070005 | ERROR_ACCESS_DENIED | either a pending deletion (no action) or access denied by storage account security settings or NTFS permissions | read the full entry for the case that applies |

Look up any other code in the Microsoft sync errors page by hexadecimal or decimal HRESULT or error string.

## Recall failures
- Telemetry events 9005, 9006, 9009 and 9059 cover recalls; 9006 gives the recall error distribution per server
  endpoint (one event per error code per hour).
- Use `Get-StorageSyncFileRecallResult` after `Invoke-StorageSyncFileRecall` to see which files failed. A recall can
  fail with 0x80070070 (ERROR_DISK_FULL) when the volume lacks free space.
- Check network access to the storage account (firewall, private endpoint DNS) with `Debug-StorageSyncServer
  -TestNetworkConnectivity`.

## Server endpoint stuck
- A long initial upload with a high item count is normal; watch the 9302 event counters.
- Changes made directly in the Azure share are detected only when change enumeration runs (once every 24 hours);
  trigger it sooner with `Invoke-AzStorageSyncChangeDetection`.

## Verify
- [ ] Recent 9102 events show `PerItemErrorCount` 0.
- [ ] `Debug-StorageSyncServer -TestNetworkConnectivity` passes.

## Checked
Date 2026-10-27. Documentation: Microsoft sync errors troubleshooting page (per-item error table), cloud tiering
troubleshooting (event IDs, recall errors), Debug-StorageSyncServer page, Az.StorageSync change detection cmdlet page.
Confirmed: log names, event 9102/9302, Debug-StorageSyncServer switches, every HRESULT row above, 24-hour change
enumeration.
Method: documentation only; no commands were run.
