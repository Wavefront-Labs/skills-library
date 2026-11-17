---
id: computing-software.systems-network-administration.backup-and-recovery.snapshot-space-planning-for-backups
name: snapshot-space-planning-for-backups
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [snapshot-space, vm-image-backup, datastore-capacity, vmware-snapshots, lvm-snapshots, backup-snapshots]
level: practitioner
status: docs-checked
description: "Plan datastore and volume free space for backup snapshots: delta growth from change rate and duration, VMware, Hyper-V and LVM thin pool behaviour, and cleanup checks."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1025279
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/choose-between-standard-or-production-checkpoints-in-hyper-v
  - https://man7.org/linux/man-pages/man7/lvmthin.7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot space planning for image backups

**Goal:** backup snapshots never fill a datastore or volume and take production down.

## Size the delta
Delta growth is roughly VM write rate x snapshot lifetime (backup duration plus any replication/copy time). Illustration: a database writing 50 MB/s for a 2 h backup (7,200 s) creates about 360 GB of delta. Backup tools see *changed blocks*, while a snapshot delta sees *every write*, so measure the VM's own write rate, not only the backup's "transferred" figure.

## Platform behaviour
| Platform | Delta | Notes from the vendor docs |
|---|---|---|
| VMware | `virtual_machine-00000#-delta.vmdk` per disk | The snapshot file keeps growing the longer it is kept and can fill the storage location and hurt performance. |
| Hyper-V | `.avhdx` files beside the `.vhdx` | Deleting a checkpoint merges the `.avhdx` back; do not delete `.avhdx` files directly. |
| LVM thin | thin pool shared by all thin volumes | Data and metadata usage must be watched; extend the pool before either reaches 100%. |

## Rules
- VMware (Broadcom guidance): snapshots are not backups; keep no single snapshot longer than 72 hours; supported chain maximum is 32, but 2 to 3 is better for performance; with third-party backup software make sure snapshots are deleted after a successful backup; snapshots taken by third-party software via API may not show in Snapshot Manager, so check from the command line; do not cancel a running deletion/consolidation task (risk of corruption); do not grow a disk while snapshots exist.
- Hyper-V: a standard checkpoint is not a full backup and can cause consistency problems for systems that replicate between nodes such as Active Directory.
- LVM thin pools: `activation/thin_pool_autoextend_threshold` (and `thin_pool_autoextend_percent`) in lvm.conf let the pool grow automatically; setting the threshold to 100 disables autoextend. The thin pool's "when full" property (`lvs -o whenfull`, set with `lvchange --errorwhenfull y|n`) chooses between erroring and queueing I/O when the pool fills.
- Stagger backups so not all VMs on one datastore are in snapshot at once; back up write-heavy VMs off-peak.
- Decide your own free-space reserve from measured delta growth and consolidation needs; this skill gives no fixed percentage.

## Gotchas
- Backup jobs failing mid-run can leave snapshots behind; detect them.

## Verify
Daily report of snapshot age and size per VM and datastore free space; no snapshot older than the vendor limit without a ticket.

## Checked

2026-11-09. Confirmed against Broadcom KB "Best practices for using VMware snapshots" (delta.vmdk naming, 72 hours, 32 maximum chain and 2 to 3 recommended, delete after backup, command-line check, consolidation caution), Microsoft "Choose between standard or production checkpoints" (.avhdx location, merge on delete, standard checkpoint caveats) and lvmthin(7) (autoextend threshold, 100 disables, whenfull error/queue, extend before 100%). Removed: 15-20% free-space rule, Paused-Critical, VMFS/NFS and sesparse detail, thick LVM snapshot behaviour, ZFS/Ceph pool claims, array snapshot row, Veeam storage-snapshot integration, VMware alarms, and the wrong `snapshot_autoextend_threshold` name (the setting is `thin_pool_autoextend_threshold`).

Method: documentation only; no commands were run.
