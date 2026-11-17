---
id: computing-software.systems-network-administration.backup-and-recovery.granular-item-restore-testing
name: granular-item-restore-testing
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [granular-restore, restore-testing, item-level-restore, application-item-recovery, veeam-explorers]
level: practitioner
status: docs-checked
description: "Test granular restores of application items from image backups with Veeam Explorers, and know the AD Recycle Bin limits for deleted objects."
sources:
  - https://helpcenter.veeam.com/docs/backup/explorers/explorers_introduction.html
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/adac/introduction-to-active-directory-administrative-center-enhancements--level-100-
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Granular item restore testing

**Goal:** prove you can return the most frequent real restore requests (a mailbox item, an AD object, a database item) quickly and correctly.

## Which Veeam Explorer covers what
Veeam Explorers need no separate install or licence; the feature set depends on the edition of the Veeam product.

| Explorer | In Veeam Backup & Replication | In Veeam Backup for Microsoft 365 |
|---|---|---|
| Microsoft Exchange, SharePoint, OneDrive, Teams | yes | yes |
| Microsoft Active Directory, SQL Server, Oracle, PostgreSQL, SAP HANA, MongoDB | yes | no |

## AD objects without a backup
The AD Recycle Bin can restore deleted objects, with limits (Microsoft):
- It needs a Windows Server 2008 R2 forest functional level and Enterprise Admins membership to enable; enabling is irreversible, and it grows the NTDS.DIT database on every domain controller over time.
- It is not fully functional until all domain controllers replicate the change.
- Active Directory Administrative Center restores only domain partitions; for other partitions use `Restore-ADObject`.
- It cannot restore a subtree in one action: restoring a deleted OU does not restore its child objects.

## Method
1. Plant known test items with known content and permissions, back them up, then delete or modify them.
2. Run the restore as a service-desk tech would, following the runbook.
3. Measure time from ticket to user confirmation.
4. Verify content and metadata, and choose restore to an alternate location or overwrite deliberately.

## Verify
A quarterly granular test per item type is recorded with time-to-restore and outcome; failures go into the backup design backlog.

## Checked

2026-11-09. Confirmed against the Veeam Explorers Overview (table of explorers, no extra install or licence) and the Microsoft Active Directory Administrative Center page and its Recycle Bin section (forest level, irreversible, database growth, partitions, subtree limit). Partial read of the long Microsoft page. Removed: file-level tools (PBS, restic), GPO and SQL restore methods, SharePoint version history, authoritative restore claims, the application-aware requirement and restore-credential remarks, and the claim that tests should run quarterly as a rule (kept only as a suggestion in Verify).

Method: documentation only; no commands were run.
