---
id: computing-software.systems-network-administration.virtualisation.hyper-v-resilient-change-tracking
name: hyper-v-resilient-change-tracking
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, resilient-change-tracking, rct, mrt, incremental-backup, recovery-checkpoint, reference-point, windows-server]
level: advanced
status: docs-checked
description: "Understand Hyper-V Resilient Change Tracking (RCT) for incremental backups: .rct/.mrt files, recovery checkpoints, reference points, and what forces a full backup."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/backup-approaches
  - https://learn.microsoft.com/en-us/windows/win32/hyperv_v2/msvm-virtualsystemsnapshotservice-converttoreferencepoint
  - https://learn.microsoft.com/en-us/windows/win32/hyperv_v2/msvm-virtualsystemreferencepoint
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/get-vmsnapshot
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Resilient Change Tracking for Hyper-V backups

**Goal:** keep host-level VM backups incremental and diagnose when they fall back to full.

## How it works (Windows Server 2016 and later)
1. Backup software creates a **recovery checkpoint** (snapshot type Recovery) through the Hyper-V WMI provider (`Msvm_VirtualSystemSnapshotService`).
2. It reads the data, then calls `ConvertToReferencePoint`: only recovery snapshots can be converted, and the snapshot is deleted as a side effect.
3. Hyper-V WMI backup uses reference points plus **resilient change tracking (RCT)**; `Msvm_VirtualSystemReferencePoint` carries `ResilientChangeTrackingIdentifiers` for the virtual disks.
4. The next backup asks for changes since the reference point, so it is incremental. The Win32 virtual disk APIs (`QueryChangesVirtualDisk` and related) read the changes locally.

## Inspect
```powershell
Get-VMSnapshot -VMName app01 -SnapshotType Recovery          # should be empty between jobs
Get-CimInstance -Namespace root\virtualization\v2 -ClassName Msvm_VirtualSystemReferencePoint |
  Select-Object ElementName, InstanceID
```

## Common issues
- Leftover recovery checkpoints after failed jobs: remove them (`Remove-VMSnapshot`) once no job is running.
- A full backup after a restore, migration or crash usually means the backup product lost its reference point; check the product's job log, because Microsoft's pages do not list the conditions.

## Verify
Two consecutive backup jobs: the second transfers only changed data (per the backup product's job statistics), and no stray `Recovery` checkpoints remain afterwards.

## Checked

Checked 2026-10-26 against MicrosoftDocs/windowsserverdocs (Hyper-V backup approaches page, dated 2025-06-17) and MicrosoftDocs/win32 (Hyper-V WMI v2 `ConvertToReferencePoint` and `Msvm_VirtualSystemReferencePoint` pages), plus the `Get-VMSnapshot -SnapshotType Recovery` reference. Confirmed: WMI-based backup from Windows Server 2016 uses reference points and RCT; only recovery snapshots convert to reference points and the snapshot is deleted. Removed as undocumented: the `.rct` and `.mrt` file names, the 6.2 configuration version gate, the list of events that reset tracking, and the antivirus exclusion advice. The sources list no longer cites generic landing pages.

Method: documentation only; no commands were run.
