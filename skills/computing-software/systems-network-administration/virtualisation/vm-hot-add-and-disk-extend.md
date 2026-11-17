---
id: computing-software.systems-network-administration.virtualisation.vm-hot-add-and-disk-extend
name: vm-hot-add-and-disk-extend
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hot-add, hot-plug, cpu-hot-add, memory-hot-add, disk-extend, growpart, extend-volume, vnuma, vsphere-vm-administration, vmware, vsphere, hyper-v, proxmox]
level: practitioner
status: draft
description: "Grow running VMs: CPU/memory hot add and its vNUMA cost, extending virtual disks then partitions and filesystems in Windows and Linux, and when a reboot is still needed."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=2040375
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM hot add and online disk extension

**Goal:** add capacity to a running VM without downtime, and know when not to enable
hot add at all.

## CPU and memory hot add
- Enable per VM while powered off (Edit Settings → CPU/Memory → Enable hot add).
- **Cost:** on vSphere, enabling CPU hot add **disables vNUMA** for that VM, so wide VMs
  (more vCPUs than a NUMA node) lose NUMA awareness and perform worse. Enable only on
  small VMs or where the app truly needs it.
- Guest support: Windows Server supports memory hot add and CPU hot add (Datacenter /
  newer editions); Linux needs the CPUs/memory onlined (udev usually does it, check
  `lscpu` and `/sys/devices/system/memory/*/state`).
- Hot remove is generally not supported: shrinking needs a power-off.
- Proxmox: enable `hotplug: disk,network,usb,memory,cpu` and NUMA; Hyper-V: dynamic memory
  or runtime memory resize for Gen 2 VMs, but not vCPU hot add.

## Extend a disk online
1. Snapshots block disk extension on vSphere: delete them first.
2. Increase the VMDK size in Edit Settings (or `Set-HardDisk -CapacityGB 200`).
3. Guest:
   - **Windows:** Disk Management → Rescan → Extend Volume, or
     `Update-HostStorageCache; Resize-Partition -DriveLetter D -Size (Get-PartitionSupportedSize -DriveLetter D).SizeMax`.
     A recovery partition after C: blocks extension; it must be moved or removed.
   - **Linux:** rescan, grow partition, grow PV/LV/filesystem:
```sh
echo 1 > /sys/class/block/sdb/device/rescan
growpart /dev/sdb 1
pvresize /dev/sdb1 && lvextend -r -l +100%FREE /dev/vg_data/lv_data   # -r resizes fs
# plain partition: xfs_growfs /mount   or   resize2fs /dev/sdb1
```
MBR disks max out at 2 TB; convert to GPT (needs care, often downtime) before growing past it.

## Gotchas
- Extending a disk that a guest cluster shares (multi-writer, RDM) needs app-level
  procedure.
- Backup tools with CBT handle size changes but may run a full on next job.
- Hot-added memory above the VM's initial NUMA layout may land on one node.

## Verify
Guest reports the new CPU/memory (`lscpu`, Task Manager) or the larger filesystem
(`df -h`, `Get-Volume`), and application logs show no errors during the change.
