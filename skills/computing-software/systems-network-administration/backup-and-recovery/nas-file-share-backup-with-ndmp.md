---
id: computing-software.systems-network-administration.backup-and-recovery.nas-file-share-backup-with-ndmp
name: nas-file-share-backup-with-ndmp
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [ndmp, file-share-backup, nas-backup, netapp, snapshots, dump-restore]
level: advanced
status: draft
description: "Back up NAS file shares: NDMP dumps to tape or disk, snapshot-based and file-level alternatives, DAR restores, and choosing between NDMP and modern NAS backup."
sources:
  - https://docs.netapp.com/us-en/ontap/ndmp/index.html
  - https://www.snia.org/ndmp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAS and file share backup with NDMP

## Methods
| Method | How | Pros | Cons |
|---|---|---|---|
| **NDMP** | Filer dumps a volume image to a backup server or tape via NDMP protocol | Preserves ACLs/streams, works with old tape workflows | Vendor-format dumps, often full volume restores, poor granularity, slow incrementals |
| File-level over SMB/NFS | Backup tool reads files from a snapshot path | Granular, cross-vendor restores | Scan time on millions of files |
| NAS integration with change tracking | Backup tool uses filer snapshot diff APIs | Fast incrementals | Vendor support needed |
| Array snapshots + replication | SnapMirror, SyncIQ | Fast, cheap restores | Same vendor, not a separate backup unless isolated |

## NDMP setup (NetApp ONTAP example)
1. Enable SVM-scoped NDMP: `vserver services ndmp on -vserver svm1`; generate the NDMP password with `vserver services ndmp generate-password -vserver svm1 -user ndmpuser`.
2. Add the filer in the backup software as an NDMP server (port 10000).
3. Create jobs per volume; dump levels 0 (full) and 1-9 (incremental since lower level).
4. Enable **DAR** (Direct Access Recovery) so single-file restores seek directly instead of reading the whole dump.

## When to choose NDMP today
Existing tape-based compliance archives, very large volumes where file scanning is impractical, or filers without integration support. Otherwise prefer change-tracking NAS integration or file-level backup from snapshots.

## Gotchas
- NDMP dumps can usually only restore to the same vendor's filer.
- Restores of a few files from a non-DAR dump read the whole image.
- Three-way NDMP (filer -> backup server -> tape) needs network sizing.

## Verify
Restore a directory with ACLs to an alternate volume and compare permissions with `icacls` or `ls -l`/`getfacl`.
