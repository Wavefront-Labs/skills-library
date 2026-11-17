---
id: computing-software.systems-network-administration.virtualisation.hyper-v-resource-metering
name: hyper-v-resource-metering
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [resource-metering, measure-vm, hyper-v-powershell, chargeback, capacity-planning, hyper-v]
level: practitioner
status: docs-checked
description: "Use Hyper-V resource metering for chargeback and right-sizing: enable per VM or pool, Measure-VM fields, network metering ACLs, save interval, export and reset."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/measure-vm
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/enable-vmresourcemetering
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/reset-vmresourcemetering
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmhost
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/add-vmnetworkadapteracl
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/measure-vmresourcepool
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hyper-V resource metering

Built-in usage accounting per VM or resource pool: average processor usage (MHz), average/min/max memory (MB), total disk allocation, hard-disk metrics and metered network traffic (MB).

## Enable and read
```powershell
Get-VM | Enable-VMResourceMetering
Set-VMHost -ResourceMeteringSaveInterval 01:00:00      # how often the host saves usage data (1 to 24 hours)
Measure-VM -VMName sql01 | Format-List *
Get-VM | Measure-VM | Select VMName, MeteringDuration, AverageProcessorUsage, AverageMemoryUsage, MaximumMemoryUsage, TotalDiskAllocation,
  @{n='NetInMB';e={($_.NetworkMeteredTrafficReport | ? Direction -eq Inbound | Measure TotalTraffic -Sum).Sum}}
```
Values cover the period in `MeteringDuration`. Data exists only after metering is enabled. Disks on virtual Fibre Channel and SR-IOV network adapters are not reported. With static memory, average, minimum and maximum memory all equal the configured amount.

## Billing period workflow
```powershell
Get-VM | Measure-VM | Export-Csv "<REPORT_DIR>\metering-$(Get-Date -f yyyyMM).csv" -NoTypeInformation
Get-VM | Reset-VMResourceMetering      # deletes the data collected so far; collection continues
```
Schedule monthly via Task Scheduler on each host (or centrally with `-ComputerName`).

## Resource pools (aggregate by tenant)
```powershell
New-VMResourcePool -Name TenantA -ResourcePoolType Processor,Memory,Ethernet,VHD -Paths "<VM_DIR>\TenantA"
Set-VMProcessor -VMName a-web01 -ResourcePoolName TenantA   # processor pool (Set-VM has no -ResourcePoolName)
Set-VMMemory -VMName a-web01 -ResourcePoolName TenantA      # memory pool
Enable-VMResourceMetering -ResourcePoolName TenantA -ResourcePoolType Memory
Measure-VMResourcePool -Name TenantA -ResourcePoolType Memory
```

## Network metering by destination
Port ACLs with `-Action Meter` (must be IP-based, so give `-RemoteIPAddress` or `-LocalIPAddress`) split traffic, for example internet vs internal. Configure them before enabling metering; if none exist, enabling metering creates ACLs that measure total traffic:
```powershell
Add-VMNetworkAdapterAcl -VMName a-web01 -RemoteIPAddress 10.0.0.0/8 -Direction Both -Action Meter
Add-VMNetworkAdapterAcl -VMName a-web01 -RemoteIPAddress 0.0.0.0/0 -Direction Both -Action Meter
```

## Gotchas
- Processor usage is reported in MHz, not %: compare with host core speed for sizing.
- For time-series monitoring use performance counters or SCOM/Prometheus; metering is
  for period totals.

## Verify
`Measure-VM` returns non-zero values a day after enabling; monthly CSV produced and
counters reset afterwards.

## Checked

Checked 2026-10-26 against the Windows Server 2025 Hyper-V cmdlet references for `Measure-VM`, `Enable-VMResourceMetering`, `Reset-VMResourceMetering`, `Measure-VMResourcePool`, `New-VMResourcePool`, `Set-VMHost` and `Add-VMNetworkAdapterAcl`. Wrong in the earlier draft: the report property names (the real ones are AverageProcessorUsage, AverageMemoryUsage, MaximumMemoryUsage, TotalDiskAllocation; AvgCPU(Mhz) and TotalDisk(M) are display columns only), the `AggregatedAverageNormalizedIOPS` property and "8 KB normalised" figure are not documented, `ResourceMeteringSaveInterval` is a 1 to 24 hour setting, and the live-migration data claim was removed as undocumented.

Method: documentation only; no commands were run.
