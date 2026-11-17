---
id: computing-software.email-administration.dovecot.mailbox-format-selection-overview
name: mailbox-format-selection-overview
category: computing-software
field: email-administration
product: dovecot
tags: [mailbox-format, maildir, sdbox, mdbox, mbox, imapc]
level: intro
status: docs-checked
description: "Compare mbox, Maildir, sdbox, mdbox, imapc and pop3c storage, and separate the format choice from the physical storage decision."
sources:
  - https://doc.dovecot.org/main/core/config/mailbox_formats/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Mailbox formats define how mail data is stored, not where it physically lives; the admin decides that separately and chooses between local and shared storage.

The formats:
- mbox: INBOXes are commonly in /var/spool/mail or /var/mail. One file holds many messages.
- Maildir: one file per message, with `cur`, `new` and `tmp` subdirectories. Reliable because message files are never modified, so operations are atomic.
- dbox: Dovecot's own high-performance format. `sdbox` keeps one message per file; `mdbox` keeps several messages per file.- imapc and pop3c: use a remote IMAP or POP3 server as storage.

See the Mail Location Setting page for configuration.

Local storage advice: Dovecot does not rely on atime, so mount with `noatime`. Put index files on a separate disk from the mail spool, since indexes see heavy writes; the page recommends RAID-10 over RAID-5 for them.

Object storage is the recommended choice for large high-availability installations, but the `obox` format is provided by Dovecot Pro. Dovecot CE only supports mailbox access on a single server: a user can only be accessed by a single Dovecot server at a time.

## Checked
2026-11-09. Read the Dovecot Mailbox Formats overview (main documentation, marked pre-release) in full. Confirmed: the
format descriptions, local storage noatime and index-disk advice with RAID-10, object storage and obox, and the CE
single-server limit. Removed as unconfirmed: the `doveadm purge` requirement, the dbox performance comparison, and the
migration advice.
Method: documentation only; no commands were run.
