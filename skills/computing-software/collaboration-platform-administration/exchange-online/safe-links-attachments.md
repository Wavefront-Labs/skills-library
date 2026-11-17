---
id: computing-software.collaboration-platform-administration.exchange-online.safe-links-attachments
name: safe-links-attachments
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [safe-links-attachments]
level: practitioner
status: draft
description: Enable time-of-click URL scanning and attachment detonation.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Safe Links and Safe Attachments
**Goal:** Enable time-of-click URL scanning and attachment detonation.

- Needs Defender for Office 365 Plan 1 or 2 (licensing: confirm).
- Safe Links: enable for email, Teams and Office apps; disable 'Let users click through'.
- Safe Attachments: Block or Dynamic Delivery; enable for SharePoint/OneDrive/Teams in global settings.
- Exclude via a policy 'do not rewrite' list sparingly.

## Gotchas
- Dynamic Delivery delays attachments for scan; communicate to users.
- Don't exclude whole domains without a risk note.

## Self-check
Click a test safe-links URL (EICAR-like safe test pages from docs) and verify rewriting.
