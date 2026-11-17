---
id: computing-software.cloud-infrastructure-engineering.google-cloud.disk-clones-and-instant-snapshots
name: disk-clones-and-instant-snapshots
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, persistent-disk, hyperdisk, disk-clone, instant-snapshots, restore, pre-change-backup]
level: practitioner
status: docs-checked
description: "Take fast in-zone restore points with instant snapshots before risky changes, clone disks for test copies, and convert to standard snapshots for durability."
sources: ["https://cloud.google.com/compute/docs/disks/instant-snapshots", "https://cloud.google.com/compute/docs/disks/create-disk-from-source", "https://cloud.google.com/sdk/gcloud/reference/compute/instant-snapshots/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disk clones and instant snapshots

| Tool | Speed | Lives | Use |
|---|---|---|---|
| Instant snapshot | lowest restore time of the snapshot types, incremental | stored in the same zone/region as the disk and deleted with it; not a backup | restore point before an upgrade or migration script |
| Disk clone | copy of a disk | independent disk in the same location (zone or region) as the source | test copy of prod data, forensics |
| Standard snapshot | slower restore than instant | independent, geo-redundant, survives disk/zone loss | backup and DR |

## 1. Restore point before a risky change
```bash
gcloud compute instant-snapshots create db-pre-upgrade --zone=<Z> --source-disk=db-data
# ... run the upgrade; if it fails:
gcloud compute instances stop db-1 --zone=<Z>
gcloud compute disks create db-data-restored --zone=<Z> --source-instant-snapshot=db-pre-upgrade
gcloud compute instances detach-disk db-1 --zone=<Z> --disk=db-data
gcloud compute instances attach-disk db-1 --zone=<Z> --disk=db-data-restored --device-name=db-data
```
Keep it durable if the change sticks around:
```bash
gcloud compute snapshots create db-pre-upgrade-std --source-instant-snapshot=db-pre-upgrade \
  --source-instant-snapshot-zone=<Z> --storage-location=europe-west2
gcloud compute instant-snapshots delete db-pre-upgrade --zone=<Z>
```

## 2. Clone a disk
```bash
gcloud compute disks create db-data-clone --zone=<Z> --source-disk=db-data   # optionally --type / --size larger
```
Attach the clone to a separate VM; do not mount a clone of a disk on the same VM as the original without changing the filesystem UUID.

## 3. Consistency
For databases, flush or freeze first (for example `fsfreeze -f /data`, or stop writes), take the snapshot, then thaw
(`fsfreeze -u /data`). Standard snapshots accept `--guest-flush` to ask the guest to prepare for an application-consistent snapshot.

## Gotchas
- Instant snapshots are not backups: they are deleted with the source disk and do not protect against zonal or regional failures; always convert anything you need to keep to a standard snapshot.
- Instant snapshots are not available for Hyperdisk ML or Hyperdisk Throughput volumes.
- A clone or restore is a new disk: update device names in `/etc/fstab` that rely on `/dev/disk/by-id/google-<name>`.

## Verify
- [ ] `gcloud compute instant-snapshots list --filter='sourceDisk~db-data'` shows the restore point before the change starts.
- [ ] A restore drill on staging mounts the restored disk with expected data.

## Checked

Checked 2026-10-27 against About instant snapshots, Duplicate a disk with clones, the gcloud reference for instant-snapshots create, snapshots create and disks create, and Create disk snapshots. Fixed: instant snapshots are restored to a new disk in minutes (the speed claim was removed), are deleted with the source disk, and are unavailable for Hyperdisk ML and Hyperdisk Throughput. Confirmed the flags, --guest-flush and that clones stay in the source location. Removed the rate-limit claim and filesystem UUID commands.

Method: documentation only; no commands were run.
