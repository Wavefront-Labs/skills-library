---
id: computing-software.collaboration-platform-administration.exchange-online.quarantine-management
name: quarantine-management
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [quarantine-management]
level: practitioner
status: draft
description: Manage quarantine, notifications and user release rights.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quarantine policies and release
**Goal:** Manage quarantine, notifications and user release rights.

- Defender portal > Email & collaboration > Review > Quarantine.
- Quarantine policies control user access (no access, limited, full) per threat type.
- Release or report false positives to Microsoft from the same view.
- Configure end-user spam notifications and an admin review SLA.

## Gotchas
- High-confidence phish should stay admin-release only.
- Retention in quarantine is limited (default 30 days for most types; confirm).

## Self-check
Quarantined test message appears; policy permits only the intended release action.
