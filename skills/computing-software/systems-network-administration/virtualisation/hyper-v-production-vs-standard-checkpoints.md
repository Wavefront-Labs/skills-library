---
id: computing-software.systems-network-administration.virtualisation.hyper-v-production-vs-standard-checkpoints
name: hyper-v-production-vs-standard-checkpoints
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, standard-checkpoint, production-checkpoint, checkpoint-vm, checkpoint-type, vss, windows-server]
level: practitioner
status: docs-checked
description: "Pick production or standard checkpoints in Hyper-V, set the checkpoint type per VM, and know what each captures (VSS-consistent disk vs saved memory state)."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/checkpoints
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vm
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/checkpoint-vm
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/manage-hyper-v-integration-services
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Production vs standard checkpoints

**Goal:** take checkpoints that restore to a supportable state.

| | Production | Standard |
|---|---|---|
| Mechanism | Volume Shadow Copy Service (Windows) or file system freeze (Linux) inside the guest; no memory state is saved | Snapshot of the VM and its memory state at the moment of the checkpoint |
| Data consistency | Data-consistent | Can cause data consistency problems with systems that replicate between nodes, such as Active Directory |
| Default | Yes, production checkpoints are selected by default | No |

## Set and take
```powershell
Set-VM -Name app01 -CheckpointType Production         # falls back to Standard if a production checkpoint cannot be taken
Set-VM -Name app01 -CheckpointType ProductionOnly     # fail instead of falling back
Set-VM -Name lab01 -CheckpointType Standard
Checkpoint-VM -Name app01 -SnapshotName 'pre-patch-2026-10'
Get-VMCheckpoint -VMName app01
Restore-VMCheckpoint -VMName app01 -Name 'pre-patch-2026-10' -Confirm:$false
Remove-VMCheckpoint  -VMName app01 -Name 'pre-patch-2026-10'    # Hyper-V merges the .avhdx into the .vhdx
```

## When production checkpoints fail
- VSS integration service disabled: list with `Get-VMIntegrationService -VMName app01` (the service is named `VSS`) and enable it with `Enable-VMIntegrationService -VMName app01 -Name 'VSS'`.
- Linux guest without the `hv_vss_daemon` (it is required for live Linux backups).

## Gotchas
- `Production` falls back to a standard checkpoint when the production one fails; use `ProductionOnly` when consistency matters (the operation then fails instead).
- A checkpoint is not a full backup.

## Verify
`Get-VM app01 | Select Name, CheckpointType` shows the intended type, and a test checkpoint with `ProductionOnly` succeeds.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: production versus standard checkpoint mechanism, production checkpoints being the default, the Disabled/Standard/Production/ProductionOnly values and their fallback behaviour, the Checkpoint-VM -SnapshotName parameter, the Get/Restore/Remove-VMCheckpoint cmdlets, the VSS integration service name and the hv_vss_daemon requirement on Linux. Removed because no documentation page confirmed them: the cold-boot behaviour on apply, the DC/clustered/replicated-database support statement, and the I/O-slowdown remark.
Method: documentation only; no commands were run.
