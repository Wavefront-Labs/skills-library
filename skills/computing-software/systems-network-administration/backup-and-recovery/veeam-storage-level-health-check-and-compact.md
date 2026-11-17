---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-storage-level-health-check-and-compact
name: veeam-storage-level-health-check-and-compact
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-health-check, compact-full, veeam, storage-level-corruption-guard, backup-integrity, defragment]
level: practitioner
status: docs-checked
description: "Veeam backup file health check (CRC and hash of the latest restore point) and compact of full backup files: defaults, scope and limitations."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/backup_health_check.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/backup_compact_file.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup file health check and compact

## Health check for backup files
- Enable **Perform backup files health check** in the backup job settings and set a schedule. Default: 5:00 on the last Saturday of every month; you can change it to weekly or monthly on specific days.
- It performs a cyclic redundancy check (CRC) on metadata and a hash check on VM data blocks, to verify the latest restore point is consistent and restorable.
- Works for forever forward incremental, forward incremental and reverse incremental (deprecated) chains.
- It verifies only the latest restore point of each VM (if that is incomplete in a forward-incremental chain, the one before it). Because the blocks of that state are spread across several backup files, the check can take long.
- Only the virtual disks and VMs present in the latest restore point are verified: a disk or VM removed from the job is no longer checked beyond its last unverified restore point.

## Compact of the full backup file
- Retention transformations make the full backup file large and fragmented over time. Compact creates a new full file in the repository, copying existing blocks and storing them close together, which defragments it, reduces its size and speeds reads and writes.
- Enable **Defragment and compact full backup file** in job settings and set a schedule. Default: last Saturday of every month; weekly or monthly on specific days is possible.
- Limitations: works for forever forward incremental or reverse incremental (deprecated) chains, so do not schedule active or synthetic fulls; backup files already offloaded to cloud object storage (capacity tier) are not compacted; the repository needs space for a file of the full backup size, since auxiliary files exist until the operation ends; on days when an active full is triggered, compact is done another day in the job session.
- Per-machine chains: a VM added to an existing job is compacted during its next incremental session.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center pages "Health Check for Backup Files" and "Compact of Full Backup File" (compact page read through the limitations list; the tail of each page was truncated).
Removed (not on the text read): UI menu path "Storage > Advanced > Maintenance", automatic repair from source, on-demand run and PowerShell claims, "Remove deleted items data" detail, scheduling and I/O advice, SureBackup remark, Verify section.
Method: documentation only; no commands were run.
