---
id: computing-software.systems-network-administration.backup-and-recovery.hyper-v-host-level-backup
name: hyper-v-host-level-backup
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [hyper-v-backup, hyper-v, vss, hyper-v-vss-writer, image-level-backup, wbadmin, csv-backup]
level: advanced
status: draft
description: "Back up Hyper-V VMs at host level: how VSS, production checkpoints and RCT interact, Windows Server Backup for VMs, clustered CSV specifics, Linux guests, and common failures."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-start-backup
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/manage-hyper-v-integration-services
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V host-level backup

**Goal:** consistent image-level backups of every VM without agents inside guests.

## How it works (Windows Server 2016+)
1. Backup software asks Hyper-V (WMI) for a **recovery checkpoint**.
2. With the "Backup (volume shadow copy)" integration service, Hyper-V asks the guest to quiesce: VSS in Windows guests (application-consistent), `hv_vss_daemon` fsfreeze in Linux guests (file-system consistent).
3. Backup reads the frozen disk state; Resilient Change Tracking records changed blocks for the next incremental.
4. Checkpoint is merged; a reference point remains for RCT.
If the guest cannot quiesce, the backup is crash-consistent (or fails, depending on product settings).

## Windows Server Backup for Hyper-V
```cmd
wbadmin start backup -backupTarget:E: -hyperv:"app01,web01" -quiet
wbadmin get versions
wbadmin start recovery -version:10/15/2026-02:00 -itemType:HyperV -items:app01
```
Fine for small standalone hosts; no central management or long retention.

## Clusters and CSV
Back up through a cluster-aware product; it coordinates with the owning node of each VM. Avoid simultaneous host-level snapshots of the same CSV from many nodes; products serialize or use CSV-aware VSS.

## Prerequisites and checks
```powershell
Get-VMIntegrationService -VMName app01 | Where-Object Name -like 'Backup*'
vssadmin list writers          # on host: "Microsoft Hyper-V VSS Writer" Stable, No error
```
Inside Windows guests, `vssadmin list writers` must show stable writers. Linux guests need `hv_vss_daemon` (hyperv-daemons package) running.

## Common failures
- Recovery checkpoints left behind after failed jobs (`Get-VMSnapshot -SnapshotType Recovery`): remove after fixing the cause.
- Guest VSS errors (full shadow storage, broken writer): fix in the guest; check its Application log.
- VMs with shared VHDX (legacy) cannot be backed up at host level; use VHD Set.
- Antivirus scanning VM folders interferes with checkpoints; apply Hyper-V AV exclusions.

## Verify
Job logs show application-consistent processing for Windows VMs, incrementals use RCT, and periodic test restores boot.
