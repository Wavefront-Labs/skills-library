---
id: computing-software.systems-network-administration.windows-server.s2d-health-service-and-performance-history
name: s2d-health-service-and-performance-history
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-spaces-direct, s2d, health-service, get-healthfault, performance-history, get-clusterperf, storage-health-report, monitoring]
level: advanced
status: docs-checked
description: "Monitor S2D with the Health Service: Get-HealthFault, health reports, performance history with Get-ClusterPerf, and Health Service settings."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/health-service-faults
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/health-service-reports
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/performance-history
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# S2D Health Service and performance history

The Health Service runs on any cluster with S2D enabled. It aggregates faults, metrics and
history; Windows Admin Center reads the same data.

## Current faults
```powershell
Get-HealthFault | Select FaultingObjectDescription,FaultType,PerceivedSeverity,Reason,RecommendedActions | fl
Get-StorageSubSystem Cluster* | Debug-StorageSubSystem
```
Each fault carries a reason and a recommended action (for example, an unsupported drive is quarantined and the action is to
replace it with supported hardware).

## Live report
```powershell
Get-StorageSubSystem Cluster* | Get-StorageHealthReport -Count 1
Get-Volume -FileSystemLabel VMs01 | Get-StorageHealthReport
```
The report gives a curated list of essential metrics, aggregated across nodes, for the cluster, a node or a volume.

## Performance history (2019+)
New in Windows Server 2019, collected by default and stored in an auto-created volume named `ClusterPerformanceHistory`
(about 10 GB). `Get-ClusterPerf` is the alias of `Get-ClusterPerformanceHistory`.
```powershell
Get-ClusterNode NODE1 | Get-ClusterPerf
Get-PhysicalDisk -SerialNumber <serial> | Get-ClusterPerf -PhysicalDiskSeriesName 'PhysicalDisk.Latency.Average' -TimeFrame LastDay
Get-Volume -FriendlyName VMs01 | Get-ClusterPerf -VolumeSeriesName 'Volume.IOPS.Total' -TimeFrame LastWeek
```
Timeframes: LastHour (10 s samples), LastDay, LastWeek, LastMonth, LastYear (up to one year retained, with diminishing
granularity). Performance history is enabled by default; `Start-ClusterPerformanceHistory` re-enables it and
`Stop-ClusterPerformanceHistory -DeleteHistory` stops it and deletes existing data.

## Settings
```powershell
Get-StorageSubSystem Cluster* | Get-StorageHealthSetting
Get-StorageSubSystem Cluster* | Set-StorageHealthSetting -Name 'System.Storage.PhysicalDisk.AutoPool.Enabled' -Value True
```
The Health Service also quarantines drives with unsupported hardware or firmware (UnsupportedHardware and
UnsupportedFirmware faults).

## Gotchas
- Faults are not pushed anywhere by themselves: poll `Get-HealthFault` or forward events to your monitoring.

## Verify
- [ ] `Get-HealthFault` empty in steady state.
- [ ] `Get-ClusterPerf` returns data.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (health-service-faults, health-service-reports, performance-history and the drive and volume series pages; repository last commit 2026-10-23): Debug-StorageSubSystem for faults, Get-StorageHealthReport for cluster, node and volume reports, Get-ClusterPerf alias and -TimeFrame values with 10-second LastHour samples, one-year retention, ClusterPerformanceHistory volume of about 10 GB, series names physicaldisk.latency.average and volume.iops.total, Start-/Stop-ClusterPerformanceHistory -DeleteHistory, and the UnsupportedHardware and UnsupportedFirmware faults. Removed the unconfirmed capacity threshold setting name, retire-drive advice and the Health Operational event channel advice.

Method: documentation only; no commands were run.
