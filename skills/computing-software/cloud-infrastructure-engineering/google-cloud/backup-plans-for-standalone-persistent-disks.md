---
id: computing-software.cloud-infrastructure-engineering.google-cloud.backup-plans-for-standalone-persistent-disks
name: backup-plans-for-standalone-persistent-disks
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, backup-and-dr, disk-backup-plans, persistent-disk, hyperdisk, backup-vaults, disk-restore]
level: practitioner
status: docs-checked
description: "Back up individual Persistent Disk and Hyperdisk volumes with Backup and DR disk backup plans into vaults, restore disks, and choose this over VM backups or snapshot schedules."
sources: ["https://cloud.google.com/backup-disaster-recovery/docs/cloud-console/compute/disk-backup", "https://cloud.google.com/backup-disaster-recovery/docs/concepts/backup-plan", "https://cloud.google.com/compute/docs/disks/scheduled-snapshots"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup plans for standalone persistent disks

## When
| Need | Use |
|---|---|
| Whole VM (all disks, config) consistently | Backup and DR Compute Engine VM backup plan |
| Individual data disks (e.g. a shared data disk, GKE PV disks outside Backup for GKE, detached disks) | **disk backup plan** |
| Cheap operational restore points, same project | snapshot schedules |
| Tamper-proof retention, separate admin domain | vault-based plans (VM or disk) |

## Setup
```bash
gcloud backup-dr backup-plans create disk-daily --location=europe-west2 \
  --resource-type=compute.googleapis.com/Disk \
  --backup-vault=projects/<BACKUP_P>/locations/europe-west2/backupVaults/compute-vault \
  --backup-rule="rule-id=daily,retention-days=30,recurrence=DAILY,time-zone=Europe/London,backup-window-start=1,backup-window-end=5"
gcloud backup-dr backup-plan-associations create data-disk-assoc --location=europe-west2 \
  --resource=projects/<P>/zones/europe-west2-a/disks/data-1 --resource-type=compute.googleapis.com/Disk \
  --backup-plan=projects/<BACKUP_P>/locations/europe-west2/backupPlans/disk-daily
```
(Confirm flags with `--help`. `hourly-frequency` applies only when the recurrence is HOURLY; the backup-plan page says supplying it otherwise is a validation error.)
Workload project must grant the Backup and DR service agent the documented disk-backup roles.

## Restore
Restore creates a **new disk** (same or different zone/project) from a vault backup; attach to a VM
and mount. Validate the filesystem after restore.

## Gotchas
- Backups are crash-consistent; for databases flush/freeze or use app-level backups.
- Decide per tier whether a disk uses snapshot schedules, vault plans or both; see the vendor's pricing page for cost.

## Verify
- [ ] Association status ACTIVE, first backup succeeded, and a restored disk mounts with expected data.

## Checked
2026-10-28. Confirmed against the Backup and DR backup-plan concepts page: backup plans define frequency (hourly to yearly), retention and vault location; hourly frequency is required only for HOURLY recurrence and a value with any other recurrence is a validation error. check_commands.py found `gcloud backup-dr backup-plans create` and `backup-plan-associations create` flags valid.
Fixed: the example used `hourly-frequency=24` with `recurrence=DAILY`, which the docs say is a validation error.
Removed: unverified claims about deleted disks, doubled cost, regional disk path support and fsck advice.
Method: documentation only; no commands were run.
