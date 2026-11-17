---
id: computing-software.cloud-infrastructure-engineering.azure.azure-file-sync-troubleshooting-per-item-errors-and-health
name: azure-file-sync-troubleshooting-per-item-errors-and-health
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-file-sync, file-sync-troubleshooting, per-item-errors, sync-health, debug-storagesyncserver, cloud-tiering]
level: advanced
status: docs-checked
description: "Diagnose Azure File Sync: server endpoint health, Debug-StorageSyncServer, telemetry and item-results event logs, common per-item errors and cloud change detection."
sources: ["https://learn.microsoft.com/troubleshoot/azure/azure-storage/files/file-sync/file-sync-troubleshoot-sync-errors", "https://learn.microsoft.com/azure/storage/file-sync/file-sync-monitoring", "https://learn.microsoft.com/troubleshoot/azure/azure-storage/files/file-sync/file-sync-troubleshoot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure File Sync troubleshooting

**Goal:** find why files aren't syncing (whole sessions failing vs individual items) and fix the cause.

## Health at a glance
- Portal: Storage Sync Service > Sync group > server endpoint: **Health**, *Files not syncing* count, last session.
- Alert on files not syncing and on a server going offline (the monitoring page lists the metrics).

## On the server
Run `Debug-StorageSyncServer` on the server to check for common problems and to list the names of items that fail to sync (see the cmdlet reference for its parameters), or run `FileSyncErrorsReport.ps1` from the agent installation directory.

Event Viewer > Applications and Services > Microsoft > FileSync > Agent:
- *Telemetry*: events 9102 and 9302 record sync session results; the portal health is based on them.

## Common per-item causes
| HResult | Meaning | Fix |
|---|---|---|
| 0x8007007b | ERROR_INVALID_NAME: the file or directory name is invalid | Follow the remediation for this error on the sync errors page |

Session-wide failures: check the server registration, storage account firewall, share quota and agent version against the troubleshooting pages.

## Changes made directly in the Azure file share
Changes made directly in the Azure file share are found by a periodic change detection; to sync them immediately, run the change detection cmdlet:
```powershell
Invoke-AzStorageSyncChangeDetection   # see the cmdlet reference for its parameters
```

## Verify
- [ ] FileSyncErrorsReport empty or explained; metrics show successful sessions both directions in the last hour.

## Checked
2026-10-28. Confirmed on the sync errors troubleshooting and monitoring pages: Debug-StorageSyncServer and FileSyncErrorsReport.ps1, Telemetry log events 9102 and 9302, `Invoke-AzStorageSyncChangeDetection`, 0x8007007b ERROR_INVALID_NAME.
Removed (not confirmed): the Debug-StorageSyncServer parameters, ItemResults event, 0x80070020 and 0x80070005 rows, metric names, the 24-hour detection interval, change detection parameters, and the cloud tiering section including `Invoke-StorageSyncFileRecall`.

Method: documentation only; no commands were run.
