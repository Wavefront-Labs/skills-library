---
id: computing-software.cloud-infrastructure-engineering.azure.managed-disk-performance-tier-change-and-type-conversion
name: managed-disk-performance-tier-change-and-type-conversion
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-disks, performance-tier, disk-type-conversion, premium-ssd, lrs-to-zrs]
level: practitioner
status: docs-checked
description: "Change managed disk performance without resizing (Premium SSD tiers) and convert disk types or redundancy (HDD/SSD/Premium, LRS to ZRS, to Premium SSD v2) with the right downtime."
sources: ["https://learn.microsoft.com/azure/virtual-machines/disks-change-performance", "https://learn.microsoft.com/azure/virtual-machines/disks-convert-types", "https://learn.microsoft.com/azure/virtual-machines/disks-migrate-lrs-zrs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Performance tier change and disk type conversion

**Goal:** get more (or cheaper) disk performance with minimal disruption.

## Premium SSD performance tiers (no resize)
A Premium SSD's performance tier is set from its size (a 128 GiB disk is baseline P10) and can be raised without resizing, e.g. a P10 disk run at P40 for a month-end batch. Only Premium SSD managed disks support tiers; you cannot set a tier below the baseline, and P60, P70 and P80 need a disk larger than 4,096 GiB.
```bash
az disk update -g rg -n vm01-data0 --set tier=P40
az disk show -g rg -n vm01-data0 --query "{size:diskSizeGb,tier:tier,iops:diskIopsReadWrite}"
```
- Most tier changes need no downtime; shared disks attached to running VMs must have their VMs stopped first, and changing the tier with Terraform shuts the VM down.
- The disk is billed at the tier you set; a disk's tier can be downgraded only once every **12 hours**.
- Disks created before June 2020 do not report a tier until updated with the baseline tier.
- Premium SSD v2 and Ultra do not use tiers; adjust IOPS/MBps directly (`--disk-iops-read-write`, `--disk-mbps-read-write`).

## Convert disk type (Standard HDD / Standard SSD / Premium SSD)
```bash
az vm deallocate -g rg -n vm01
az disk update -g rg -n vm01-osdisk --sku Premium_LRS
az vm start -g rg -n vm01
```
- Stop and deallocate the VM before changing the storage type; for a regional disk the conversion itself is instantaneous.
- Change the VM to a Premium-capable size before moving to Premium (skip when going from Premium to Standard).
- You can change a disk's type only **twice per day**.

## LRS to ZRS
ZRS for managed disks supports only Premium SSD and Standard SSD (not Premium SSD v2 or Ultra). First check whether the disk is regional (no value in `zones` in `az disk show`) or zonal.
- **Regional disk**: convert directly with `az disk update --sku Premium_ZRS` (or `StandardSSD_ZRS`) after deallocating the VM.
- **Zonal disk**: cannot be changed directly; snapshot it, then create a new ZRS disk and attach it to a new VM:
```bash
az snapshot create -g rg -n snap-os --source vm01-osdisk
az disk create -g rg -n vm01-osdisk-zrs --source snap-os --sku Premium_ZRS
az vm create -g rg -n vm01-new --attach-os-disk vm01-osdisk-zrs --os-type linux
```
The source disks keep billing until you delete them.

## To Premium SSD v2 / Ultra
You can switch an existing disk to Premium SSD v2 as for other types, with limits: no OS disks, only to 512 sector size v2 disks, detach all VMs from a shared disk first, set host caching to none and disable bursting first, and not if the disk was created from an Azure Compute Gallery image. For many disks, convert in batches of 50 to 100 per subscription per region.

## Gotchas
- A disk's performance is also bounded by the VM's own limits (see the Learn page on virtual machine and disk performance).
- For temporary sustained demand a tier change can cost less than relying on bursting.
- Keep snapshots until the converted disk is validated.

## Verify
- [ ] `az disk show` reflects new sku/tier; a fio/DiskSpd test confirms expected IOPS and the VM-level cap isn't the bottleneck.

## Checked
2026-10-28. Confirmed on the Performance tiers, Convert disk types and Convert LRS to ZRS pages: tier restrictions (Premium SSD only, no tier below baseline, P60 to P80 above 4,096 GiB, 12-hour downgrade limit, shared-disk and Terraform exceptions), P10 to P40 allowed, two type changes per day, deallocate-and-resize steps, ZRS only for Premium and Standard SSD, regional versus zonal paths, Premium SSD v2 conversion limits. CLI flags checked with check_commands. Removed: the incremental-snapshot flag, zone-attachment remark, `az vm update --os-disk` swap, D2s example, bursting-cheaper claim, sizes-with-s rule.
Method: documentation only; no commands were run.
