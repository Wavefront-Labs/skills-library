---
id: computing-software.systems-network-administration.backup-and-recovery.synthetic-and-active-full-backups
name: synthetic-and-active-full-backups
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-methods, backup-types, synthetic-full, active-full, incremental-backup, fast-clone, block-cloning, refs, xfs-reflink, veeam]
level: practitioner
status: docs-checked
description: "Veeam synthetic and active full backups and how Fast Clone (ReFS block cloning, XFS reflink) cuts the I/O of synthetic fulls: requirements, mkfs.xfs format and limitations."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/backup_methods.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/backup_repository_block_cloning.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synthetic vs active full backups (Veeam)

**Goal:** periodic full backups without needless load on production or the repository.

## Where the two fit
In forward incremental (FI) chains, full backups can be created with the synthetic full or the active full method. Regular fulls split the chain into shorter series, which lowers the chance of losing the chain completely and, per Veeam, makes FI the most reliable method. FI has the lowest repository I/O, but the impact on backup storage rises on days with synthetic fulls, and the impact on production storage rises on days with active fulls. FI needs more space than the other methods and may keep more restore points than the retention setting states. The Active Full and Synthetic Full articles themselves were not read, so their exact procedures are not described here.

## Fast Clone
Fast Clone references existing data blocks on a volume instead of copying them between files; blocks are copied only when files are modified. It speeds up synthetic backup creation and transformation, reduces disk space and decreases storage load. In backup jobs it is used to merge backup files, create synthetic full backups (including GFS), transform reverse incremental backups and compact full backup files.

Supported repository types: Linux server, Microsoft Windows server, SMB share, Dell Data Domain, ExaGrid, Fsas ETERNUS CS800, HPE StoreOnce, Infinidat InfiniGuard, Quantum DXi. Fast Clone needs file offsets aligned to cluster boundaries, so Veeam automatically enables the Align backup file data blocks option for repositories that support it.

### Linux (XFS reflink)
Requirements: XFS, a supported Linux distribution, a kernel that supports reflinks, CRC enabled, data block size from 1 KB to 4 KB. Format as documented:
```sh
mkfs.xfs -b size=4096 -m reflink=1,crc=1 /dev/sda1
```
`reflink=1` is disabled by default; `crc=1` is required for reflink and is on by default. Mount the disk, check with `df -hT`, and for a permanent mount add an `/etc/fstab` entry, preferably by UUID (`blkid /dev/sda1`).

### Windows and SMB (ReFS block cloning)
Windows repository: Windows Server 2016 or later (or Windows 10 Pro for Workstations or later) with ReFS 3.1 or later. SMB repository: must support `FSCTL_DUPLICATE_EXTENTS_TO_FILE` and `FSCTL_SET_INTEGRITY_INFORMATION`; SMB shares on Windows also need SMB 3.1.1 and ReFS 3.1 or later. Veeam recommends a ReFS volume formatted with 64 KB cluster size for large data volumes.

## Limitations stated by Veeam
- After manually moving backup chains to a Fast Clone repository (Linux or Windows/SMB), create active full backups for those chains to activate Fast Clone; the backup file compact operation can be scheduled instead. Not required when using Veeam copy or move features.
- Repositories configured in version 9.5 or earlier do not use Fast Clone until you edit the repository and finish the wizard.
- Source and destination files must be on the same ReFS volume.
- Copying data off a ReFS volume downloads (expands) cloned blocks, so the copy takes more space than the original.
- Fast Clone and Windows data deduplication cannot be used together on a Fast Clone repository; a job to an SMB ReFS repository with Windows deduplication enabled fails.
- In a scale-out backup repository with Fast Clone extents, enable the Data Locality placement policy; if backup files sit on different extents, Fast Clone is not used.

## Checked
2026-11-07. Read in full: Veeam Help Center "Backup Methods" (build 13.1.2.57) and "Fast Clone" (page updated 2026-07-20). Removed because the pages do not state them: the definitions of active and synthetic full as written, weekly/monthly schedule advice, health checks as the answer to corruption, DD Boost and StoreOnce Catalyst "virtual synthetics", and the claim that moved block-cloned files "rehydrate" (the page says copying off ReFS expands cloned blocks), the "ReFS needs 64 KB" rule (the page recommends it), the ReFS patch-level gotcha and the invented Verify step. The Active Full and Synthetic Full pages were not read.
Method: documentation only; no commands were run.
