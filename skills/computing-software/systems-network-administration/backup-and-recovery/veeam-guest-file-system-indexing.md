---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-guest-file-system-indexing
name: veeam-guest-file-system-indexing
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, guest-indexing, guest-file-system-catalog, enterprise-manager, file-search, guest-processing]
level: practitioner
status: draft
description: "Enable Veeam guest file system indexing so restore operators can search files across restore points in Enterprise Manager; scope, credentials, catalog sizing."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/overview.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Guest file system indexing

**Use when** help desk needs "find report.xlsx on any file server, any day last month" without mounting each restore point.

## Enable
Job > Guest Processing > tick **Enable guest file system indexing** > Indexing button per VM:
- Index everything
- Index everything except (default excludes Windows, Program Files, temp)
- **Index only following folders** (best: e.g. `%SystemDrive%\Shares`, `D:`-style data volumes as variables)

Guest OS credentials are required (same as application-aware processing); Linux needs `mlocate` or `plocate` installed in the guest.

## Where the catalog lives
- Indexes are built in the guest during backup, collected to the backup server's **VBRCatalog** folder, then pulled by Enterprise Manager into its catalog.
- Size the catalog drive: roughly 2-5 MB per million files per restore point kept; retention follows the job, with EM keeping 3 months by default (configurable).
- Move the catalog folder off the system drive via the `CatalogPath` registry value (per Veeam KB) on large estates.

## Searching
Enterprise Manager > Files tab: search by name/wildcard, filter by VM and date, then restore or download. Requires the job to be on a B&R server added to EM.

## Gotchas
- Indexing millions of small files adds minutes to the guest processing phase and can push jobs outside the window; scope to share folders.
- No index is built for crash-consistent jobs without guest credentials.

## Verify
Job log shows "Indexing guest file system: completed"; searching a known file in EM returns all restore points containing it.
