---
id: computing-software.systems-network-administration.virtualisation.hyper-v-linux-production-checkpoints
name: hyper-v-linux-production-checkpoints
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [linux-production-checkpoint, production-checkpoint, hyper-v, linux]
level: practitioner
status: docs-checked
description: "Make production checkpoints work for Linux guests on Hyper-V: the VSS daemon, filesystem freeze, ProductionOnly policy, and common reasons they fall back to standard."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/checkpoints
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/manage-hyper-v-integration-services
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Production checkpoints for Linux guests

**Goal:** consistent checkpoints and backups of Linux VMs, without the saved-memory state of standard checkpoints.

## How it works
For Linux guests, a production checkpoint uses a file system freeze instead of VSS and does not save memory state. The `hv_vss_daemon` is required to create live Linux backups.

## Guest requirements
- Integration service *Backup (volume shadow copy)* enabled on the VM:
```powershell
Get-VMIntegrationService -VMName lnx01          # the service is named VSS
Enable-VMIntegrationService -VMName lnx01 -Name 'VSS'
```
- The `hv_vss_daemon` Linux integration daemon running in the guest (Microsoft shows it with `ps -ef | grep hv`); install the Hyper-V daemons package for your distribution.

## Policy
```powershell
Set-VM -VMName lnx01 -CheckpointType ProductionOnly   # fail instead of silently taking a standard checkpoint
Checkpoint-VM -Name lnx01 -SnapshotName pre-upgrade
```
With `Production` Hyper-V falls back to a standard checkpoint when a production checkpoint cannot be taken; `ProductionOnly` fails instead.

## Verify
`Get-VM lnx01 | Select Name, CheckpointType` shows `ProductionOnly`, and `Checkpoint-VM -Name lnx01 -SnapshotName test` succeeds.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: Linux production checkpoints use a file system freeze with no memory state, the hv_vss_daemon requirement, the VSS integration service name, and Production versus ProductionOnly fallback behaviour. Removed because no documentation page confirmed them: the per-distribution package and service names, the cause list for failed freezes, the application-consistency remarks and the log-name claims.
Method: documentation only; no commands were run.
