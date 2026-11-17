---
id: computing-software.systems-network-administration.virtualisation.hyper-v-replica-extended-replication-and-recovery-points
name: hyper-v-replica-extended-replication-and-recovery-points
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, hyper-v-replica, extended-replication, recovery-points, recovery-history, vss-snapshot-frequency, app-consistent, windows-server]
level: advanced
status: docs-checked
description: "Configure Hyper-V Replica recovery history, app-consistent VSS recovery points, and extended (chained) replication to a third site, with their storage and frequency limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-virtual-machines
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/enable-vmreplication
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmreplication
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/get-vmsnapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extended replication and recovery points

## Recovery points
By default only the latest replicated state is kept. Keep history:
```powershell
Set-VMReplication -VMName app01 -RecoveryHistory 24 -VSSSnapshotFrequencyHour 4
```
- `RecoveryHistory`: additional recovery points to store on the replica (up to 24).
- `VSSSnapshotFrequencyHour`: VSS snapshot frequency in hours; it needs a non-zero `RecoveryHistory` and must not be set when extending replication from the replica VM.
- Additional recovery points need more storage and processing resources on the replica.

Choose a point on failover:
```powershell
Get-VMSnapshot -VMName app01 -SnapshotType Replica
Get-VMSnapshot -VMName app01 -SnapshotType AppConsistentReplica
```

## Extended replication (A -> B -> C)
Run on the replica server B, after primary replication is healthy (the `Extend Replication` action in the management tools is the documented route):
```powershell
Enable-VMReplication -VMName app01 -ReplicaServerName 'drsite-c.corp.example' -ReplicaServerPort 443 `
  -AuthenticationType Certificate -CertificateThumbprint $thumb -ReplicationFrequencySec 900
Start-VMInitialReplication -VMName app01
```
- Extended replication frequency can only be 5 or 15 minutes (30 seconds is not supported).
- You cannot choose which virtual hard disks to replicate: the disks replicated to the first replica server are used.
- Recovery points on the extended link are configured when you extend (Hyper-V Manager offers the same additional-recovery-point options).

## Verify
`Get-VMReplication -VMName app01` on server C shows `Replicating`, and the replica holds the expected number of recovery points.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: RecoveryHistory up to 24, VSSSnapshotFrequencyHour rules, extended replication to a third host, extended frequency limited to 5 or 15 minutes, the fixed disk set, and the Replica and AppConsistentReplica snapshot types. Removed because no documentation page confirmed them: the 4-hour VSS rule of thumb, resync-on-history-change remark, and the per-AVHDX storage claim.
Method: documentation only; no commands were run.
