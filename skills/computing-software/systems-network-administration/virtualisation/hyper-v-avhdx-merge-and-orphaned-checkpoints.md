---
id: computing-software.systems-network-administration.virtualisation.hyper-v-avhdx-merge-and-orphaned-checkpoints
name: hyper-v-avhdx-merge-and-orphaned-checkpoints
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, avhdx, checkpoint-merge, merge-vhd, orphaned-checkpoint, broken-chain, vhdx-recovery, windows-server]
level: advanced
status: docs-checked
description: "Fix Hyper-V AVHDX problems: stuck or failed checkpoint merges, VMs running on orphaned AVHDX files after backups, and manual Merge-VHD with permission repair."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/merge-vhd
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/virtualization/merge-checkpoints-with-many-differencing-disks
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/checkpoints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AVHDX merges and orphaned checkpoint recovery

**Goal:** get a VM back onto its base VHDX without losing the changes held in AVHDX files.

## Detect the problem
```powershell
Get-VMHardDiskDrive -VMName app01 | Select-Object Path            # ends in .avhdx?
Get-VMSnapshot -VMName app01                                      # empty -> orphaned AVHDX
Get-VMSnapshot -VMName app01 -SnapshotType Recovery               # leftover backup checkpoints
Get-VHD '<VM_DIR>\app01_6F3...avhdx' | Select-Object Path, ParentPath
```
If checkpoints are listed, delete them normally (`Remove-VMCheckpoint`); Hyper-V merges the differencing disks. Checkpoints left behind by third-party backup software can be missing from Hyper-V Manager while the differencing disks remain on disk.

## Manual merge (no checkpoint objects left)
1. Take a **file-level copy** of the whole VM folder first.
2. Shut down the VM.
3. Walk the chain from the newest disk to the base with `Get-VHD ... ParentPath`.
4. Merge (the chain must not be attached; `Merge-VHD` is an offline operation). Merging a child into an ancestor also merges the disks between them, and the merged-in child files are no longer valid:
```powershell
Merge-VHD -Path '<VM_DIR>\app01_6F3.avhdx' -DestinationPath '<VM_DIR>\app01.vhdx'
```
5. Repoint the VM:
```powershell
Set-VMHardDiskDrive -VMName app01 -ControllerType SCSI -ControllerNumber 0 -ControllerLocation 0 -Path '<VM_DIR>\app01.vhdx'
```

## Gotchas
- Never delete an AVHDX by hand (Microsoft: do not delete `.avhdx` files directly); it holds the changes since the checkpoint.
- Check `ParentPath` for every disk before merging; if the chain does not match, stop and restore from the copy.
- Backup software that leaves `Recovery` checkpoints has not cleaned up after a backup; fix the job, then remove them.

## Verify
`Get-VMHardDiskDrive` points to `.vhdx` files only, no `.avhdx` remain in the folder, and the guest's latest data is present.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: Merge-VHD being offline with -Path and -DestinationPath, merge of intermediates when merging to an ancestor, Get-VHD ParentPath chain walking, the Recovery snapshot type, checkpoints left by backup software being invisible in Hyper-V Manager, and the warning against deleting .avhdx files. Removed because no documentation page confirmed them: the icacls re-grant of the VM SID step, the free-space and speed remarks, and the event-log name.
Method: documentation only; no commands were run.
