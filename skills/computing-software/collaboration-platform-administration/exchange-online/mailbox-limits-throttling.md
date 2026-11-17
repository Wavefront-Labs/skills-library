---
id: computing-software.collaboration-platform-administration.exchange-online.mailbox-limits-throttling
name: mailbox-limits-throttling
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [mailbox-limits-throttling]
level: practitioner
status: draft
description: Know quotas and sending limits and adjust them within service caps.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mailbox, message and recipient limits
**Goal:** Know quotas and sending limits and adjust them within service caps.

- Mailbox size depends on plan (commonly 50 GB or 100 GB; archives auto-expand; confirm per plan).
- Message size: default 25 MB send limit for Exchange Online; max 150 MB via `Set-TransportConfig -MaxSendSize`. Recipient limit 500 per message; per-day recipient rate limit 10,000.
- Set per mailbox: `Set-Mailbox -MaxSendSize 50MB`.
- Enable archive: `Enable-Mailbox -Archive`.

## Gotchas
- Encoding adds about 33 percent to attachment size.
- Verify current limits at the Exchange Online limits page.

## Self-check
`Get-Mailbox <id> | fl MaxSendSize,ProhibitSendQuota` match your plan.
