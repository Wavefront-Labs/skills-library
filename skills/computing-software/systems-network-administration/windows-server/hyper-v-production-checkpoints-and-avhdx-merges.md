---
id: computing-software.systems-network-administration.windows-server.hyper-v-production-checkpoints-and-avhdx-merges
name: hyper-v-production-checkpoints-and-avhdx-merges
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, production-checkpoints, avhdx, hyper-v-checkpoints, standard-checkpoints, checkpoint-merge, differencing-disks]
level: practitioner
status: gated
description: "Use Hyper-V checkpoints safely: production vs standard checkpoints, how AVHDX differencing chains and merges work, and cleaning orphaned AVHDX files."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/choose-between-standard-or-production-checkpoints-in-hyper-v
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/enable-or-disable-checkpoints-in-hyper-v
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/checkpoint-vm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Production vs standard checkpoints and merges

## Types
| | Production checkpoint (default since 2016) | Standard checkpoint |
|---|---|---|
| Mechanism | VSS in Windows guests / File System Freeze in Linux guests | VM and memory state |
| Consistency | data-consistent backup of the VM | VM plus memory state at the time |
| Safe for | Learn's checkpoint-type page gives the guidance; check it for databases and domain controllers | test/dev; check Learn's guidance before restoring running DC/database state |
```powershell
Set-VM -Name app01 -CheckpointType Production          # ProductionOnly = fail rather than fall back to standard
Checkpoint-VM -Name app01 -SnapshotName "pre-patch-2026-10"
Get-VMSnapshot -VMName app01
Restore-VMSnapshot -VMName app01 -Name "pre-patch-2026-10" -Confirm:$false
Remove-VMSnapshot -VMName app01 -Name "pre-patch-2026-10"    # triggers merge
```
With `-CheckpointType ProductionOnly`, if the production checkpoint fails a standard checkpoint is not created; use it when a fallback to standard is unacceptable.

## How the files work
Taking a checkpoint makes the current VHDX read-only and creates an **.avhdx** differencing disk; all new writes go there. Each further checkpoint adds another level.
- Checkpoints are stored as .avhdx files next to the VM's .vhdx files; deleting a checkpoint merges the .avhdx back (per Learn), which also frees host space.
- Long chains and forgotten checkpoints cost I/O and space; monitor them.

## Never do this
- Delete .avhdx files manually in Explorer, or edit the VM to point at the parent VHDX: you lose all writes since the checkpoint and can corrupt the chain.
- Keep checkpoints for weeks as a "backup": they're on the same storage, break when the chain breaks, and degrade performance.

## Orphaned AVHDX / failed merges
Backup software uses recovery checkpoints; failures can leave AVHDX files the GUI doesn't show.
```powershell
Get-VM app01 | Get-VMHardDiskDrive | Select Path            # attached .avhdx? the chain is still active
Get-VHD -Path '<VMPath>\app01\disk_ABC.avhdx' | Select Path, ParentPath, FileSize
Get-VMSnapshot -VMName app01 -SnapshotType Recovery | Remove-VMSnapshot
```
If no checkpoint objects exist but the VM still runs on an AVHDX: shut down the VM, then merge with `Merge-VHD -Path child.avhdx -DestinationPath parent.vhdx` in order from newest to oldest (or Hyper-V Manager > Edit Disk > Merge), then reattach the parent. Back up the files first.

## Policy
- Short-lived checkpoints only (hours to a couple of days) around changes; monitor for checkpoints older than N days (`Get-VMSnapshot | Where-Object CreationTime -lt (Get-Date).AddDays(-3)`).
- Keep free space on the volume for merges.

## Verify
- [ ] No VM has checkpoints older than policy; attached disks are .vhdx, not .avhdx, outside maintenance.
- [ ] A production checkpoint of a database VM completes without falling back (use ProductionOnly to test).

## Checked
2026-10-28. Confirmed on Learn (production vs standard checkpoints, checkpoint-vm): Production uses VSS or File System Freeze on Linux,
Standard captures memory state, `Set-VM -CheckpointType ProductionOnly` does not fall back, checkpoints are .avhdx files
and deleting merges them. Removed as unconfirmed: the DC/VM-GenerationID safety statement, restore-behaviour wording,
Paused-Critical, live-merge detail, the merge free-space sizing. Remaining PowerShell cmdlet usage (Get-VMSnapshot,
Merge-VHD recovery recipe, Recovery snapshot type, Get-VHD) follows the cmdlet names but was not checked against their
module pages (gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
