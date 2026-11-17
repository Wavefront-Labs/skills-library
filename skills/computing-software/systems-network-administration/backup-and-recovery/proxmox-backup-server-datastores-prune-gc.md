---
id: computing-software.systems-network-administration.backup-and-recovery.proxmox-backup-server-datastores-prune-gc
name: proxmox-backup-server-datastores-prune-gc
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [proxmox-backup-server, pbs-datastore, pbs-garbage-collection, pbs-prune, chunk-store, namespaces, proxmox-backup]
level: advanced
status: docs-checked
description: "Run Proxmox Backup Server datastores: creation and chunk store layout, namespaces, prune jobs, two-phase garbage collection and its atime requirement, and maintenance modes."
sources:
  - https://pbs.proxmox.com/docs/storage.html
  - https://pbs.proxmox.com/docs/maintenance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PBS datastores, prune and garbage collection

**Goal:** deduplicated backup storage that stays within capacity and keeps the retention it promises.

## Datastore
```bash
proxmox-backup-manager datastore create store1 /mnt/datastore/store1
proxmox-backup-manager datastore list
```
Layout: a `.chunks` directory with content-addressed chunks (deduplicated across all backups in the datastore) and per-group snapshot directories with index files. Use **namespaces** to separate clusters, tenants or retention classes within one datastore while still deduplicating.

Many small chunk files: the PBS docs recommend a fast metadata cache, for example a ZFS special device mirror.

## Prune (remove snapshots per policy)
Configured as prune jobs per datastore/namespace:
```bash
proxmox-backup-manager prune-job create daily-prune --store store1 --schedule daily \
  --keep-last 3 --keep-daily 7 --keep-weekly 4 --keep-monthly 6
```
Pruning removes snapshot indexes only; space is freed by garbage collection.

## Garbage collection (two phases)
1. **Mark**: read every index and update the access time (atime) of every referenced chunk.
2. **Sweep**: delete chunks whose atime is older than 24 hours and 5 minutes (and older than the oldest running backup).
Schedule GC after prune (e.g. daily); `proxmox-backup-manager garbage-collection start store1`.
The filesystem must support atime updates; the default `relatime` mount option is fine (the docs describe an atime update safety check).

## Maintenance mode
`read-only` (restores allowed, no new backups) or `offline` (unmount disks, replace storage), set with `proxmox-backup-manager datastore update <store> --maintenance-mode`.

## Gotchas
- Deleting snapshots manually without GC frees nothing.

## Verify
GC task logs show removed chunks and freed bytes, and datastore usage trend is stable relative to retention.

## Checked

2026-10-28

Confirmed: PBS maintenance and storage docs: prune-job create and keep-* options, two-phase GC (mark updates atime, sweep with 24 hours and 5 minutes cutoff), garbage-collection start, maintenance modes read-only and offline.

Removed or corrected: filesystem recommendation, relatime explanation, GUI path, free-space percentage.

Method: documentation only; no commands were run.
