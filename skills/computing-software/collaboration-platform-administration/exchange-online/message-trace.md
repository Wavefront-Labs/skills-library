---
id: computing-software.collaboration-platform-administration.exchange-online.message-trace
name: message-trace
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [message-trace, exo-troubleshooting]
level: practitioner
status: draft
description: Find where a message went using message trace.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Message trace
**Goal:** Find where a message went using message trace.

- Exchange admin center > Mail flow > Message trace; or `Get-MessageTraceV2` (cmdlet name per current docs; older `Get-MessageTrace` is being replaced, confirm).
- Quick trace covers 10 days; use start/end traces for older, up to 90 days (confirm).
- Read Status: Delivered, Failed, Pending, Quarantined, FilteredAsSpam, Expanded.
- Open message details for events and the NDR text.

## Gotchas
- Subject/body are not searchable; use sender, recipient, message ID.
- Time zone defaults can mislead; use UTC.

## Self-check
Trace by Message-ID returns the same final status the recipient experienced.
