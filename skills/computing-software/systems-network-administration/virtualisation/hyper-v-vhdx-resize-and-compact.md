---
id: computing-software.systems-network-administration.virtualisation.hyper-v-vhdx-resize-and-compact
name: hyper-v-vhdx-resize-and-compact
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, resize-vhd, optimize-vhd, vhdx, disk-expand, disk-shrink, trim, windows-server]
level: practitioner
status: docs-checked
description: "Grow and shrink VHDX files online with Resize-VHD, extend the guest volume, and reclaim space from dynamic disks with TRIM and Optimize-VHD."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/resize-vhd
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/optimize-vhd
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resize and compact VHDX

**Goal:** change a virtual disk's size without downtime and give space back to the host.

## Grow (online for VHDX on a SCSI controller)
```powershell
Resize-VHD -Path <VM_DIR>\app01-data.vhdx -SizeBytes 300GB
```
Then inside the guest:
```powershell
Update-HostStorageCache
Resize-Partition -DriveLetter E -Size (Get-PartitionSupportedSize -DriveLetter E).SizeMax
```
Linux: grow the partition and then the file system with your distribution's tools.

## Shrink
1. Shrink the guest partition first (Disk Management or `Resize-Partition`).
2. `Resize-VHD -Path ... -ToMinimumSize` or an explicit `-SizeBytes` not below the disk's `MinimumSize` property.
Shrinking works for VHDX only, and fails if it would go below `MinimumSize`.

## Compact dynamic disks
Deleted guest data stays allocated in the VHDX until reclaimed.
1. `Resize-VHD` does not remove empty blocks from a dynamic disk; use `Optimize-VHD`. Trim the free space inside the guest first (`Optimize-Volume -DriveLetter E -ReTrim` on Windows).
2. Compact with the disk not attached, or attached read-only (Full and Quick modes require the read-only attach; the default mode for VHDX is Quick):
```powershell
Stop-VM app01
Mount-VHD -Path <VM_DIR>\app01-data.vhdx -ReadOnly
Optimize-VHD -Path <VM_DIR>\app01-data.vhdx -Mode Full
Dismount-VHD -Path <VM_DIR>\app01-data.vhdx
```

## Gotchas
- Disks on an IDE controller (Gen 1 boot disks) cannot be resized while the VM is online; SCSI disks can.
- `Optimize-VHD` does not work on fixed disks.
- A compact can succeed without reducing the file size if no optimization is possible.

## Verify
`Get-VHD` shows the new `Size`, the guest sees the full volume, and after compaction `FileSize` dropped.

## Checked

Checked 2026-10-26 against the Windows Server 2025 `Resize-VHD` and `Optimize-VHD` references. Confirmed: online resize on SCSI but not IDE, grow for VHD/VHDX and shrink for VHDX only, `-ToMinimumSize` and the `MinimumSize` limit, `Resize-VHD` does not reclaim empty blocks, `Optimize-VHD` modes (Full, Quick, Retrim, Pretrimmed, Prezeroed), read-only attach requirement, not for fixed disks. Corrected: the shrink limit is `MinimumSize` rather than "end of the last partition". Removed as undocumented: automatic TRIM/UNMAP shrinking, `fstrim`, `growpart`/`xfs_growfs` commands and the checkpoint resize restriction.

Method: documentation only; no commands were run.
