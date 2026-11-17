---
id: computing-software.systems-network-administration.windows-server.physical-disk-health-and-reliability-counters
name: physical-disk-health-and-reliability-counters
category: computing-software
field: systems-network-administration
product: windows-server
tags: [storage-spaces, storagereliabilitycounter, get-physicaldisk, disk-health, s2d]
level: practitioner
status: docs-checked
description: "Monitor physical disk health in Storage Spaces: HealthStatus and OperationalStatus, Get-StorageReliabilityCounter wear and errors, and when to retire a disk."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/storage/get-storagereliabilitycounter
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/storage-spaces-states
  - https://learn.microsoft.com/en-us/powershell/module/storage/set-physicaldisk
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/health-service-faults
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Physical disk health and reliability counters

## Status at a glance
```powershell
Get-PhysicalDisk | Sort FriendlyName | Format-Table FriendlyName,SerialNumber,MediaType,Usage,HealthStatus,OperationalStatus,Size
```
| OperationalStatus | Meaning (Microsoft's drive states) |
|---|---|
| OK / In service | healthy; In service is internal housekeeping and should return to OK |
| Predictive failure | the drive reported it is close to failing; replace it |
| IO error / Transient error | temporary access error; if it does not return to OK try `Reset-PhysicalDisk`, then `Repair-VirtualDisk`; replace if it recurs |
| Lost communication | the drive is missing (health Warning) |
| Starting / Stopping maintenance mode, In maintenance mode | an administrator put the drive in maintenance mode; leave it with `Disable-StorageMaintenanceMode` |
| Abnormal latency | the Storage Spaces Direct Health Service measured the drive as slow; replace if it persists |
| Failed media / Device hardware failure | replace the drive |

## Reliability counters
```powershell
Get-PhysicalDisk | Get-StorageReliabilityCounter |
  Select DeviceId,Temperature,Wear,ReadErrorsUncorrected,WriteErrorsUncorrected,PowerOnHours |
  Format-Table -AutoSize
```
The cmdlet returns device temperature, errors, wear and time in use. Its documented counters include
ReadErrorsCorrected/Total/Uncorrected, WriteErrorsCorrected/Total/Uncorrected, Temperature and TemperatureMax, Wear,
PowerOnHours, StartStopCycleCount and LoadUnloadCycleCount. A counter can be blank (the documented example shows an
empty Wear), so a blank value means the device did not report it. Set your own replacement thresholds from the drive
vendor's guidance; Microsoft publishes none for Wear or error counts.

## Retire and replace
```powershell
$d = Get-PhysicalDisk -SerialNumber ABC123
$d | Set-PhysicalDisk -Usage Retired
Get-VirtualDisk | Repair-VirtualDisk -AsJob
Get-StorageJob                                    # wait until repair completes
Remove-PhysicalDisk -StoragePoolFriendlyName Pool01 -PhysicalDisks $d
```
Physically locate it first: `Enable-PhysicalDiskIdentification -FriendlyName <name>` blinks the LED.

## Automate
Schedule a daily check that alerts on non-OK disks and on your chosen counter thresholds. On Storage Spaces Direct the
Health Service raises faults you can list with `Get-StorageSubSystem Cluster* | Debug-StorageSubSystem`.

## Verify
- [ ] All disks OK, counters tracked; the replaced disk shows Usage AutoSelect and the pool is healthy after `Optimize-StoragePool`.

## Checked

2026-10-27. Documentation release: windowsserverdocs Storage Spaces health and operational states (current) and the Storage module references for Get-StorageReliabilityCounter, Set-PhysicalDisk, Remove-PhysicalDisk and Enable-PhysicalDiskIdentification (Windows Server 2022 docset), and the Health Service faults page. Confirmed drive operational states and actions, the Retired usage value, counter names and the blank-Wear example. Removed the wear and error thresholds, the ReadLatencyMax and WriteLatencyMax properties, the firmware and RAID visibility claim and Get-HealthFault (the faults page uses Debug-StorageSubSystem) as unconfirmed.

Method: documentation only; no commands were run.
