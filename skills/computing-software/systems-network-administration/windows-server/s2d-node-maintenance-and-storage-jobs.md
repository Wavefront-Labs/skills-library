---
id: computing-software.systems-network-administration.windows-server.s2d-node-maintenance-and-storage-jobs
name: s2d-node-maintenance-and-storage-jobs
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-spaces-direct, s2d, storage-maintenance-mode, get-storagejob, suspend-clusternode, drain-roles, storage-repair, patching, cluster-node-drain]
level: advanced
status: docs-checked
description: "Take an S2D node down safely: pre-checks, drain, storage maintenance mode, patch, resume, then wait for storage repair jobs before the next node."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/understand-storage-resync
  - https://learn.microsoft.com/en-us/powershell/module/storage/enable-storagemaintenancemode
  - https://learn.microsoft.com/en-us/powershell/module/storage/get-storagejob
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# S2D node maintenance and storage repair jobs

Rule: **one node at a time, and never start the next until every storage job has finished
and every virtual disk is Healthy.** Data on a node that is down is out of sync until the resync completes.

## Pre-checks
```powershell
Get-VirtualDisk | ? HealthStatus -ne Healthy     # must be empty
Get-StorageJob | ? JobState -ne Completed        # must be empty
Get-ClusterNode | Select Name,State              # all Up
```

## Take the node down
```powershell
Suspend-ClusterNode -Name NODE2 -Drain -Wait
Get-StorageScaleUnit -FriendlyName NODE2 | Enable-StorageMaintenanceMode
# patch, firmware, reboot
```
- While a device is in storage maintenance mode no I/O flows to it and other fault domains serve the I/O; the cmdlet
  refuses to enable it if that would take the last copy of data offline. Cluster-Aware Updating can wait for storage
  repair between nodes (`WaitForStorageRepairTimeoutMinutes`).
- If drain fails, fix the cause instead of forcing.

## Bring it back
```powershell
Get-StorageScaleUnit -FriendlyName NODE2 | Disable-StorageMaintenanceMode
Resume-ClusterNode -Name NODE2 -Failback Immediate
```

## Watch the resync
```powershell
while (Get-StorageJob | ? JobState -eq Running) {
  Get-StorageJob | Select Name,ElapsedTime,JobState,PercentComplete,IsBackgroundTask | ft; Start-Sleep 30 }
Get-VirtualDisk | Select FriendlyName,OperationalStatus,HealthStatus
```
- Storage jobs such as Regeneration show resync progress; rebalancing after adding drives or servers can be triggered with
  `Optimize-StoragePool`.
- While data is out of sync, the node's storage is flagged degraded (see the `ClusterNode.Storage.Degraded` performance series).

## Gotchas
- Drive firmware rollouts follow the same node-by-node procedure.
- On two-node clusters confirm the witness is online before starting.

## Verify
- [ ] Node Up and roles failed back.
- [ ] No running storage jobs and all virtual disks Healthy before the next node.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (understand-storage-resync, add-nodes and cluster OS rolling upgrade; repository last commit 2026-10-23) and the Windows Server 2025 PowerShell reference: Enable-StorageMaintenanceMode semantics (no I/O to the device, refused when it would take the last copy offline), Get-StorageJob fields and Regeneration example, Optimize-StoragePool rebalancing, Suspend-ClusterNode -Drain and Resume-ClusterNode -Failback, the CAU WaitForStorageRepairTimeoutMinutes parameter. Removed the unconfirmed OperationalStatus values, stuck-job diagnosis, job-name list beyond Regeneration and the claim that a second node down takes volumes offline.

Method: documentation only; no commands were run.
