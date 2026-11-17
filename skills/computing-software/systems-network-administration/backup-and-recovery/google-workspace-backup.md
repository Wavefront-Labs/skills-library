---
id: computing-software.systems-network-administration.backup-and-recovery.google-workspace-backup
name: google-workspace-backup
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [google-workspace-backup, saas-backup, google-workspace, google-vault, gmail-backup, google-drive-backup]
level: practitioner
status: draft
description: "Back up Google Workspace (Gmail, Drive, shared drives, Calendar, Contacts): what Vault and native retention do not cover, third-party backup setup, restore windows and testing."
sources:
  - https://support.google.com/a/answer/2462365
  - https://support.google.com/vault/answer/2462365
  - https://support.google.com/a/answer/162106
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Google Workspace backup

**Goal:** recover deleted or corrupted Workspace data beyond Google's native windows, including after an account compromise or ransomware sync.

## What native tools do
- **Trash**: Drive items 30 days; admin can restore Drive/Gmail data for a user up to 25 days after it is permanently deleted (Admin console -> Users -> Restore data).
- **Google Vault**: retention and eDiscovery (holds, search, export). It preserves data for legal purposes but has no one-click restore into mailboxes or Drive; exports must be re-imported manually. Vault data for a deleted user disappears unless the account is retained (Archived User licence) or held.
- **Takeout / data export**: one-off exports, not a backup schedule.
So native features are retention, not recoverable backup.

## Third-party backup
Typical products: Spanning, Backupify, Afi, Synology Active Backup for Google Workspace, Veeam-partner products.
Setup pattern:
1. Create the app via Marketplace or a service account with **domain-wide delegation** and the scopes the vendor lists (Gmail, Drive, Calendar, Contacts, Admin SDK read).
2. Choose scope: all users (auto-add new users), shared drives, OUs.
3. Configure frequency (several times a day), retention, data region and encryption keys.
4. Protect the backup console: SSO with MFA, separate admin roles, no deletion by a single admin.

## Restore scenarios to support
- Single file or folder version, including sharing permissions.
- Whole mailbox or label to the same or a different user.
- Leaver account: retain backups after licence removal.
- Mass restore after ransomware-encrypted files synced from endpoints (restore to a point in time).

## Gotchas
- Google API quotas slow first full backups of large tenants (weeks for tens of TB).
- Shared drives are not owned by users; include them explicitly.
- Revoking the delegation stops backups silently; monitor job status.

## Verify
Quarterly: restore a deleted file with its permissions and a deleted Gmail label for a test user; time it.
