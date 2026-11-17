---
id: computing-software.collaboration-platform-administration.tenant-migration.hybrid-remote-move
name: hybrid-remote-move
category: computing-software
field: collaboration-platform-administration
product: tenant-migration
tags: [hybrid-remote-move]
level: advanced
status: draft
description: Move mailboxes between on-premises and Exchange Online with MRS.
sources: ['https://learn.microsoft.com/en-us/exchange/mailbox-migration/mailbox-migration', 'https://learn.microsoft.com/en-us/sharepointmigration/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hybrid remote move migrations
**Goal:** Move mailboxes between on-premises and Exchange Online with MRS.

- EAC > Migration > Add migration batch > Migration to Exchange Online (remote move).
- PowerShell: `New-MoveRequest` or `New-MigrationBatch -SourceEndpoint <hybrid>` with `-TargetDeliveryDomain`.
- Review `Get-MoveRequestStatistics -IncludeReport`.
- Large item and bad item limits: set `-BadItemLimit`, `-LargeItemLimit` and approve skipped items.

## Gotchas
- Autodiscover must point to the correct place after each move.
- Outlook profiles update on first connection; test clients.

## Self-check
Moved mailbox opens in Outlook with no data loss in the statistics.
