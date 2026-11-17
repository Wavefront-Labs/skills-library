---
id: computing-software.systems-network-administration.virtualisation.hyper-v-storage-qos-policies
name: hyper-v-storage-qos-policies
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, storage-qos, storage-qos-policy, iops-limit, new-storageqospolicy, sofs, csv, noisy-neighbour, windows-server]
level: advanced
status: docs-checked
description: "Control Hyper-V VM disk IOPS with Storage QoS: per-disk limits on standalone hosts, and dedicated or aggregated cluster policies with flow monitoring on CSV and SOFS."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-qos/storage-qos-overview
  - https://learn.microsoft.com/en-us/powershell/module/storageqos/new-storageqospolicy
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmharddiskdrive
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V Storage QoS policies

**Goal:** stop noisy-neighbour VMs from starving others and guarantee minimum IOPS to critical ones.

IOPS are **normalised to 8 KB**: any I/O of 8 KB or smaller counts as one normalised IO and larger I/Os count as multiple (a 64 KB I/O counts as 8).

## Standalone host (per virtual disk)
```powershell
Set-VMHardDiskDrive -VMName app01 -ControllerType SCSI -ControllerNumber 0 -ControllerLocation 1 `
  -MinimumIOPS 200 -MaximumIOPS 2000
```
`-MinimumIOPS` and `-MaximumIOPS` are normalised IOPS for the disk.

## Cluster policies (Scale-Out File Server or CSV, Windows Server 2016 and later)
```powershell
$gold  = New-StorageQosPolicy -Name Gold  -PolicyType Dedicated  -MinimumIops 500 -MaximumIops 5000
$batch = New-StorageQosPolicy -Name Batch -PolicyType Aggregated -MaximumIops 10000
Get-VM -Name sql* | Get-VMHardDiskDrive | Set-VMHardDiskDrive -QoSPolicyID $gold.PolicyId
```
- **Dedicated**: each disk gets the full min/max.
- **Aggregated**: all disks sharing the policy share the min/max.
- `New-StorageQosPolicy` also has `-MaximumIOBandwidth`. Name, MinimumIOPS, MaximumIOPS and MaximumIoBandwidth can be changed later; the policy type cannot.

## Monitor
```powershell
Get-StorageQosFlow | Sort-Object StorageNodeIOPS -Descending |
  Format-Table InitiatorName, FilePath, InitiatorIOPS, StorageNodeIOPS, Status -AutoSize
Get-StorageQosVolume | Format-Table Mountpoint, IOPS, Latency, Bandwidth
```
`Status = InsufficientThroughput` means a minimum cannot be met: the storage is oversubscribed.

## Gotchas
- If a policy is deleted before it is removed from a VM, the VM keeps running as if no policy applied and flows show `UnknownPolicyId`.
- Minimums that sum above what the storage can deliver guarantee nothing; size them from measured capacity.

## Verify
Run a load test on a limited VM and confirm `Get-StorageQosFlow` caps it at the policy maximum while others keep their minimum.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: normalised IOPS (8 KB), Dedicated and Aggregated policy types, New-StorageQosPolicy parameters, Set-VMHardDiskDrive -MinimumIOPS/-MaximumIOPS/-QoSPolicyID, Get-StorageQosFlow and Get-StorageQosVolume, flow status InsufficientThroughput and UnknownPolicyId, behaviour after deleting a policy, and that the policy type cannot be changed after creation. Removed as unconfirmed: the claim that the per-disk minimum is only an alert on standalone hosts.

Method: documentation only; no commands were run.
