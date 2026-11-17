---
id: computing-software.systems-network-administration.windows-server.azure-file-sync-server-endpoint-disaster-recovery
name: azure-file-sync-server-endpoint-disaster-recovery
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-file-sync, afs-disaster-recovery, server-endpoint, cloud-tiering, restore]
level: advanced
status: docs-checked
description: "Recover from losing an Azure File Sync server: rebuild the server endpoint from the Azure file share, fast DR with namespace-first download, and what tiering means for RTO."
sources:
  - https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-disaster-recovery-best-practices
  - https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-server-recovery
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure File Sync server endpoint disaster recovery

The Azure file share is the authoritative copy. If a file server dies, a new server can be rebuilt from the
cloud without restoring backups to the server.

## Rebuild steps
1. Build a new Windows Server, install the Azure File Sync agent, **register** it with the same Storage Sync Service.
2. In the sync group, **add a server endpoint** on the new server with an empty local path.
3. Initial download mode: with cloud tiering enabled, leave it at the default (namespace only): only the namespace
   downloads and files appear as tiered, which speeds recovery. With tiering disabled the only option is a full
   download. Do not copy data manually while the namespace syncs. The "namespace first, then content" mode suits
   server-side DR when the path starts empty: content then recalls in the background by heatmap order.
4. Recreate SMB shares and share permissions (not synced; keep a script, see export-share-definitions).
5. Point DNS alias/DFS-N to the new server.

If data on the old disk never uploaded, the recovery guide copies it to the new volume with
`Robocopy <old-dir> <new-dir> /COPY:DATSO /MIR /DCOPY:AT /XA:O /B /IT /UNILOG:<log-file>`, finishing each server's
copy before the changeover. Then delete the old server endpoint and unregister the old server
(`Unregister-AzStorageSyncServer` / portal "Unregister server").

## RTO and RPO
- RPO: changes not yet uploaded from the dead server are lost unless recovered from its disk as above.
- RTO: the namespace downloads first, then content in the background while users keep working; a recall-heavy
  workload needs bandwidth planning.
- For HA, a standby server with its own endpoints in the same sync group (no user access, namespace-only tiering)
  plus DFS-N lets you redirect users quickly; a failover cluster needs no special Azure File Sync steps.

## Other DR scenarios
- Ransomware: share snapshots are read-only, so restore from Azure file share snapshots (Azure Backup); enable soft
  delete to protect the snapshots.
- Region loss: with GRS or GZRS, Microsoft may fail over the Storage Sync Service if the region is judged
  permanently unrecoverable. After a customer-initiated storage account failover you must also open a support ticket
  to fail over the Storage Sync Service; expect reconciliation and possible conflicts.
- Unsupported on a registered server: OS backup restore, cloning the OS, reverting to a VM checkpoint, moving the
  volume to another server while the endpoint is active, or restoring tiered files from third-party backup. Restore
  files into the share or a new endpoint instead.

## Verify
- [ ] DR test: new server endpoint reaches healthy sync with all items visible; a user opens a recalled file.

## Checked
Date 2026-10-27. Documentation: Azure File Sync disaster recovery best practices, server recovery guide, server
endpoint creation (initial download modes). Confirmed: rebuild steps, default download mode, robocopy command,
unsupported actions, HA standby design, failover process for GRS/GZRS.
Method: documentation only; no commands were run.
