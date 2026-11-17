---
id: computing-software.systems-network-administration.windows-server.backup-restore-deduplicated-volumes
name: backup-restore-deduplicated-volumes
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, data-deduplication, dedup, dedup-backup, optimized-backup, windows-server-backup, vss, restore]
level: practitioner
status: docs-checked
description: "Back up and restore deduplicated volumes correctly: optimised VSS backups, restore size implications, file-level restore and disaster recovery of the chunk store."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/interop
  - https://learn.microsoft.com/en-us/windows-server/storage/data-deduplication/run
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup and restore of deduplicated volumes

## How backup apps see dedup
- Windows Server Backup can back up an optimised volume as-is, that is without removing the deduplicated data.

Check that your backup vendor explicitly supports Windows Data Deduplication.

## Windows Server Backup
```powershell
wbadmin start backup -include:E: -backuptarget:F: -quiet
wbadmin get versions
```
The Microsoft interop page also shows restoring a whole volume (`wbadmin start recovery` with `-itemtype:Volume`) or
selected files (`-itemtype:File -recursive`) from a Windows Server Backup version.

## Restore pitfalls
- Install the Data Deduplication feature (`FS-Data-Deduplication`) on any server that will read a restored dedup volume; on a cluster every node needs it.
- After a volume restore run `Start-DedupJob -Type Scrubbing -Full` to validate all data on the volume.
- The chunk store lives in `System Volume Information`; optimised files copied without it are corrupted.
- Do not use Robocopy to copy dedup volumes: some commands can corrupt the chunk store.

## DR testing
Restore a sample of files monthly to a different host with dedup installed and compare
hashes (`Get-FileHash`).

## Verify
- [ ] Volume-level backup size is in line with an optimised (not fully rehydrated) volume.
- [ ] Test restore succeeded on a host with the feature installed.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23). Confirmed that Windows Server Backup backs up an optimised volume as-is, the wbadmin backup and recovery commands on the interop page, that every cluster node needs the feature, the Robocopy and chunk-store warning, and Scrubbing -Full semantics. Removed the unconfirmed optimised-versus-unoptimised backup taxonomy, vssFull example, unreadable-files claim and size heuristic.

Method: documentation only; no commands were run.
