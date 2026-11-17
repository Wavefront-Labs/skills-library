---
id: computing-software.cloud-infrastructure-engineering.azure.managed-disks-performance-and-encryption
name: managed-disks-performance-and-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-disks, premium-ssd, premium-ssd-v2, ultra-disk, shared-disks, snapshots, host-caching, disk-encryption, sizing]
level: practitioner
status: docs-checked
description: "Choose Azure managed disk types, understand the VM-versus-disk performance caps, resize and snapshot safely, use shared disks correctly, and pick one encryption model."
sources: ["https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types", "https://learn.microsoft.com/en-us/azure/virtual-machines/disks-shared", "https://learn.microsoft.com/en-us/azure/virtual-machines/disks-scalability-targets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed disks — performance you can predict, encryption you can explain

**Goal:** disks sized for IOPS not just GiB, the VM cap understood, snapshots incremental,
and one deliberate encryption model per environment.

## 1. Disk types
| Type | Facts confirmed in the docs |
|---|---|
| Standard HDD | latency-tolerant, large sequential I/O; use as an OS disk retires on 8 September 2028 |
| Standard SSD | usable as OS disk; can be a shared disk |
| Premium SSD | production default; supports disk bursting; fixed sizes |
| Premium SSD v2 | no fixed sizes: 1 GiB to 64 TiB, baseline 3,000 IOPS free, 3,000-80,000 IOPS and 125-2,000 MB/s provisioned separately from size; no host caching; cannot be an OS disk |
| Ultra Disk | 4 GiB to 64 TiB; no host caching; not ZRS; cannot be an OS disk |
Look up per-size IOPS/throughput and burst limits in the disk-types and scalability-targets pages
rather than copying figures.
```bash
az disk create -g <RG> -n data01 --size-gb 512 --sku Premium_LRS --zone 1 --tier P40
az disk create -g <RG> -n db01 --size-gb 1024 --sku PremiumV2_LRS --zone 1 --disk-iops-read-write 20000 --disk-mbps-read-write 600
az vm disk attach -g <RG> --vm-name <VM> --name data01 --lun 0 --caching ReadOnly
```
Premium SSD v2 disks can be attached to zonal VMs, or to nonzonal VMs with extra limitations.

## 2. The two caps
Effective performance is limited by both the disks and the VM size: check the VM size's
uncached and cached limits, and the Azure Monitor disk metrics, before adding disks.
- Host caching is available on Premium SSD but not on Premium SSD v2 or Ultra.
- Stripe disks to aggregate IOPS under the VM cap.

## 3. Resize and snapshots
- Grow: `az disk update --size-gb <N>`, then grow the partition and filesystem inside the guest. Shrinking is not possible; copy to a smaller disk.
- Snapshots: `az snapshot create --incremental true --source data01` for incremental snapshots.
- Export: `az disk grant-access --duration-in-seconds 3600 --access-level Read` returns a SAS URI.
- Convert SKU: `az disk update --sku StandardSSD_LRS` (deallocate the VM first).

## 4. Shared disks
Only Ultra Disks, Premium SSD v2, Premium SSD and Standard SSD can be shared (`--max-shares`).
VMs with a SCSI disk controller coordinate through SCSI persistent reservations, so use a
cluster-aware application, never two VMs mounting the same filesystem. Premium SSD with
maxShares>1 has no host caching and no disk bursting.

## 5. Encryption decision
| Need | Option |
|---|---|
| Default | server-side encryption with platform-managed keys |
| Own the key | server-side encryption with customer-managed keys via a Disk Encryption Set (`--enable-auto-key-rotation`) |
| Temp disk and caches encrypted too | encryption at host (check the current host-based-encryption article for enablement and supported sizes) |
| In-guest BitLocker or dm-crypt | Azure Disk Encryption |

## Gotchas
- A zonal disk is tied to its zone: create zonal from the start when using Premium SSD v2 or Ultra.
- Load tests on Premium SSD should outlast burst credits.

## Verify
- [ ] `az disk show --query "{sku:sku.name,tier:tier,iops:diskIopsReadWrite,mbps:diskMBpsReadWrite}"` matches the design.
- [ ] A restore from an incremental snapshot mounts and passes an application-level check.

## Checked
2026-10-28. Confirmed on the Learn pages "Select a disk type for Azure IaaS VMs", "Share an Azure managed disk" and "Scalability and performance targets for VM disks": disk-type facts above, shared-disk types and Premium SSD maxShares limits, SCSI persistent reservations. The az commands kept were checked against the Azure CLI reference (flags exist). Removed (not confirmed in those pages): Standard SSD and Premium IOPS figures, P-tier numbers, VM size cap examples, metric names, incremental-snapshot cross-region and zone-redundancy claims, Ultra snapshot/Backup statements, `az vm update --encryption-at-host` and `az disk update --os-type` (flags not in the CLI reference), Confidential VM and ADE detail, double-encryption flag value.
Method: documentation only; no commands were run.
