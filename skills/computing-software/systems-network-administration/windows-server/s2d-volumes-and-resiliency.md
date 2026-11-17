---
id: computing-software.systems-network-administration.windows-server.s2d-volumes-and-resiliency
name: s2d-volumes-and-resiliency
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-spaces-direct, s2d, s2d-volumes, mirror-accelerated-parity, three-way-mirror, nested-resiliency, new-volume, csvfs-refs, reserve-capacity, s2d-reserve-capacity]
level: advanced
status: docs-checked
description: "Plan and create S2D volumes: three-way mirror, dual parity, mirror-accelerated parity, nested resiliency for two nodes, sizing and reserve capacity."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/plan-volumes
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/create-volumes
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/nested-resiliency
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/manage-volumes
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Create S2D volumes and choose resiliency

## Resiliency options
| Type | Nodes | Efficiency | Use |
|---|---|---|---|
| Two-way mirror | 2 | 50% | two-node clusters |
| Three-way mirror | 3+ | 33% | VMs, SQL: best write performance |
| Dual parity | 4+ | 50% at 4 servers, up to 80% at 16 | archive, backup, cold data |
| Mirror-accelerated parity (MAP) | 4+ | in between | writes land in mirror, rotate to parity |
| Nested two-way mirror / nested MAP | 2 | 25% / around 35-40% | survives a node plus a drive loss |

## Create
```powershell
New-Volume -FriendlyName VMs01 -FileSystem CSVFS_ReFS -StoragePoolFriendlyName 'S2D*' -Size 4TB `
  -ResiliencySettingName Mirror            # Mirror or Parity; three-way mirror needs 3+ servers
# Mirror-accelerated parity, 20% mirror
New-Volume -FriendlyName Archive01 -FileSystem CSVFS_ReFS -StoragePoolFriendlyName 'S2D*' `
  -StorageTierFriendlyNames Performance,Capacity -StorageTierSizes 2TB,8TB
```
Nested resiliency (Windows Server 2019 and later, two servers). Windows Server 2019 needs the tier templates created first; later
releases include NestedMirrorOn*MediaType* and NestedParityOn*MediaType* templates:
```powershell
New-StorageTier -StoragePoolFriendlyName S2D* -FriendlyName NestedMirrorOnSSD -ResiliencySettingName Mirror `
  -MediaType SSD -NumberOfDataCopies 4
New-Volume -StoragePoolFriendlyName S2D* -FriendlyName Vol01 -StorageTierFriendlyNames NestedMirrorOnSSD -StorageTierSizes 1TB
```
- Volumes mount as CSVs under `ClusterStorage\<name>` on the system drive.
- CSVFS_ReFS is recommended for all volumes and required for mirror-accelerated parity; CSVFS_NTFS is the alternative.

## Sizing rules
- Leave **reserve capacity** unallocated: one capacity drive per node, up to four drives,
  so repairs can rebuild in place.
- Microsoft recommends limiting each volume to 64 TB; with VSS-based backups, 10 TB improves performance.

## Grow a volume
```powershell
Get-VirtualDisk VMs01 | Get-StorageTier | Resize-StorageTier -Size 6TB
$p = Get-VirtualDisk VMs01 | Get-Disk | Get-Partition | ? Type -eq Basic
$p | Resize-Partition -Size ($p | Get-PartitionSupportedSize).SizeMax
```

## Verify
- [ ] `Get-VirtualDisk | Select FriendlyName,ResiliencySettingName,NumberOfDataCopies,PhysicalDiskRedundancy,FootprintOnPool`.
- [ ] `Get-StoragePool S2D* | Select Size,AllocatedSize` still leaves reserve.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (plan-volumes, create-volumes, nested-resiliency, add-nodes and manage-volumes; repository last commit 2026-10-23): resiliency types and efficiencies (two-way 50 percent, three-way 33 percent, dual parity 50 percent at four servers up to 80 percent, nested two-way 25 percent, nested mirror-accelerated parity around 35-40 percent), New-Volume parameters and CSVFS_ReFS recommendation, default Performance and Capacity tiers, NestedMirrorOn/NestedParityOn templates (2019 needs them created), reserve of one capacity drive per server up to four drives, 64 TB volume recommendation, Resize-StorageTier and Resize-Partition steps. Removed the unconfirmed block cloning claim, the volume-count balancing rule and the MAP working-set rule.

Method: documentation only; no commands were run.
