---
id: computing-software.collaboration-platform-administration.exchange-online.mailbox-delegation-permissions
name: mailbox-delegation-permissions
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [mailbox-delegation-permissions]
level: practitioner
status: draft
description: Grant the right delegation type and avoid unintended access.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mailbox permissions (Full Access, Send As, Send on Behalf)
**Goal:** Grant the right delegation type and avoid unintended access.

- Full Access: `Add-MailboxPermission -Identity <mbx> -User <user> -AccessRights FullAccess -AutoMapping $false`.
- Send As: `Add-RecipientPermission -Identity <mbx> -Trustee <user> -AccessRights SendAs`.
- Send on Behalf: `Set-Mailbox <mbx> -GrantSendOnBehalfTo @{Add='user'}`.
- Audit with `Get-MailboxPermission` and `Get-RecipientPermission`.

## Gotchas
- Permissions can take up to about an hour to appear in Outlook.
- Full Access does not include Send As.

## Self-check
Run both Get- cmdlets and confirm only intended trustees appear.
