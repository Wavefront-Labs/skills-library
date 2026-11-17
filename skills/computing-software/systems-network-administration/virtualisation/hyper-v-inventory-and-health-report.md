---
id: computing-software.systems-network-administration.virtualisation.hyper-v-inventory-and-health-report
name: hyper-v-inventory-and-health-report
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v-inventory-report, hyper-v, reporting, powershell, health-check]
level: practitioner
status: docs-checked
description: "Build a PowerShell inventory and health report for Hyper-V hosts and clusters: VM sizing, disks, checkpoints, integration services, replication and CSV capacity."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/get-vm
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/get-vhd
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/get-vmsnapshot
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/get-clustersharedvolume
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V inventory and health report

**Goal:** one report that answers "what runs where, how big is it, and what needs attention".

## Script
Property names below are those exposed by the VM, VHD, snapshot and CSV objects on current Windows Server; confirm
them on your version with `Get-VM | Get-Member` (and the same for the other objects) before relying on the report.
```powershell
$hosts = (Get-ClusterNode -Cluster HVCL01).Name          # or a list of standalone hosts
$vms = foreach ($h in $hosts) { Get-VM -ComputerName $h }

$inv = foreach ($vm in $vms) {
  $disks = Get-VMHardDiskDrive -VM $vm | ForEach-Object { Get-VHD -ComputerName $vm.ComputerName -Path $_.Path }
  [pscustomobject]@{
    Host = $vm.ComputerName; VM = $vm.Name; State = $vm.State; Gen = $vm.Generation; Version = $vm.Version
    vCPU = $vm.ProcessorCount; MemGB = [math]::Round($vm.MemoryStartup/1GB,1); DynMem = $vm.DynamicMemoryEnabled
    DiskGB = [math]::Round(($disks | Measure-Object Size -Sum).Sum/1GB)
    UsedGB = [math]::Round(($disks | Measure-Object FileSize -Sum).Sum/1GB)
    Checkpoints = @(Get-VMSnapshot -VM $vm).Count
    OldestCheckpoint = (Get-VMSnapshot -VM $vm | Sort CreationTime | Select -First 1).CreationTime
    ICState = $vm.IntegrationServicesState; Heartbeat = $vm.Heartbeat
    Replication = $vm.ReplicationHealth; Uptime = $vm.Uptime
  }
}
$inv | Export-Csv hv-inventory.csv -NoTypeInformation

Get-ClusterSharedVolume -Cluster HVCL01 | ForEach-Object {
  $p = $_.SharedVolumeInfo.Partition
  [pscustomobject]@{CSV=$_.Name; SizeGB=[math]::Round($p.Size/1GB); FreePct=[math]::Round($p.PercentFree,1)}
} | Export-Csv hv-csv.csv -NoTypeInformation
```

## Health rules to flag
Thresholds are suggestions for you to tune, not Microsoft limits.
- Old checkpoints (differencing-disk growth and merge risk).
- Integration services not up to date; heartbeat not OK on running VMs.
- Replication health Warning or Critical.
- Low CSV free space.
- VM configuration version below the cluster's current version after a rolling upgrade.
- Hosts: committed memory against physical memory, and whether the VMs would fit with one node down.

## Delivery
Run as a scheduled task under a group managed service account; render HTML with `ConvertTo-Html -Fragment` and mail
it, or feed your monitoring system.

## Verify
VM count matches `Get-ClusterGroup | Where GroupType -eq VirtualMachine`; flagged items match manual spot checks.

## Checked

Date checked: 2026-10-27. Documentation: Get-VM, Get-VHD, Get-VMSnapshot and Get-ClusterSharedVolume reference pages (Windows Server 2025 docset).
Confirmed: the cmdlets and the -ComputerName and -Cluster parameters used. The reference pages do not list the object property names, so the skill tells readers to verify them with Get-Member; thresholds are labelled as suggestions.

Method: documentation only; no commands were run.
