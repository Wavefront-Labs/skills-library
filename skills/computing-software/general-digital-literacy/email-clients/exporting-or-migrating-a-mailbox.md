---
id: computing-software.general-digital-literacy.email-clients.exporting-or-migrating-a-mailbox
name: exporting-or-migrating-a-mailbox
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-account-setup, export-mailbox, pst-export, mbox, import-email]
level: practitioner
status: draft
description: "Export a mailbox to PST or MBOX, move email between Gmail, Outlook and iCloud with import tools or IMAP, and keep an offline archive."
sources:
  - https://support.google.com/accounts
  - https://support.microsoft.com/en-us/outlook
  - https://support.google.com/mail
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Export or migrate a mailbox

## Export (archive or backup)
- **Gmail**: takeout.google.com › select *Mail* (all or chosen labels) › export → `.mbox` file(s).
  Open with Thunderbird (ImportExportTools NG add-on) or Apple Mail (File › Import Mailboxes).
- **Classic Outlook (Windows)**: File › Open & Export › **Import/Export › Export to a file › Outlook
  Data File (.pst)** › choose the account's top folder › include subfolders. New Outlook can't create
  PSTs; use classic Outlook.
- **Outlook.com**: Privacy dashboard › *Export your data* (mailbox), or via classic Outlook PST.
- **Apple Mail**: select mailbox › Mailbox › Export Mailbox (.mbox).

## Migrate to a new provider
- **Gmail ← Outlook/Yahoo/other**: Gmail Settings › Accounts and Import › **Import mail and contacts**
  (uses ShuttleCloud, runs ~30 days).
- **Outlook.com/Microsoft 365 ← Gmail**: Outlook web Settings › *Import* (where available) or classic
  Outlook with both accounts added via IMAP: drag folders from one to the other.
- **Any IMAP to IMAP**: add both accounts in Thunderbird or classic Outlook; copy folders across.
  Work accounts: IT uses migration tools.
- Contacts: export CSV/vCard and import; calendars: export .ics and import.

## Gotchas
- PST files above ~20 GB get slow; split by year.
- Drag-copy over IMAP is slow and can time out; do a year at a time.
- Gmail labels become folders (one copy per label) in mbox/IMAP exports.
- Keep the old account open (with forwarding) for a few months.

## Verify
- [ ] Message counts per folder roughly match source and destination; spot-check attachments open.
