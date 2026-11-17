---
id: computing-software.systems-network-administration.virtualisation.hyper-v-shared-vhdx-and-vhd-set
name: hyper-v-shared-vhdx-and-vhd-set
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, vhd-set, shared-vhdx, vhds, guest-clustering, persistent-reservations, csv, windows-server]
level: advanced
status: docs-checked
description: "Provide shared storage to guest failover clusters with VHD Set (.vhds) or legacy shared VHDX on CSV or SOFS, including persistent reservations and backup limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/create-vhdset-file
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/add-vmharddiskdrive
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Shared VHDX and VHD Set for guest clusters

**Goal:** give two or more VMs a shared disk so they can form a Windows failover cluster (e.g. SQL FCI, file server) without iSCSI inside the guest.

## Requirements
- Hosts in a failover cluster, with the shared file on a CSV or a Scale-Out File Server share (confirm the exact requirements in the current Microsoft documentation).
- Disks attached with `-SupportPersistentReservations`, which marks a shared disk used by multiple VMs as supporting SCSI persistent reservations.

## VHD Set (Windows Server 2016+, preferred)
```powershell
New-VHD -Path <CSV_ROOT>\Volume1\Shared\sqlfci-data.vhds -SizeBytes 200GB
foreach ($vm in 'sql01','sql02') {
  Add-VMHardDiskDrive -VMName $vm -Path <CSV_ROOT>\Volume1\Shared\sqlfci-data.vhds `
    -SupportPersistentReservations
}
```
VHD Set files (`.vhds`, Windows Server 2016) support online resizing, Hyper-V Replica and application-consistent checkpoints; the VHD Set stores checkpoint metadata for the group disk and Hyper-V manages the chain. Evaluate performance and latency before production use.

## Migrating an existing shared VHDX
Migration to a VHD Set needs the VM offline: remove the VHDX from the VM (`Remove-VMHardDiskDrive`), run `Convert-VHD existing.vhdx new.vhds`, and add the `.vhds` to the VM (`Add-VMHardDiskDrive`, with `-SupportPersistentReservations`).

## Inside the guests
Online and initialise the disk on one node, run cluster validation, then add it as a cluster disk.

## Gotchas
- Do not attach a shared disk without `-SupportPersistentReservations`; both VMs would mount it as normal disks and corrupt it.
- Guest cluster VMs need anti-affinity (see the preferred owners skill: AntiAffinityClassNames takes a string collection) so both nodes do not sit on one host.

## Verify
`Test-Cluster` in the guests passes the storage persistent-reservation tests, and failover of the clustered role moves disk ownership cleanly.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed in the VHD Set page: .vhds format, online resize, Hyper-V Replica, application-consistent checkpoints, New-VHD with a .vhds path, and the offline migration steps with Convert-VHD; Add-VMHardDiskDrive -SupportPersistentReservations. Corrected: removed the statement that VHD Sets only support host-level backup checkpoints. Removed as unconfirmed: legacy shared VHDX limits, the shared SAS disk remark and the -Dynamic switch.

Method: documentation only; no commands were run.
