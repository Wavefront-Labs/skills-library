---
id: computing-software.collaboration-platform-administration.exchange-online.user-shared-mailbox
name: user-shared-mailbox
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [user-shared-mailbox, exo-mailbox-types]
level: practitioner
status: draft
description: Create and manage shared mailboxes and convert between user and shared types.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# User and shared mailboxes
**Goal:** Create and manage shared mailboxes and convert between user and shared types.

- `New-Mailbox -Shared -Name Support -DisplayName Support -PrimarySmtpAddress support@contoso.com`.
- `Set-Mailbox -Identity <id> -Type Shared|Regular` converts types.
- Shared mailboxes need no licence under 50 GB and without archive or holds.
- Add members via `Add-MailboxPermission` and `Add-RecipientPermission`, or the admin center.

## Gotchas
- Signing in directly to a shared mailbox account should be blocked; access it via delegation.
- Auto-mapping can be turned off with `-AutoMapping $false`.

## Self-check
`Get-Mailbox -Identity support | fl RecipientTypeDetails` returns SharedMailbox.
