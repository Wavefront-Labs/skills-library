---
id: computing-software.systems-network-administration.windows-server.disks-partitions-and-refs-volumes
name: disks-partitions-and-refs-volumes
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-spaces, initialize-disk, refs, ntfs, new-partition, format-volume, storage-module, gpt, diskpart, resize-partition, allocation-unit-size]
level: practitioner
status: docs-checked
description: "Prepare disks with Storage cmdlets: online and initialise GPT, partition, format ReFS vs NTFS with the right allocation unit, extend volumes and clean reused disks."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/storage/initialize-disk
  - https://learn.microsoft.com/en-us/windows-server/storage/refs/refs-overview
  - https://learn.microsoft.com/en-us/powershell/module/storage/format-volume
  - https://learn.microsoft.com/en-us/powershell/module/storage/clear-disk
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/san
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disks, partitions and ReFS vs NTFS volumes (Storage cmdlets)

## New disk to formatted volume
```powershell
Get-Disk | Where PartitionStyle -eq 'RAW' | Select Number,FriendlyName,Size,OperationalStatus
Set-Disk -Number 2 -IsOffline $false          # SAN policy keeps new shared disks offline
Set-Disk -Number 2 -IsReadOnly $false
Initialize-Disk -Number 2 -PartitionStyle GPT
New-Partition -DiskNumber 2 -UseMaximumSize -DriveLetter F |
  Format-Volume -FileSystem ReFS -AllocationUnitSize 4096 -NewFileSystemLabel Data -Confirm:$false
```
- `Initialize-Disk` defaults to GPT; MBR is available with `-PartitionStyle MBR`.
- The SAN policy (show with `diskpart` then `san`) decides whether newly discovered disks come online and read/write.
  `offlineShared` brings non-shared-bus disks online and leaves shared-bus (SCSI, iSCSI) disks offline and read-only;
  `onlineAll` on a server that shares disks can corrupt data unless the server is in a cluster. Bring shared disks
  online per disk instead of flipping the policy.

## ReFS or NTFS
| Need | Choose |
|---|---|
| Hyper-V VHDX, S2D, backup targets (block cloning, sparse VDL for fast fixed VHD creation) | ReFS |
| Detect and repair corruption online (integrity streams, with a Storage Spaces mirror or parity space) | ReFS |
| Boot volume, removable media | NTFS (ReFS is not bootable and not supported on removable media) |
| Disk quotas, short names, object IDs, ODX, transactions, shrinking volumes | NTFS (not available on ReFS) |
| File system encryption (EFS) | NTFS; ReFS only on Windows Server 2025 |
| Page file, BitLocker, volume snapshots | both |
- Data Deduplication on ReFS is available on Windows Server 1709 and later and Windows Server 2019 (1809) LTSC or later.
- ReFS-formatted CSVs do not use Direct I/O with Storage Spaces, S2D or SAN; for SAN storage format CSVs with NTFS.
- ReFS supports 4K and 64K clusters: 4K is recommended for most deployments, 64K for large, sequential I/O workloads.
  ReFS maximum volume size is 35 PB (NTFS 256 TB).

## Extend and shrink
```powershell
Update-HostStorageCache
$max = (Get-PartitionSupportedSize -DriveLetter F).SizeMax
Resize-Partition -DriveLetter F -Size $max
```
ReFS volumes can grow but not shrink (shrinking is available on NTFS).

## Clean a reused disk
```powershell
Clear-Disk -Number 2 -RemoveData -RemoveOEM -Confirm:$false
```
`Clear-Disk -RemoveData` is required when the disk holds active data volumes, and `-RemoveOEM` also clears OEM
recovery partitions. `Reset-PhysicalDisk` is destructive for Storage Spaces: it removes pool configuration and data
from the physical disk, and on a disk not in a pool it clears lingering Storage Spaces data and metadata. Triple-check
the disk number: there is no undo.

## Verify
- [ ] `Get-Volume F | Select FileSystem,AllocationUnitSize,HealthStatus,SizeRemaining`.
- [ ] `fsutil fsinfo refsinfo F:` (ReFS version) or `fsutil fsinfo ntfsinfo F:`.
- [ ] Disk is Online and not read-only after reboot.

## Checked

2026-10-27. Documentation release: windowsserverdocs ReFS overview (current), the Storage module references for Initialize-Disk, Clear-Disk, Format-Volume, Set-Disk, Reset-PhysicalDisk and Get-PartitionSupportedSize (Windows Server 2022 docset) and the DiskPart san command reference. Confirmed: GPT default, ReFS versus NTFS feature table (page file, BitLocker, snapshots, dedup version, EFS on Server 2025, shrinking, quotas, boot, removable media), 4K and 64K cluster guidance, CSV Direct I/O note, SAN policy options, Clear-Disk and Reset-PhysicalDisk behaviour. Corrected: page file hosting is supported on ReFS, and the 64 KB allocation default for ReFS. Removed the default SAN policy by edition, the in-place conversion claim, FSRM and NTFS shrink limit statements as unconfirmed.

Method: documentation only; no commands were run.
