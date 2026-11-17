---
id: computing-software.cloud-infrastructure-engineering.azure.incremental-snapshots-and-disk-restore
name: incremental-snapshots-and-disk-restore
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-disks, incremental-snapshots, snapshot-restore, az-snapshot, copy-start]
level: practitioner
status: docs-checked
description: "Create incremental managed-disk snapshots, copy them across regions with a managed copy, and restore a disk from a snapshot, with the documented limits."
sources: ["https://learn.microsoft.com/en-us/azure/virtual-machines/disks-incremental-snapshots", "https://learn.microsoft.com/en-us/azure/virtual-machines/disks-copy-incremental-snapshot-across-regions", "https://learn.microsoft.com/en-us/azure/virtual-machines/scripts/create-managed-disk-from-snapshot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incremental snapshots and restore

**Goal:** cheap, frequent point-in-time disk copies and a tested restore path.

## Create
```bash
DISK_ID=$(az disk show -g rg -n datadisk1 --query id -o tsv)
az snapshot create -g rg -n snap-2026-11-02 --source "$DISK_ID" --incremental true
```
- The first incremental snapshot is a full copy of the disk; later ones occupy only the changes since the last snapshot. Incremental snapshots are billed for the used size only.
- Incremental snapshots use Standard HDD storage regardless of the source disk type. If zone-redundant storage (ZRS) is available in the region the snapshot uses it automatically; otherwise it defaults to LRS.
- Limits: up to seven incremental snapshots per disk every five minutes; up to 500 incremental snapshots per disk at any one time (delete older ones to make room).
- Incremental snapshots cannot be moved between subscriptions or to another resource group (they can be copied), and cannot be created outside the disk's subscription.
- Snapshots of Premium SSD, Standard SSD and Standard HDD can be used immediately. Incremental snapshots of Ultra Disk and Premium SSD v2 cannot be used until the background copy finishes, unless you enable instant access when you create the snapshot.

## Cross-region copy (managed copy)
```bash
az snapshot create -g rg2 -n snap-dr --source "$SNAP_ID" --incremental --location westeurope --copy-start
az snapshot show -g rg2 -n snap-dr --query [completionPercent] -o tsv
```
- `completionPercent` must be 100 before you restore a disk or generate a SAS URI from the target.
- Restrictions: 100 incremental snapshots copying in parallel per subscription per region; one incremental snapshot of a given disk at a time; snapshots must be copied in the order created; only incremental snapshots can be copied across regions; do not delete the source snapshot while the copy runs.

## Restore
```bash
az disk create -g rg -n datadisk1-restored --source "$SNAP_ID" --sku Premium_LRS
az vm disk attach -g rg --vm-name vm1 --name datadisk1-restored
```
- If you pass `--size-gb`, the sample's comment says the size should be greater than the VHD file size.
- Creating a disk from a snapshot starts a background copy. Attaching the disk while it runs is possible but costs performance (4k disks see read impact, 512e disks read and write impact). `completionPercent` is only meaningful for Ultra Disk and Premium SSD v2; other types report 100%.
- Snapshots of Ultra Disk or Premium SSD v2 disks with a 4096 logical sector size (stored as VHDX) can only be used to create Ultra Disks and Premium SSD v2 disks. Check with `az snapshot show -g rg -n snap --query [creationData.logicalSectorSize] -o tsv`.

## Checked
Date: 2026-11-07
Read in full: Learn "Create an incremental snapshot for managed disks" (storage, ZRS/LRS, billing, restrictions, CLI create, status checks), "Copy an incremental snapshot to a new region" (managed copy restrictions, `--incremental --copy-start`, `completionPercent`), "Create a managed disk from a snapshot with CLI (Linux)" (`az disk create --source`, `--sku`, `--size-gb`, background copy impact).
Removed as unconfirmed: "stored on Standard storage" (page says Standard HDD), the claim that full and incremental snapshots cannot be converted, the operations section (Azure Backup, crash-consistency, "deleting an older snapshot is safe", tags and delete locks), the OS-disk swap and `--attach-os-disk` line, and the checksum Verify step. `az vm disk attach` is not used on these pages; its flags were checked against the CLI reference by the review tooling only.
Method: documentation only; no commands were run.
