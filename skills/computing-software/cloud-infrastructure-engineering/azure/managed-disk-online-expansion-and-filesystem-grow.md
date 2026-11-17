---
id: computing-software.cloud-infrastructure-engineering.azure.managed-disk-online-expansion-and-filesystem-grow
name: managed-disk-online-expansion-and-filesystem-grow
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-disks, disk-resize, resize-filesystem, growpart, az-disk-update]
level: practitioner
status: docs-checked
description: "Expand Azure managed disks (data and OS), know when deallocation is required, and grow the partition and file system inside Linux and Windows afterwards."
sources: ["https://learn.microsoft.com/en-us/azure/virtual-machines/windows/expand-os-disk", "https://learn.microsoft.com/en-us/azure/virtual-machines/linux/expand-disks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed disk expansion

**Goal:** more capacity with minimal downtime, then make the guest actually use it.

## Expand the disk
```bash
az disk update -g rg -n datadisk1 --size-gb 512
# if the disk needs a deallocated VM:
az vm deallocate -g rg -n vm1
az disk update -g rg -n datadisk1 --size-gb 512
az vm start -g rg -n vm1
```
- Shrinking an existing disk isn't supported and might result in data loss. The updated size is rounded up to the nearest managed disk size.
- Expansion without downtime (deallocation) is supported only for data disks, using the latest Azure CLI or PowerShell module, the portal, or an ARM template with API version 2021-04-01 or newer. OS disks and data disks that don't meet the requirements need the VM deallocated (`az vm deallocate`; `az vm stop` doesn't release compute).
- The disk's host cache setting doesn't change whether you can expand a data disk without deallocating.
- Standard HDD, Standard SSD or Premium SSD of 4 TiB or less: deallocate the VM and detach the disk before expanding it beyond 4 TiB. If it is already larger than 4 TiB you can expand it live. This limit doesn't apply to Premium SSD v2 or Ultra Disks (which also can't be expanded while a background copy is running on the disk).
- Some classic VM SKUs don't support live expansion; the Learn pages include a PowerShell script to list the ones that do.
- OS disk maximum is 4,095 GiB, but MBR partitioning limits usable size to 2 TiB; convert to GPT or use data disks.
- Back up or snapshot before expanding; make sure the file system is healthy and the partition table (GPT or MBR) supports the new size.

## Grow inside the guest
After a live expansion the guest may not see the new size until the device is rescanned (normally only at boot):
```bash
echo 1 | sudo tee /sys/class/block/sda/device/rescan    # replace sda with the resized device
```
Learn says to allow up to 10 minutes for the size to show for Ultra Disk / Premium SSD v2, and to rescan again if needed.

Linux (identify the device and file system type first with `df -Th`, `lsblk -f`; the Learn examples use `growpart` from cloud-utils/gdisk):
```bash
sudo growpart /dev/sda 4          # disk and partition number as separate arguments
sudo xfs_growfs /                 # XFS (mount point)
sudo resize2fs /dev/sda4          # ext4 (partition device); do not run xfs_growfs on ext4
```
- Ubuntu 16.x and newer: cloud-init expands the root partition and file system automatically after the OS disk is expanded and the VM restarted (a small amount of free space is needed).
- LVM: after `growpart`, run `pvresize /dev/sda4`, then `lvresize -r -L +10G /dev/mapper/rootvg-rootlv` (the `-r` also resizes the file system).

Windows: connect by RDP, then in DiskPart run `list volume`, `select volume <volumenumber>`, `extend [size=<size>]` (size in MB), or use Disk Management > Extend Volume on the partition. Striped volumes can't be expanded.

## Check
`az disk list -g rg --query '[*].{Name:name,size:diskSizeGB,Tier:sku.tier}' --output table`; `df -Th` on Linux shows the new file system size.

## Checked
Date: 2026-11-07
Read in full: Learn "Expand virtual hard disks attached to a Windows virtual machine" (expand-os-disk URL; redirects to expand-disks) and "Expand virtual hard disks on a Linux VM" (live-expansion limitations, rounding, rescan, Ubuntu auto-expansion, SUSE/Red Hat growpart, LVM `pvresize`/`lvresize -r`, xfs_growfs/resize2fs, DiskPart steps).
Fixed or removed: the claim that host caching must be off for larger disks (pages say the cache setting is irrelevant; the real limit is the 4 TiB boundary for Standard/Premium SSD), "next performance tier" cost claim, `Get-PartitionSupportedSize`/`Resize-Partition`, the recovery-partition and dynamic-disk gotchas, `lvextend -r -l +100%FREE` (pages use `lvresize -r -L`), `growpart /dev/sdc 1` example device, and the "unconfirmed" footer. Not opened: the linked Windows rescan procedure and the portal steps.
Method: documentation only; no commands were run.
