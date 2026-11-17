---
id: computing-software.systems-network-administration.windows-server.hyper-v-replica-extended-and-recovery-points
name: hyper-v-replica-extended-and-recovery-points
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, hyper-v-replica, extended-replication, recovery-points, recovery-history, vss-snapshot, three-site-dr]
level: advanced
status: docs-checked
description: "Configure Hyper-V Replica recovery history, application-consistent recovery points and extended (chained) replication to a third site."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-overview
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-virtual-machines
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/enable-vmreplication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extended replication and recovery points

## Recovery points
- `-RecoveryHistory N` stores up to 24 additional hourly recovery points on the replica, besides the latest. More
  points need more storage and processing on the replica.
- `-VSSSnapshotFrequencyHour H` sets how often (in hours) VSS takes an application-consistent snapshot. Give it only
  when RecoveryHistory is not zero; it is zero when application-consistent replication is off.
```powershell
Set-VMReplication -VMName SQL01 -RecoveryHistory 12 -VSSSnapshotFrequencyHour 2
Get-VMSnapshot -VMName SQL01 -SnapshotType Replica | Select Name,CreationTime
```
Use VSS-based points for VSS-aware applications such as SQL Server. For multi-disk applications (data and log on
separate disks) add `-EnableWriteOrderPreservationAcrossDisks` to `Enable-VMReplication`.

## Extended replication (primary > replica > extended replica)
Replicates from the replica server on to a third Hyper-V host or cluster. Configure it from the replica host for a VM
that is already replicating (Windows Admin Center, Hyper-V Manager, Failover Cluster Manager, or PowerShell):
```powershell
Enable-VMReplication -VMName APP01 -ComputerName hv-dr01 -ReplicaServerName hv-dr2.partner.example.com `
  -ReplicaServerPort 443 -AuthenticationType Certificate -CertificateThumbprint <thumb> -ReplicationFrequencySec 900
Start-VMInitialReplication -VMName APP01 -ComputerName hv-dr01
```
- Extended replication supports only 5 or 15 minute frequency; 30 seconds is not offered.
- You cannot choose which disks replicate; the disks replicated to the first replica are used.
- The extended replica can use a different interval and its own recovery-point settings. Do not pass
  `-VSSSnapshotFrequencyHour` when extending from the replica VM.
- Use the port and authentication type configured on the extended replica host.

## Verify
- [ ] `Get-VMReplication -ComputerName hv-dr01` lists the extended relationship for the VM.
- [ ] `Get-VMSnapshot -SnapshotType Replica` on the replica shows the expected recovery points.

## Checked

2026-10-26 against the Windows Server docs (replication-overview, replication-virtual-machines; repository last commit 2026-10-23) and the Hyper-V module reference (Windows Server 2025): 24 hourly recovery points, VSS snapshot frequency rules, 5 or 15 minute frequency for extended replication, no disk selection, third-host topology, Enable-VMReplication parameters. Removed unconfirmed claims about Mode values, a single extended hop, the relation of extended to primary frequency, the Backup integration service requirement, storage sizing formula and the 50% log threshold.

Method: documentation only; no commands were run.
