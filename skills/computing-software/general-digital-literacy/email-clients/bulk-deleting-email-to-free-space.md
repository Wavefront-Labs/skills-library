---
id: computing-software.general-digital-literacy.email-clients.bulk-deleting-email-to-free-space
name: bulk-deleting-email-to-free-space
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, filters, mailbox-full, bulk-delete-email, large-attachments, storage-cleanup]
level: intro
status: draft
description: "Free mailbox space fast in Gmail, Outlook and iCloud Mail by searching for large and old messages, selecting all matches and emptying trash."
sources:
  - https://support.google.com/mail
  - https://support.microsoft.com/en-us/outlook
  - https://support.apple.com/guide/icloud/welcome/icloud
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Bulk delete to free mailbox space

## Gmail (storage shared with Drive and Photos, 15 GB free)
1. Search `larger:10M` (or `has:attachment larger:5M older_than:2y`).
2. Tick the select-all box › **Select all conversations that match this search** › Delete.
3. Promotions/Social: click the tab › select all › *Select all conversations* › Delete.
4. **Empty Trash** and **Spam** (Trash › *Empty Trash now*); space frees within ~24 h.
5. Check what else uses space: one.google.com/storage › *Clean up space*.

## Outlook.com / Microsoft 365
- Search box › filters: *Has attachments*, date range; or sort the folder by **Size**.
- Outlook.com: Settings › General › **Storage** shows usage by folder; *Empty* folders there.
- Empty **Deleted Items** then **Recoverable Items** (right-click Deleted Items › *Recover items
  deleted from this folder* › purge) in Microsoft 365.
- Classic Outlook: File › Tools › **Mailbox Cleanup** › *Find items larger than*.

## iCloud Mail
icloud.com/mail › sort by size is not available; search `has attachment` in Mail app on Mac, sort
Mailbox by Size (View › Sort By › Size), delete, then Mailbox › Erase Deleted Items.

## Gotchas
- Save important attachments to cloud storage before deleting the email.
- Deleting from a phone app (IMAP) removes from the server too; with POP it may not.
- Outlook.com has a separate attachment storage counted from OneDrive in some plans.

## Verify
- [ ] Storage meter dropped after emptying Trash, and new mail arrives normally.
