---
id: computing-software.systems-network-administration.virtualisation.storage-vmotion-disk-format-and-per-disk-placement
name: storage-vmotion-disk-format-and-per-disk-placement
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [svmotion-thin-conversion, storage-vmotion, thin-provisioning, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Move one virtual disk to another datastore or datastore cluster and change its format with PowerCLI Move-HardDisk: parameters, accepted formats and SDRS behaviour."
sources:
  - https://developer.broadcom.com/powercli/latest/vmware.vimautomation.core/commands/move-harddisk
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Move a single disk with PowerCLI (Move-HardDisk)

**Goal:** relocate one virtual disk, and optionally change its format, without touching the
rest of the VM.

## Syntax
`Move-HardDisk -HardDisk <HardDisk[]> [-Datastore] <StorageResource> [-StorageFormat
<VirtualDiskStorageFormat>] [-RunAsync] [-Server <VIServer[]>]`

- `-Datastore` (required, position 1): a datastore or a datastore cluster to move the disk
  to. For a datastore cluster the cmdlet checks whether Storage DRS is enabled. If SDRS is
  enabled the disk is allocated to the cluster in automated SDRS mode; if SDRS is
  deactivated the disk goes to the datastore with the most free space in the cluster.
- `-HardDisk` (required, named, accepts pipeline input): the disk to move.
- `-StorageFormat` (optional): accepts `Thin`, `Thick` and `EagerZeroedThick`.
- `-RunAsync`: returns immediately with a Task object instead of waiting.
- `-Server`: the vCenter Server systems to run against; default servers when omitted.
- Output is a HardDisk object.

## Examples from the reference page
```powershell
$myDisk = Get-VM -Name 'MyVM1' | Get-HardDisk
$myDatastore1 = Get-Datastore -Name 'MyDatastore1'
Move-HardDisk -HardDisk $myDisk -Datastore $myDatastore1 -StorageFormat 'EagerZeroedThick'
```
The same call without `-StorageFormat` moves the disk and keeps the format. Passing a
`Get-DatastoreCluster` object to `-Datastore` moves the disk to that datastore cluster.

## Checked
Date: 2026-11-07. Read the whole PowerCLI reference page for Move-HardDisk. The `Move-VM
-DiskStorageFormat` cmdlet page, the vSphere Client Migrate wizard and the Storage vMotion
documentation were not opened. Removed as not on the page: the vSphere Client wizard steps
and format names, the `Move-VM` example, free-space, same-datastore, NFS VAAI, RDM,
eager-zeroed, concurrency (2 per host, 8 per datastore) and snapshot claims, and the
`Get-HardDisk ... StorageFormat` verify line.
Method: documentation only; no commands were run.
