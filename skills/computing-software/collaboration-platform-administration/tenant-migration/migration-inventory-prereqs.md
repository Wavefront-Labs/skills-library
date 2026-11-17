---
id: computing-software.collaboration-platform-administration.tenant-migration.migration-inventory-prereqs
name: migration-inventory-prereqs
category: computing-software
field: collaboration-platform-administration
product: tenant-migration
tags: [migration-inventory-prereqs]
level: practitioner
status: draft
description: Assess source, licences, DNS and clients before moving.
sources: ['https://learn.microsoft.com/en-us/exchange/mailbox-migration/mailbox-migration', 'https://learn.microsoft.com/en-us/sharepointmigration/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inventory and prerequisites
**Goal:** Assess source, licences, DNS and clients before moving.

- Inventory mailboxes, sizes, delegates, shared mailboxes, public folders, archives, rules.
- Pre-assign licences and verify domains.
- Reduce TTL on MX/autodiscover a few days ahead.
- Identify client changes (Outlook profiles, mobile).

## Gotchas
- Public folders need a separate migration path.
- Large mailboxes dominate time.

## Self-check
Inventory spreadsheet reconciles to the user list.
