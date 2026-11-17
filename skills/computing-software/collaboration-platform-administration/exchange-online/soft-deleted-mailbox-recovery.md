---
id: computing-software.collaboration-platform-administration.exchange-online.soft-deleted-mailbox-recovery
name: soft-deleted-mailbox-recovery
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [soft-deleted-mailbox-recovery]
level: practitioner
status: draft
description: Restore a deleted mailbox within the 30 day window or from an inactive mailbox.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recover deleted mailboxes
**Goal:** Restore a deleted mailbox within the 30 day window or from an inactive mailbox.

- Deleting the user soft-deletes the mailbox for 30 days.
- Restore the user in the admin center, or `Undo-SoftDeletedMailbox` into an existing mailbox.
- Inactive mailboxes (deleted while on hold) persist and can be recovered or restored with `New-MailboxRestoreRequest`.
- Confirm with `Get-Mailbox -SoftDeletedMailbox`.

## Gotchas
- Past 30 days without a hold, the mailbox is gone.
- Licence the restored mailbox to keep it.

## Self-check
Restored mailbox is visible in `Get-Mailbox` and its content opens.
