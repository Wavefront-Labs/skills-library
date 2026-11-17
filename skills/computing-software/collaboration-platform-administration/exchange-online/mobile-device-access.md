---
id: computing-software.collaboration-platform-administration.exchange-online.mobile-device-access
name: mobile-device-access
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [mobile-device-access]
level: practitioner
status: draft
description: Control which mobile devices can connect.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile device access (ActiveSync)
**Goal:** Control which mobile devices can connect.

- `Get-MobileDevice`, `Set-CASMailbox -ActiveSyncEnabled`.
- Access rules: Allow, Block or Quarantine by device family/model.
- Prefer Outlook mobile with app protection through Intune (reference Intune product).
- Remote wipe via Exchange admin center is for ActiveSync devices; use Intune where managed.

## Gotchas
- Quarantine is the default for new devices only if set in organisation settings.
- A wipe removes all data on non-managed devices; confirm first.

## Self-check
A test device lands in the expected allow/block/quarantine state.
