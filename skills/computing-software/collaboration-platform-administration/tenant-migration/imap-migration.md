---
id: computing-software.collaboration-platform-administration.tenant-migration.imap-migration
name: imap-migration
category: computing-software
field: collaboration-platform-administration
product: tenant-migration
tags: [imap-migration]
level: practitioner
status: draft
description: Migrate mail from IMAP or Google Workspace.
sources: ['https://learn.microsoft.com/en-us/exchange/mailbox-migration/mailbox-migration', 'https://learn.microsoft.com/en-us/sharepointmigration/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IMAP and Google Workspace sources
**Goal:** Migrate mail from IMAP or Google Workspace.

- IMAP: EAC > Migration > IMAP endpoint; CSV with EmailAddress, UserName, Password.
- Google Workspace: use the Gmail migration endpoint (Google service account with domain-wide delegation) in EAC.
- Contacts and calendar are not part of IMAP; use Google endpoint for those types.
- Only mail from the date range accessible is moved.

## Gotchas
- App passwords or admin access needed for IMAP.
- Service account key handling must follow security policy.

## Self-check
Mailbox item counts agree between source and destination.
