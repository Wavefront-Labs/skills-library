---
id: computing-software.systems-network-administration.backup-and-recovery.storage-snapshots-vs-backups
name: storage-snapshots-vs-backups
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [storage-snapshot, snapshot-vs-backup, backup-methods, 3-2-1, failure-domain, rpo]
level: practitioner
status: draft
description: "Explain and design the role of storage snapshots versus real backups: failure domains, consistency, retention, performance cost, and using both together for low RPO and safety."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
  - https://www.cisa.gov/stopransomware/ransomware-guide
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Storage snapshots vs backups

## The difference
| | Snapshot (array, ZFS, VM, cloud disk) | Backup |
|---|---|---|
| Location | same storage system (pointer-based) | separate system/media, ideally offsite |
| Survives storage failure / array loss | **no** | yes |
| Survives admin/ransomware deleting the volume | only if immutable/locked snapshots | yes if isolated/immutable |
| Speed to create/restore | seconds | minutes-hours |
| Typical retention | hours-days | weeks-years |
| Consistency | crash-consistent unless orchestrated with app quiesce | app-consistent with agent/VSS |
| Performance impact | CoW/RoW overhead grows with count and age (VM snapshots especially) | load during backup window |

A snapshot is a recovery point, not a backup, until it's **copied** to another failure
domain (replication to another array/region, or backup software reading from it).

## Use together
- Frequent snapshots (every 15-60 min, keep 24-72 h) for fast operational restores and low RPO.
- Daily backups to separate storage, plus an offsite/immutable copy (3-2-1-1-0).
- Backup software can use array snapshots as a source (Veeam storage snapshot
  integration, NetApp SnapCenter) to reduce VM snapshot time.

## VM snapshots specifically
VMware/Hyper-V/Proxmox VM snapshots are short-term change tools. Long-lived VM snapshots
degrade performance and fill datastores; never use them as backups.

## Cloud
EBS/managed-disk snapshots are stored separately from the volume (in S3/Azure storage) but in
the **same account/region**: copy to another account and region with locks (AWS Backup vault
lock, Azure immutable vaults) to make them backups.

## Gotchas
- Snapshot reserve/space exhaustion can delete old snapshots automatically (array autodelete)
  or take volumes offline.
- Snapshots of encrypted-by-ransomware data are just as encrypted: you need points before
  the encryption began, which short retention may not have.

## Verify
For each tier, you can name snapshot frequency/retention and the separate-failure-domain
backup copy; a test restore from the backup (not the snapshot) succeeds.
