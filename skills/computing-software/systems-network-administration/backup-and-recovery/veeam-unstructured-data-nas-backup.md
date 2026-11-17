---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-unstructured-data-nas-backup
name: veeam-unstructured-data-nas-backup
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-nas-backup, file-share-backup, unstructured-data, smb, nfs, changed-file-tracking]
level: advanced
status: draft
description: "Protect SMB and NFS shares and NAS filers with Veeam unstructured data backup: file proxies, cache repository, storage snapshots, retention and file restores."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/overview.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam unstructured data (NAS) backup

## Components
- **File share** source: SMB share, NFS export, Windows/Linux managed server folders, or an enterprise NAS (NetApp, Isilon/PowerScale, Lenovo, etc.) added via storage integration.
- **General-purpose backup proxy**: reads files; many concurrent threads per proxy.
- **Cache repository**: holds metadata about the last state so incrementals only need a metadata compare; put on fast disk near the proxy. It is not a backup target.
- **Backup repository** (disk or object) for data; optional archive repository for long-term versions.

## Job setup
1. Add the share (prefer backing up from a **storage snapshot** or VSS snapshot path so open files are consistent).
2. Choose files and folders, include/exclude masks.
3. Retention: "Keep all file versions for N days/months"; optionally archive older versions to a cheaper repository for years.
4. Schedule; first run reads everything, incrementals use changed file tracking (NAS integration) or a full metadata scan.

## Performance
- Millions of small files: scan time dominates; use NAS integration with change tracking (e.g. NetApp, PowerScale) or split shares into multiple jobs.
- Set proxy threads (Advanced > Backup I/O control) to protect the filer.

## Restore
Restore entire share, folders, or individual files to original/alternate location; **rollback to a point in time** restores only files changed since then, useful after ransomware.

## Verify
Job reports files processed and transferred; restore a folder to an alternate path and compare counts and hashes.
