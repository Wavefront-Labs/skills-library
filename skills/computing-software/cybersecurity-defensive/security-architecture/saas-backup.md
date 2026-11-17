---
id: computing-software.cybersecurity-defensive.security-architecture.saas-backup
name: saas-backup
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [saas-backup, microsoft-365-backup, google-workspace-backup, salesforce-backup, shared-responsibility, ransomware-recovery, retention]
level: practitioner
status: draft
description: "Back up SaaS data (Microsoft 365, Google Workspace, Salesforce, GitHub): why native retention is not backup, tool choice, scope, immutability and restore testing."
sources: ["https://learn.microsoft.com/en-us/microsoft-365/backup/backup-overview", "https://help.salesforce.com/s/articleView?id=sf.backup_restore_intro.htm", "https://support.google.com/a/answer/7068143"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SaaS backup

SaaS providers protect against their infrastructure failing, not against your admin deleting a
mailbox, a malicious OAuth app wiping files, sync-propagated ransomware or a retention gap.

## Native features are not backups
| Feature | Limit |
|---|---|
| M365 recycle bins / retention policies | Admin or attacker with Global Admin can change them; restore is coarse |
| Google Vault | eDiscovery/hold tool, not point-in-time restore of Drive structure |
| Salesforce Recycle Bin (15 days) | Metadata and large data loss not covered; use Salesforce Backup or third party |

## Scope
Mailboxes, OneDrive/SharePoint/Teams, Google Drive/Gmail, Salesforce data and metadata, Entra/Okta
configuration (users, groups, CA policies), GitHub/GitLab repositories with issues and wikis.

## Design
- Third-party or Microsoft 365 Backup with backup stored **outside** the tenant's admin control (separate credentials, separate IdP admin, ideally different cloud).
- Immutability/retention lock so a compromised SaaS admin cannot purge backups.
- Frequency per RPO (many tools: several times daily for Exchange/SharePoint).
- API throttling limits throughput; size initial seeding and large restores.

## Restore testing
Quarterly: restore a deleted mailbox folder, a SharePoint site to an earlier point, a Salesforce
object with relationships. Time the restores against the RTO.

## Gotchas
- Backup app registrations have high privileges (Mail.ReadWrite, Sites.FullControl.All); protect and monitor them as tier 0.
- Licence-based retention: deleting a user's licence may purge their data before backup catches up.
- Salesforce restores must respect relationship order (parents before children).

## Verify
- [ ] Backup coverage report = 100% of in-scope users/sites.
- [ ] Restore test met RTO.
- [ ] Backup console uses separate admin identity with MFA.
