---
id: computing-software.systems-network-administration.backup-and-recovery.vadp-backup-snapshots-and-cleanup
name: vadp-backup-snapshots-and-cleanup
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [image-level-backup, vadp, vadp-snapshot, stuck-backup-snapshot, changed-block-tracking, hotadd, nbd, san-transport, vmware, vsphere]
level: practitioner
status: draft
description: "How VADP image backups use VM snapshots and CBT, transport modes (HotAdd, NBD, SAN), and cleaning up orphaned backup snapshots and hot-added disks left by failed jobs."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1020128
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VADP backup snapshots and cleanup

**Goal:** understand what image-level backup products do to VMware VMs, and fix the
leftovers when a backup fails halfway.

## Mechanism (vSphere Storage APIs - Data Protection)
1. Backup product asks vCenter for a VM **snapshot** (quiesced via VMware Tools/VSS if
   application-aware processing is off, or after the product's own guest processing).
2. Reads base disks via VDDK using **Changed Block Tracking** (CBT) to get only changed
   blocks since the last backup.
3. Deletes the snapshot (consolidation merges writes made during the backup).

## Transport modes
| Mode | Path | Notes |
|---|---|---|
| SAN / Direct storage access | Proxy reads LUNs directly over FC/iSCSI | Fastest, no ESXi load; proxy must not initialise or write to LUNs |
| **HotAdd** | Proxy VM mounts the snapshot's disks | Fast; proxy VM must be on a host that sees the datastore; leaves disks attached if a job crashes |
| NBD/NBDSSL | Over the ESXi management network | Always works, slowest; limited by management vmk bandwidth |

## Cleanup after failed jobs
1. Find leftover snapshots: names like "VEEAM BACKUP TEMPORARY SNAPSHOT", "Consolidate Helper",
   or vendor equivalents; and VMs with "consolidation needed".
   `Get-VM | Get-Snapshot | Where Name -match 'BACKUP|Consolidate'`
2. Check the **backup proxy VMs** for hot-added disks belonging to other VMs (Edit Settings
   → extra disks pointing to another VM's folder). Remove them **without deleting files**.
3. Delete the snapshot / run Consolidate on the protected VM.
4. If locked, see the snapshot consolidation skill (lock owner via `vmkfstools -D`).

## CBT problems
- After storage changes, restores from CBT-corrupt chains are the risk: products reset CBT
  in specific events; force a full or reset CBT (`ctkEnabled` false/true with a snapshot
  cycle) if the vendor KB says so.
- Known ESXi CBT bugs historically required full backups after patching; watch vendor KBs.

## Gotchas
- Snapshots on VMs with large, busy disks during backup grow fast; schedule heavy writers
  outside the backup window or use storage snapshot integration.
- Independent disks are excluded from snapshots and therefore from VADP backups.

## Verify
No backup-named snapshots older than a day; proxies have only their own disks; job logs
show the expected transport mode ("hotadd", "san") and CBT use.
