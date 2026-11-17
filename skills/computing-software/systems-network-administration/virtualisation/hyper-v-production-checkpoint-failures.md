---
id: computing-software.systems-network-administration.virtualisation.hyper-v-production-checkpoint-failures
name: hyper-v-production-checkpoint-failures
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [production-checkpoint-failure, production-checkpoint, hyper-v-checkpoint, vss, integration-services, hyper-v]
level: advanced
status: docs-checked
description: "Fix Hyper-V production checkpoint failures: guest VSS writers, the backup integration service, Linux freeze daemon, disk space, and choosing ProductionOnly vs fallback."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/checkpoints
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vm
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/manage-hyper-v-integration-services
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-feature-compatibility-by-generation-and-guest
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Production checkpoint failures

A production checkpoint uses the Volume Shadow Copy Service (Windows) or a file system freeze (Linux) to take a data-consistent checkpoint, with no memory state. With the `Production` type, a failure falls back to a standard checkpoint; with `ProductionOnly` the operation fails instead.

## Check the mode
```powershell
Get-VM app01 | Select Name, CheckpointType
Set-VM app01 -CheckpointType ProductionOnly     # fail instead of falling back
```
Types: `Disabled` (blocks checkpoints), `Standard`, `Production` (falls back to standard), `ProductionOnly`.

## Causes to check
| Check | Command / fix |
|---|---|
| VSS integration service enabled | `Get-VMIntegrationService -VMName app01` shows `VSS` Enabled with status OK; `Enable-VMIntegrationService -VMName app01 -Name 'VSS'` |
| Guest VSS requestor service (Windows) | in the guest, the `vmicvss` service ("Hyper-V Volume Shadow Copy Requestor") is running |
| Linux guest | the `hv_vss_daemon` process is running (required for live Linux backups) |
| Integration services version | keep guest integration components current (Windows Update for Windows guests) |

## Domain controllers
Hyper-V lists domain controllers as supported only when using production checkpoints, so use `ProductionOnly` on DC guests rather than allowing a fallback to standard checkpoints.

## Verify
`Checkpoint-VM -Name app01 -SnapshotName test` succeeds with type `ProductionOnly`; remove the test checkpoint with `Remove-VMCheckpoint`.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: the four CheckpointType values and fallback behaviour, the VSS integration service and vmicvss service names, the Linux hv_vss_daemon requirement, and the domain-controller production-checkpoint-only support statement. Removed because no documentation page confirmed them: the error-message text, vssadmin checks, shadow-storage percentage, unsupported-disk list, host event-log names, backup-software remarks and VM-GenerationID claim.
Method: documentation only; no commands were run.
