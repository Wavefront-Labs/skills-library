---
id: computing-software.systems-network-administration.virtualisation.hyper-v-storage-spaces-direct-hyperconverged
name: hyper-v-storage-spaces-direct-hyperconverged
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [s2d-hyper-converged, storage-spaces-direct, hyper-v, failover-cluster, storage]
level: advanced
status: docs-checked
description: "Build and operate a hyper-converged Hyper-V cluster on Storage Spaces Direct: validation, enable S2D, volume resiliency, reserve capacity, maintenance and health checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/deploy-storage-spaces-direct
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/plan-volumes
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/storage-spaces-direct-hardware-requirements
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/quorum
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/nested-resiliency
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/troubleshooting-storage-spaces
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/health-service-reports
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Spaces Direct for hyper-converged Hyper-V

**Goal:** Hyper-V and software-defined storage on the same nodes, with resilient volumes and safe maintenance.

## Prerequisites
- Minimum two servers, maximum 16; Windows Server Datacenter edition; drives behind an SAS HBA, or a RAID controller that passes SAS devices straight through (RAID controllers without pass-through and SAN storage are not supported); drives unpartitioned.
- At least 10 GbE between servers, RDMA recommended (iWARP or RoCE).

## Deploy
```powershell
Test-Cluster -Node hv01,hv02,hv03,hv04 -Include 'Storage Spaces Direct','Inventory','Network','System Configuration'
New-Cluster -Name HCI01 -Node hv01,hv02,hv03,hv04 -NoStorage -StaticAddress 10.0.0.60
Set-ClusterQuorum -Cluster HCI01 -CloudWitness -AccountName <storageacct> -AccessKey <key>
Enable-ClusterStorageSpacesDirect -CimSession HCI01
New-Volume -CimSession HCI01 -FriendlyName VMs01 -FileSystem CSVFS_ReFS -StoragePoolFriendlyName 'S2D*' -Size 4TB -ResiliencySettingName Mirror
```
Clear old disks before enabling (`Clear-Disk -RemoveData -RemoveOEM`).

## Resiliency
- 2 nodes: two-way mirror or nested resiliency (Windows Server 2019 and later, exactly two servers), with a witness (required).
- 3 nodes: three-way mirror (witness strongly recommended with 3 or 4 nodes).
- 4+ nodes: per volume, three-way mirror, dual parity or a mirror-accelerated parity mix (Microsoft's trade-off is performance vs capacity efficiency). From 5 nodes a witness adds no resiliency.
- Leave **reserve capacity** unallocated in the pool: one capacity drive per server, up to 4, so repairs can run after a drive failure.

## Maintenance
```powershell
Suspend-ClusterNode -Name hv02 -Drain -Wait
Get-StorageFaultDomain -Type StorageScaleUnit | Where-Object {$_.FriendlyName -eq 'hv02'} | Enable-StorageMaintenanceMode
Get-PhysicalDisk                              # OperationalStatus should show In Maintenance
# patch/reboot
Get-StorageFaultDomain -Type StorageScaleUnit | Where-Object {$_.FriendlyName -eq 'hv02'} | Disable-StorageMaintenanceMode
Resume-ClusterNode -Name hv02 -Failback Immediate
Get-StorageJob                                # wait for repairs to finish before the next node
```

## Health
```powershell
Get-StorageSubSystem Cluster* | Get-StorageHealthReport
Get-StorageSubSystem Cluster* | Debug-StorageSubSystem
Get-PhysicalDisk | Where HealthStatus -ne Healthy
Get-VirtualDisk | Select FriendlyName, HealthStatus, OperationalStatus
```

## Gotchas
- Check `Get-VirtualDisk` shows Healthy and `Get-StorageJob` is empty before draining the next node; Microsoft's shutdown procedure starts with the health check.
- Microsoft recommends limiting each volume to 64 TB, and mixed drive sizes across servers can strand capacity (drive symmetry page).

## Checked

Checked 2026-10-26 against MicrosoftDocs/windowsserverdocs storage-spaces pages (deploy, plan volumes, hardware requirements, quorum, nested resiliency, troubleshooting shutdown procedure, health service reports; latest commit 2026-10-23). Confirmed: 2 to 16 servers, Datacenter edition, 10 GbE minimum, `Test-Cluster` inclusion list, `New-Cluster -NoStorage`, `Enable-ClusterStorageSpacesDirect`, `New-Volume` parameters including `-ResiliencySettingName Mirror`, `Clear-Disk -RemoveData -RemoveOEM`, cloud witness cmdlet, reserve capacity guidance (one capacity drive per server, up to 4), `Get-StorageSubSystem Cluster* | Get-StorageHealthReport/Debug-StorageSubSystem`. Corrected: `Get-StorageScaleUnit` is not used in the docs (they pipe `Get-StorageFaultDomain -Type StorageScaleUnit` to Enable/Disable-StorageMaintenanceMode); nested resiliency exists from Windows Server 2019, not 2022; the "second node reboot takes volumes offline" and ReFS dedup remarks were unconfirmed and replaced with documented guidance.

Method: documentation only; no commands were run.
