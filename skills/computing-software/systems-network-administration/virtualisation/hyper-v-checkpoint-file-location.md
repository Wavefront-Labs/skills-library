---
id: computing-software.systems-network-administration.virtualisation.hyper-v-checkpoint-file-location
name: hyper-v-checkpoint-file-location
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [snapshot-file-location, hyper-v-checkpoint, avhdx, capacity-planning, hyper-v]
level: practitioner
status: docs-checked
description: "Know where Hyper-V checkpoint files really go (AVHDX beside the parent VHDX, state files in SnapshotFileLocation), plan space, and move checkpoint locations safely."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/checkpoints
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vm
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/move-vmstorage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checkpoint file location and space planning

## Where files go
| File | Location |
|---|---|
| `.avhdx` differencing disks | the same location as the VM's `.vhdx` files |
| checkpoint configuration files | the *Checkpoint File Location* (`SnapshotFileLocation`); default `%systemroot%\ProgramData\Microsoft\Windows\Hyper-V\Snapshots` |
```powershell
Get-VM app01 | Select ConfigurationLocation, SnapshotFileLocation
Get-VMHardDiskDrive -VMName app01 | Select Path
Get-VMCheckpoint -VMName app01 | Select Name, CreationTime
```
So moving SnapshotFileLocation to another volume does not move the differencing disks:
AVHDX growth still lands next to the VHDX files.

## Space planning
- Each checkpoint adds an AVHDX that grows with changes; Hyper-V merges it into the VHDX when you delete the checkpoint.
- Keep checkpoints short-lived and watch free space on the volumes that hold the VHDX files.

## Change the location
```powershell
Set-VM -Name app01 -SnapshotFileLocation "<VM_DIR>\Snapshots"
```
Hyper-V Manager: VM Settings -> Management -> Checkpoints (or Checkpoint File Location) -> enter the folder. To move the VM's files as a whole, use storage migration (`Move-VMStorage -VMName app01 -DestinationStoragePath <new>`).

## Gotchas
- Do not delete `.avhdx` files directly; delete the checkpoint so Hyper-V merges them.

## Verify
`Get-VMCheckpoint -VMName *` lists only the checkpoints you expect, and the VM volumes have free space for their growth.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: AVHDX files live beside the VHDX files, the default checkpoint configuration folder, the Set-VM -SnapshotFileLocation parameter, merge on checkpoint deletion, and the warning not to delete .avhdx files directly. Removed because no documentation page confirmed them: the Paused-Critical behaviour, memory-file size, the 15% alert threshold, and the claim that the location change applies only to new checkpoints.
Method: documentation only; no commands were run.
