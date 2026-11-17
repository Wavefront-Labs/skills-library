---
id: computing-software.collaboration-platform-administration.tenant-migration.post-migration-validation
name: post-migration-validation
category: computing-software
field: collaboration-platform-administration
product: tenant-migration
tags: [post-migration-validation]
level: practitioner
status: draft
description: Prove the migration worked and close it out.
sources: ['https://learn.microsoft.com/en-us/exchange/mailbox-migration/mailbox-migration', 'https://learn.microsoft.com/en-us/sharepointmigration/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-migration validation
**Goal:** Prove the migration worked and close it out.

- Compare item counts per mailbox (`Get-MailboxStatistics`) against the source.
- Verify permissions, delegates, rules, calendar sharing and mobile connectivity.
- Check shared mailbox and group moves and licence assignment.
- Decommission the source after the agreed retention window; export a final report.

## Gotchas
- Outlook cached mode may need profile recreation.
- Retain evidence for audit.

## Self-check
A signed-off checklist per batch with a helpdesk watch period.
