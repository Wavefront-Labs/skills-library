---
id: computing-software.systems-network-administration.virtualisation.hyper-v-pass-through-disks
name: hyper-v-pass-through-disks
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pass-through-disk, hyper-v, storage]
level: practitioner
status: docs-checked
description: "Attach physical disks directly to Hyper-V VMs as pass-through disks, including the offline requirement, cluster use, and the features you lose compared with VHDX."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/add-vmharddiskdrive
  - https://learn.microsoft.com/en-us/powershell/module/storage/set-storagesetting
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/maximum-scale-limits
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Pass-through disks

**Goal:** give a VM a raw physical disk or LUN when there is a real reason, knowing the trade-offs.

## Attach
```powershell
Get-Disk | Select Number, FriendlyName, Size, OperationalStatus
Set-Disk -Number 5 -IsOffline $true          # must be offline on the host
Add-VMHardDiskDrive -VMName fs01 -ControllerType SCSI -DiskNumber 5
Get-VMHardDiskDrive -VMName fs01
```
`Add-VMHardDiskDrive -DiskNumber` takes the number of an offline physical disk to connect as a pass-through disk.

## Trade-offs
Microsoft's cmdlet reference does not list which features a pass-through disk loses. Test checkpoints, host-level backup, Hyper-V Replica, live storage migration and clustering with your own configuration before relying on one. The maximum size of a pass-through disk is set by the guest operating system rather than a VHDX limit (Hyper-V maximum scale limits page). Disk numbers can differ between hosts, so inventory them.

## When it is still used
- Migrating a large existing LUN into a VM without copying data (temporary step).
- Vendor support statements that require direct disk access (rare today).
Prefer a VHDX unless you have a concrete reason for direct disk access.

## Gotchas
- `-DiskNumber` takes an offline physical disk, so keep the disk offline on the host and document which VM owns it.
- The host's new-disk policy decides whether newly attached disks come online; `Set-StorageSetting -NewDiskPolicy OfflineShared` leaves new disks on shared buses (iSCSI, FC, SAS) offline (the default policy on Windows Server 2016 and later per the reference).

## Verify
The guest sees the disk in Disk Management/`lsblk`; on the host it stays *Offline*.

## Checked

Checked 2026-10-26 against the Windows Server 2025 `Add-VMHardDiskDrive` reference (`-DiskNumber` is the offline physical disk connected as pass-through) and the `Set-StorageSetting` reference (`OfflineShared` policy and default), plus the Hyper-V maximum scale limits page. Removed as undocumented: the list of lost features (checkpoints, VSS/RCT backup, Replica, storage migration), the cluster-disk dependency instructions and the "within a few percent" performance claim.

Method: documentation only; no commands were run.
