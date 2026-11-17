---
id: computing-software.systems-network-administration.windows-server.clustered-iscsi-target-server
name: clustered-iscsi-target-server
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, iscsi, clustered-iscsi-target, iscsi-target-server, failover-clustering, high-availability]
level: advanced
status: docs-checked
description: "Build a highly available iSCSI Target Server role on a failover cluster: shared disk, the clustered role, virtual disks on cluster storage and failover testing."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/iscsi/iscsi-target-server
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/add-clusteriscsitargetserverrole
  - https://learn.microsoft.com/en-us/powershell/module/iscsitarget/new-iscsiservertarget
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Highly available iSCSI Target Server on a cluster

A standalone iSCSI Target Server is a single point of failure. Clustered, the target role (IP, name, iSCSI
virtual disks) fails over between nodes.

## Prerequisites
- 2+ node failover cluster with shared storage (the iSCSI Target Server docs name Fibre Channel hardware or a SAS storage array).
- `FS-iSCSITarget-Server` feature on every node.
```powershell
Invoke-Command -ComputerName NODE1,NODE2 { Install-WindowsFeature FS-iSCSITarget-Server }
```

## Create the clustered role
Name the role `ISCSI01`, give it a static IP and a cluster disk for the virtual disks:
```powershell
Add-ClusteriSCSITargetServerRole -Name ISCSI01 -Storage 'Cluster Disk 2' -StaticAddress 10.30.0.50
```

## Virtual disks and targets (on the owner node)
```powershell
New-IscsiVirtualDisk -Path '<CSV_DISK>:\iSCSIVirtualDisks\sql-data.vhdx' -SizeBytes 500GB -ComputerName ISCSI01
New-IscsiServerTarget -TargetName sql-cluster -InitiatorIds 'IQN:iqn.1991-05.com.microsoft:sql01.ad.example.com' -ComputerName ISCSI01
Add-IscsiVirtualDiskTargetMapping -TargetName sql-cluster -Path '<CSV_DISK>:\iSCSIVirtualDisks\sql-data.vhdx' -ComputerName ISCSI01
```
`<CSV_DISK>:` is the clustered disk owned by the role. `New-IscsiServerTarget` also has a `-ClusterGroupName` parameter.

## Initiators
Connect to the role IP, enable MPIO if multiple paths, and set persistent connections (see mpio-for-iscsi and
iscsi-initiator-persistent-connections). Add CHAP if required.

## Failover test
Move the role (`Move-ClusterGroup ISCSI01 -Node NODE2`) during I/O; initiators should pause briefly and resume.

## Verify
- [ ] Role moves between nodes with initiator sessions reconnecting and no I/O errors in the initiator's System log.

## Checked

Confirmed 2026-10-25 against the iSCSI Target Server overview (high availability needs a cluster with Fibre Channel or SAS shared storage; repository last commit 2026-10-23) and the Windows Server 2025 PowerShell reference: Add-ClusteriSCSITargetServerRole (Name, Storage, StaticAddress), New-IscsiVirtualDisk (Path, SizeBytes, ComputerName), New-IscsiServerTarget (TargetName, InitiatorIds in IdType:Value form such as IQN:..., ClusterGroupName), Add-IscsiVirtualDiskTargetMapping. Removed the unconfirmed initiator timeout, S2D lab claim and Failover Cluster Manager click path.

Method: documentation only; no commands were run.
