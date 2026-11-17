---
id: computing-software.cloud-infrastructure-engineering.google-cloud.persistent-disk-hyperdisk-and-snapshots
name: persistent-disk-hyperdisk-and-snapshots
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, persistent-disk, hyperdisk, hyperdisk-balanced, hyperdisk-extreme, pd-ssd, pd-balanced, local-ssd, disk-snapshots, snapshot-schedule, regional-persistent-disk, disk-resize, disk-iops, disk-throughput, block-storage, snapshot-consistency, multi-writer, storage-pools]
level: practitioner
status: docs-checked
description: "Choose and operate Compute Engine block storage: Hyperdisk vs Persistent Disk types, IOPS sizing, regional disks for HA, online resize and restorable snapshot schedules."
sources: ["https://cloud.google.com/compute/docs/disks", "https://cloud.google.com/compute/docs/disks/hyperdisks", "https://cloud.google.com/compute/docs/disks/performance", "https://cloud.google.com/compute/docs/disks/scheduled-snapshots", "https://cloud.google.com/compute/docs/disks/regional-persistent-disk", "https://cloud.google.com/compute/docs/disks/resize-persistent-disk"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Persistent Disk, Hyperdisk and snapshots

**Goal:** the right disk type for the IOPS you actually need, a zone failure that does not lose
data, and snapshots you have restored at least once.

## 1. Pick the type
| Type | Performance model |
|---|---|
| `pd-standard` (HDD) | scales with size |
| `pd-balanced` | scales with size (6 read and write IOPS per GiB) plus a size-independent baseline |
| `pd-ssd` | scales with size (30 read and write IOPS per GiB) plus a size-independent baseline |
| `pd-extreme` | provisioned IOPS |
| **`hyperdisk-balanced`** | **provision IOPS and throughput independently of size** |
| `hyperdisk-extreme` / `hyperdisk-throughput` / `hyperdisk-ml` | provisioned (Extreme: IOPS; Throughput and ML: MiB/s); not usable as boot disks |
| Local SSD | scratch, caches; not persistent |

Performance also caps **per VM**: it increases with the instance's vCPU count, so a small VM cannot drive what a large disk offers.
Maximum PD performance = baseline + (per-GiB rate x combined size of same-type disks attached to the VM).

```bash
gcloud compute disks create db-data --size=500GB --type=hyperdisk-balanced \
  --provisioned-iops=12000 --provisioned-throughput=600 --zone=europe-west1-b
```

## 2. Regional PD / Hyperdisk Balanced HA for zone failure
- Synchronous replication between two zones of a region; protects against one zonal failure. Attach only to instances in the replica zones. On failure, **force-attach** the disk to a VM in the other zone (`gcloud compute instances attach-disk --force-attach`; see "Regional disk failover" in the regional disk page).
- Not a substitute for backups.

## 3. Resize
`gcloud compute disks resize db-data --size=1TB --zone=...`, then grow the partition and filesystem inside the guest (see the resize page for your OS).
Disks never shrink; snapshot, create a smaller disk, copy data.

## 4. Snapshots that restore
- Stored in a region or multi-region storage location (`--storage-location`).
- **Schedule:** 
  ```bash
  gcloud compute resource-policies create snapshot-schedule daily-14d --region=europe-west1 \
    --daily-schedule --start-time=02:00 --max-retention-days=14 --on-source-disk-delete=keep-auto-snapshots \
    --storage-location=eu
  gcloud compute disks add-resource-policies db-data --resource-policies=daily-14d --zone=...
  ```
- **Consistency:** for application data at backup time use an application-consistent (guest-flush / VSS on Windows) snapshot as described in the Linux and Windows application-consistent snapshot guides, or rely on DB-level backups.
- **Instant snapshots** cannot be created from Hyperdisk ML or Hyperdisk Throughput volumes.
- Disk from snapshot: `gcloud compute disks create restored --source-snapshot=<NAME> --zone=...`.

## 5. Other things that bite
- Hyperdisk **Storage Pools** exist as a pooled-capacity option; see the hyperdisks page for limits before designing around them.
- Multi-writer is available for Hyperdisk Balanced High Availability, and only in read-write mode; see "Share disks between instances" for requirements.
- Hyperdisk ML supports read-only mode for sharing across VMs, with documented attach limits; you cannot go back to read-write once read-only is enabled.

## Verify
- [ ] A benchmark on a new disk reaches the provisioned IOPS (minus the VM cap).
- [ ] The snapshot schedule is attached to the disk and snapshots appear on schedule.
- [ ] Quarterly: restore last night's snapshot to a new VM, mount, run the app's integrity check.
- [ ] For regional disks: force-attach to a VM in the other zone completes and the filesystem mounts clean.

## Checked
2026-10-31. Confirmed against the Compute Engine disks pages (performance, hyperdisks, regional disks, scheduled snapshots, resize): 6 and 30 IOPS per GiB for balanced and SSD PD with baseline, vCPU dependence, Hyperdisk type names and billing basis, no Hyperdisk Extreme/ML/Throughput boot disks, instant snapshot limitation, regional sync replication between two zones and force-attach, multi-writer read-write only, no shrink, snapshot-schedule flags and storage locations, application-consistent (guest-flush/VSS) snapshots.
Removed as unconfirmed: filesystem grow commands, "no reboot", incremental/any-zone claim, fsfreeze and LVM consistency-group advice, lazy-load warm-up, auto-delete default, `--mode=ro`, storage-pool thin-provisioning detail, regional write-latency claims, `fio` command.
Method: documentation only; no commands were run.
