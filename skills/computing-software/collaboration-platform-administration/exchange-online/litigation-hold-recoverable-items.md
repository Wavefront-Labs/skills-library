---
id: computing-software.collaboration-platform-administration.exchange-online.litigation-hold-recoverable-items
name: litigation-hold-recoverable-items
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [litigation-hold-recoverable-items, exo-retention-recovery]
level: practitioner
status: draft
description: Preserve mailbox content and understand the dumpster.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Litigation hold and Recoverable Items
**Goal:** Preserve mailbox content and understand the dumpster.

- `Set-Mailbox <id> -LitigationHoldEnabled $true -LitigationHoldDuration 2555`.
- Purview retention policies are preferred for new work; litigation hold remains valid.
- Recoverable Items limit 100 GB (with hold, the quota is raised and archive expansion may be needed, confirm).
- Users recover deleted items via Outlook > Recover deleted items; default retention 14 days, up to 30 (`Set-Mailbox -RetainDeletedItemsFor`).

## Gotchas
- Removing a hold can result in immediate purge of items past retention.
- Check `Get-Mailbox | fl *Hold*` for all hold sources.

## Self-check
`Get-Mailbox <id> | fl LitigationHoldEnabled,InPlaceHolds` shows the expected holds.
