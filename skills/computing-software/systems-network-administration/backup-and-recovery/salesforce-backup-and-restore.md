---
id: computing-software.systems-network-administration.backup-and-recovery.salesforce-backup-and-restore
name: salesforce-backup-and-restore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [salesforce-backup, saas-backup, salesforce, data-export, metadata-backup, record-restore]
level: advanced
status: draft
description: "Back up and restore Salesforce data and metadata: weekly data export, Salesforce Backup and third-party tools, metadata retrieval, and restoring related records with new IDs."
sources:
  - https://help.salesforce.com/s/articleView?id=sf.admin_exportdata.htm
  - https://help.salesforce.com/s/articleView?id=sf.backup_restore_intro.htm
  - https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_project_commands_unified.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Salesforce backup and restore

**Goal:** recover Salesforce records (and their relationships) and configuration after bad data loads, integration bugs or malicious deletion.

## Native options
- **Recycle Bin**: deleted records for 15 days (subject to storage limits); hard-deleted and mass-updated records are not there.
- **Data Export service** (Setup -> Data Export): weekly (or monthly on lower editions) CSV zip of objects, optionally with files/attachments. Links expire after 48 h. Useful as a baseline, not a restore tool.
- **Salesforce Backup** (paid add-on) and acquired third-party (Own): scheduled backups, compare and restore in the UI.
- Field history tracking helps reconstruct values but is not a backup.

## Third-party / DIY
- Products: Own, OwnBackup-style tools, Odaseva, Gearset, Veeam Backup for Salesforce.
- DIY data: Bulk API exports (Data Loader CLI) of all objects daily.
- Metadata: `sf project retrieve start --manifest package.xml --target-org prod` into Git; covers objects, fields, flows, Apex, profiles/permission sets.

## Restore is the hard part
- Re-inserted records get **new IDs**; children and lookups must be re-pointed. Restore in dependency order (Accounts, then Contacts, then Opportunities, ...) and map old IDs to new.
- Use external ID fields and `upsert` to keep restores idempotent.
- Disable triggers, flows, validation rules and duplicate rules (or use a bypass permission) during restore to avoid side effects (emails, integrations).
- Owners, record types and inactive users must exist.
- Mass updates (not deletes) are restored by updating fields from the backup snapshot for affected IDs.

## Gotchas
- API call limits: backups and restores consume them; schedule off-peak and check the org's daily limit.
- Files (ContentVersion) and big objects are often excluded by default.
- Sandbox refreshes are not backups (and copy production data, so mind privacy).

## Verify
Quarterly in a full sandbox: delete a parent with children, restore from backup, confirm relationships, record counts and that no automation fired.
