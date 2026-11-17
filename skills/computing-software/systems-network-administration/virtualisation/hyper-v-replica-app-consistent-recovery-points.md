---
id: computing-software.systems-network-administration.virtualisation.hyper-v-replica-app-consistent-recovery-points
name: hyper-v-replica-app-consistent-recovery-points
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [app-consistent-recovery-point, hyper-v-replica, vss, hyper-v]
level: practitioner
status: docs-checked
description: "Configure application-consistent Hyper-V Replica recovery points with VSS snapshot frequency, choose them at failover, and fix VSS failures that stop them."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmreplication
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/get-vmsnapshot
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-virtual-machines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App-consistent recovery points with VSS

**Goal:** replica recovery points that databases and applications recover from cleanly, not just crash-consistent ones.

## Point types
- **Latest point**: replication cycles run every 30 s, 5 min or 15 min; by default only the latest recovery point is kept.
- **Additional hourly points**: up to 24 can be kept (`RecoveryHistory`). With VSS integration, some of them are application-consistent for VSS-aware applications such as SQL Server (`VSSSnapshotFrequencyHour`, in hours).

## Configure
```powershell
Set-VMReplication -VMName sql01 -RecoveryHistory 24 -VSSSnapshotFrequencyHour 4
Get-VMReplication -VMName sql01 | Format-List *
```
`VSSSnapshotFrequencyHour` applies only when `RecoveryHistory` is not zero, and must not be set when extending replication from the replica VM.
Hyper-V Manager: Replication settings -> *Recovery Points* -> *Create additional hourly recovery points* + *Volume Shadow Copy Service (VSS) snapshot frequency*.

Requirement: VSS-aware applications in the guest (the replica stores hourly points; storing more of them needs more storage and processing on the replica).

## At failover
Choose a recovery point marked *Application-consistent* in the failover dialog, or in PowerShell:
```powershell
Get-VMSnapshot -VMName sql01 -SnapshotType AppConsistentReplica | Select Name, CreationTime   # on the replica server; type Replica lists the other points
Start-VMFailover -VMName sql01 -VMRecoverySnapshot (Get-VMSnapshot -VMName sql01 -Name '<app-consistent point>')
Complete-VMFailover -VMName sql01
```

## Gotchas
- `Get-VMSnapshot -SnapshotType` distinguishes `Replica` from `AppConsistentReplica`; filter on the wrong type and the point you want is not listed.
- More recovery history needs more storage and processing resources on the replica.

## Verify
`Get-VMSnapshot -SnapshotType AppConsistentReplica` on the replica lists recent points; a test failover to one brings the database online without recovery warnings.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: RecoveryHistory (up to 24 points), VSSSnapshotFrequencyHour semantics, the 30 s/5 min/15 min frequencies, the Replica and AppConsistentReplica snapshot types, Start-VMFailover -VMRecoverySnapshot and Complete-VMFailover. Removed because no documentation page confirmed them: the VSS writer, shadow-storage and integration-service troubleshooting list, the Linux VSS daemon remark and the I/O claims.
Method: documentation only; no commands were run.
