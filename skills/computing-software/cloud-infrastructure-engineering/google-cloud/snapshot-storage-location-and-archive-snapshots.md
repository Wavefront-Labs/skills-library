---
id: computing-software.cloud-infrastructure-engineering.google-cloud.snapshot-storage-location-and-archive-snapshots
name: snapshot-storage-location-and-archive-snapshots
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, persistent-disk, disk-snapshots, snapshot-location, archive-snapshots, data-residency, cost-optimisation]
level: practitioner
status: docs-checked
description: "Choose where disk snapshots live (regional vs multi-region, residency policy) and when to use cheaper archive snapshots, including minimum retention and restore cost."
sources: ["https://cloud.google.com/compute/docs/disks/snapshots", "https://cloud.google.com/compute/docs/disks/snapshot-best-practices", "https://cloud.google.com/compute/docs/disks/create-snapshots", "https://cloud.google.com/compute/disks-image-pricing#snapshots"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot storage location and archive snapshots

## 1. Location
By default a snapshot goes to the **multi-region nearest the disk** (e.g. `eu`, `us`, `asia`).
Set it explicitly:
```bash
gcloud compute snapshots create db-2026-10-16 --source-disk=db-data --source-disk-zone=europe-west2-a \
  --storage-location=europe-west2          # regional: residency, cheaper network
gcloud compute resource-policies create snapshot-schedule daily-eu --region=europe-west2 \
  --daily-schedule --start-time=02:00 --max-retention-days=30 --storage-location=eu
```
| Choice | Pros | Cons |
|---|---|---|
| multi-region (`eu`) | survives a regional outage; restore in any region of it | data spans countries in the multi-region |
| regional same as disk | strict residency, lower cost | regional loss = snapshot loss |
| regional elsewhere | DR copy in a second region | cross-region transfer cost at creation |
Snapshots are global resources by default (a disk can be created from them in any project or region); use snapshot settings to restrict the regions where snapshots can be created and restored, before teams create snapshots.

## 2. Archive snapshots
For long retention you rarely restore (compliance, year-end):
```bash
gcloud compute snapshots create db-ye-2026 --source-disk=db-data --source-disk-zone=<Z> \
  --snapshot-type=ARCHIVE --storage-location=europe-west2
```
- Lower storage price than standard; billed for a **minimum of 90 days** of storage plus a retrieval charge when used to create a disk (see the Compute Engine disk pricing page for current rates).
- Archive and standard snapshots are kept in separate incremental snapshot chains. Deleting an archive snapshot is irreversible.
- Snapshot schedules cannot create archive snapshots (the schedule create command has no snapshot-type option); create them with a scheduled job that runs `gcloud compute snapshots create --snapshot-type=ARCHIVE`.

## 3. Retention hygiene
```bash
gcloud compute snapshots list --filter='creationTimestamp<-P400D' --format='table(name,storageLocations,diskSizeGb,snapshotType)'
```
With the recycle bin (Preview at the time of checking) a deleted standard snapshot stays recoverable for three days by default; an archive snapshot cannot be recovered.

## Gotchas
- Create the snapshot in the location you need: the location is chosen at creation with `--storage-location`.
- Snapshot schedules take `--max-retention-days` (required) and `--storage-location`.

## Verify
- [ ] `gcloud compute snapshots describe <S> --format='value(storageLocations,snapshotType)'` matches policy.
- [ ] A restore test from an archive snapshot completes and the cost appears as retrieval in billing.

## Checked

Checked 2026-10-27 against About disk snapshots, Create disk snapshots, the Compute Engine disk and image pricing page (minimum 90 days and retrieval charge for archive snapshots, no prices quoted) and the gcloud reference for snapshots create and resource-policies create snapshot-schedule. Fixed wrong claims: archive snapshots are incremental in their own chain and snapshot schedules cannot create them. Confirmed the default location (nearest multi-region), the recycle bin (Preview) and --snapshot-type, --storage-location, --max-retention-days. Removed unconfirmed location-change, egress and chain-deletion claims.

Method: documentation only; no commands were run.
