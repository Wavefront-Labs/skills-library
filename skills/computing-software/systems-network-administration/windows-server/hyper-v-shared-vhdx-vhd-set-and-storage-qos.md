---
id: computing-software.systems-network-administration.windows-server.hyper-v-shared-vhdx-vhd-set-and-storage-qos
name: hyper-v-shared-vhdx-vhd-set-and-storage-qos
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, hyper-v-host, hyper-v-vm, vhd-set, vhds, shared-vhdx, guest-clustering, storage-qos, new-storageqospolicy, minimumiops, maximumiops, convert-vhd, resize-vhd]
level: advanced
status: docs-checked
description: "Hyper-V storage beyond basics: VHD Set (.vhds) for guest clusters, converting shared VHDX, and Storage QoS policies with Hyper-V and Scale-Out File Server."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/create-vhdset-file
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-qos/storage-qos-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VHD Set, shared VHDX and Storage QoS

## Guest clusters with VHD Set
A **VHD Set** (`.vhds`) is the shared virtual disk model for guest clusters introduced in
Windows Server 2016. It supports online resizing of shared virtual disks, supports Hyper-V
Replica and can be included in application-consistent checkpoints.
```powershell
New-VHD -Path <CSV_ROOT>\Volume1\GuestCluster\data.vhds -SizeBytes 200GB -Dynamic
Add-VMHardDiskDrive -VMName sql-n1 -Path <CSV_ROOT>\Volume1\GuestCluster\data.vhds -SupportPersistentReservations
Add-VMHardDiskDrive -VMName sql-n2 -Path <CSV_ROOT>\Volume1\GuestCluster\data.vhds -SupportPersistentReservations
```
(`<CSV_ROOT>` is the cluster shared storage root.) `New-VHD` creates a VHD Set when the path ends in `.vhds`.

Convert an existing shared VHDX, then attach the result (Learn example: `Convert-VHD existing.vhdx new.vhds`,
then `Add-VMHardDiskDrive new.vhds`).

## Storage QoS (CSV / Scale-Out File Server)
Storage QoS (Windows Server 2016 and later) manages storage performance for VMs using Hyper-V and the Scale-Out File Server role, in normalized IOPS. Policies are stored in the cluster database with `PolicyId`, `MinimumIOPS` (reservation), `MaximumIOPS` (limit), `ParentPolicy` and `PolicyType`:
- **Dedicated**: min/max managed for each VHD/VHDX individually.
- **Aggregated**: min/max shared among all VHDs assigned the policy. Keep it to 20 VHD/VHDX files or fewer per Aggregated policy.
```powershell
$p = New-StorageQosPolicy -Name Gold -PolicyType Dedicated -MinimumIops 500 -MaximumIops 5000
Get-VM sql-n1 | Get-VMHardDiskDrive | Set-VMHardDiskDrive -QoSPolicyID $p.PolicyId
Get-StorageQosFlow | Sort-Object StorageNodeIOPS -Descending | ft InitiatorName, StorageNodeIOPS, Status, FilePath -AutoSize
```
The default IOPS normalization size is 8 KB (adjustable cluster-wide, minimum 1 KB). A flow with status `InsufficientThroughput` has a policy applied but its minimum IOPS cannot be delivered.

## Verify
- [ ] Guest cluster validation passes storage tests with the VHD Set.
- [ ] `Get-StorageQosFlow` shows policies applied and no persistent InsufficientThroughput.

## Checked
2026-10-28. Confirmed against "Create a VHD Set file", "Storage Quality of Service" (policy properties, Dedicated/Aggregated semantics, 20-file guidance, 8 KB default normalization and 1 KB minimum, flow status, `Get-StorageQosFlow`, `New-StorageQosPolicy`, `Set-VMHardDiskDrive -QoSPolicyID`) and the Hyper-V reference pages for `New-VHD` (`-SizeBytes`, `-Dynamic`), `Add-VMHardDiskDrive` and `Set-VMHardDiskDrive` (`-SupportPersistentReservations`, `-QoSPolicyID`). Removed as unconfirmed: the `.avhdx` and host-backup claims, CSV/SOFS placement requirements, the Resize-VHD/Resize-Partition section and the `InitiatorIOPS` property (the page uses `StorageNodeIOPS`).
Method: documentation only; no commands were run.
