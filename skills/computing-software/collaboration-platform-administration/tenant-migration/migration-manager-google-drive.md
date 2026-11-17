---
id: computing-software.collaboration-platform-administration.tenant-migration.migration-manager-google-drive
name: migration-manager-google-drive
category: computing-software
field: collaboration-platform-administration
product: tenant-migration
tags: [migration-manager-google-drive]
level: advanced
status: draft
description: Use Migration Manager in the SharePoint admin center for large scale moves, including Google Drive.
sources: ['https://learn.microsoft.com/en-us/exchange/mailbox-migration/mailbox-migration', 'https://learn.microsoft.com/en-us/sharepointmigration/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration Manager and Google Drive moves
**Goal:** Use Migration Manager in the SharePoint admin center for large scale moves, including Google Drive.

- SharePoint admin center > Migration > Migration Manager; install agents on source servers.
- Google Workspace source: Migration Manager connects to Google Drive via a service account (confirm steps in docs).
- Map users and run tasks in waves.
- Use scan only to preview.

## Gotchas
- Sharing permissions from Google map imperfectly.
- Google native formats convert to Office formats.

## Self-check
Sample documents open correctly and permission spot checks pass.
