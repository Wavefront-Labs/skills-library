---
id: computing-software.collaboration-platform-administration.tenant-migration.migration-method-selection
name: migration-method-selection
category: computing-software
field: collaboration-platform-administration
product: tenant-migration
tags: [migration-method-selection, mig-planning]
level: practitioner
status: draft
description: Pick cutover, staged, hybrid or IMAP migration by size and source.
sources: ['https://learn.microsoft.com/en-us/exchange/mailbox-migration/mailbox-migration', 'https://learn.microsoft.com/en-us/sharepointmigration/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choose a migration method
**Goal:** Pick cutover, staged, hybrid or IMAP migration by size and source.

- Cutover: Exchange on-premises, fewer than 2000 mailboxes (recommended under 150), one-time move.
- Staged: older Exchange 2003/2007 only (staged migration is not available for newer versions, confirm).
- Hybrid: Exchange 2010+ for longer coexistence and larger counts.
- IMAP: any IMAP source; mail only, not calendar or contacts.

## Gotchas
- Check supported source version before choosing.
- Plan for coexistence of free/busy and GAL.

## Self-check
A written plan lists method, batch sizes and rollback.
