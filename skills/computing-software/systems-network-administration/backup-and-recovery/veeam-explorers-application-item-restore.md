---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-explorers-application-item-restore
name: veeam-explorers-application-item-restore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam-explorer, application-item-restore, active-directory-restore, sql-point-in-time, exchange-item-restore, veeam]
level: advanced
status: draft
description: "Restore application items with Veeam Explorers: AD objects and attributes, SQL databases to a point in time or export, Exchange mailboxes to PST, and the backup-side prerequisites."
sources:
  - https://helpcenter.veeam.com/docs/backup/explorers/explorers_introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application item restore with Veeam Explorers

**Goal:** recover a single deleted user, database or mailbox in minutes without restoring whole servers.

## Prerequisite at backup time
Application-aware processing enabled in the job (VSS for Windows apps). For SQL point-in-time restore, also **transaction log backup** in the job (log shipping to repository). Without these, explorers may still open data, but consistency and point-in-time options are limited.

## Active Directory
- Open the DC restore point in Veeam Explorer for Active Directory.
- Compare with production, restore deleted or changed **objects**, **attributes**, OUs, group membership, GPOs, AD-integrated DNS records.
- Restoring user accounts can include password hashes when restoring from the AD database (requires the original object restore path, not just attribute export).
- Restores go to the live directory; the account running the restore needs rights to write the objects.

## SQL Server
- Restore a database to the latest state, a **point in time**, or a specific transaction (when log backups exist), to the original or another instance.
- **Export** as `.bak` files or detached MDF/LDF for DBAs.
- **Publish** (instant) mounts the database from the backup to a SQL instance for quick access.

## Exchange / SharePoint / Microsoft 365
- Open EDB files from the backup, search mailboxes, restore items to original/another mailbox, or export to PST (PST export requires a 64-bit Outlook installed on the console machine).
- SharePoint documents, lists, sites; Microsoft 365 objects via Veeam Backup for Microsoft 365.

## Others
Oracle (point in time with redo logs), PostgreSQL, and Teams/OneDrive via respective explorers.

## Gotchas
- Explorers mount backup files over the network from the repository; slow links slow restores.
- AD tombstone/recycle bin restores may be faster for very recent deletions; use the explorer when attributes or older states are needed.

## Verify
Quarterly: restore a test user with group memberships, a test database to a point in time on a non-production instance, and a test mailbox item; confirm contents.
