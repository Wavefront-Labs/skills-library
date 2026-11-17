---
id: computing-software.email-administration.dovecot.mbox-dirty-sync-and-lazy-writes
name: mbox-dirty-sync-and-lazy-writes
category: computing-software
field: email-administration
product: dovecot
tags: [mbox, mbox-dirty-syncs, mbox-lazy-writes, x-uid-header, full-sync, mbox-format]
level: advanced
status: docs-checked
description: "How mbox_dirty_syncs avoids rereading large mbox files, what dirty mode is, and the X-UID verification fallback."
sources:
  - https://doc.dovecot.org/main/core/config/mailbox_formats/mbox.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Large mbox files take long to resync after an unexpected change. Because the change is usually new mail appended by the LDA, Dovecot can read only the new messages first and fall back to a full read if something else is off.

Without `mbox_dirty_syncs`, any change makes Dovecot reread the whole file. With it, Dovecot assumes external changes are appends, with safeguards so this is safe even for other changes. On a timestamp or size change it checks the size:
- If the size is unchanged, only flags probably changed, so it does a full read to find them.
- If the file shrank, mails were expunged, so it does a full sync.
- If it grew, it checks that the last known message is still where expected. If so, it reads only the added messages and enters dirty mode.

In dirty mode Dovecot cannot be sure mails are where it believes. When a mail is accessed it first verifies it by finding its `X-UID` header; a mismatch triggers a full sync to find the right position. Dirty mode ends after the full sync.

If `mbox_lazy_writes` is enabled and a message has no `X-UID` header yet, Dovecot identifies it by an MD5 of a couple of headers.

The downside is that external message flag modifications may not be visible immediately.

## Checked
2026-11-09. Read the Dovecot Mbox Mailbox Format page (main documentation, marked deprecated for production) and its
`mbox_dirty_syncs` and `mbox_lazy_writes` setting entries. Confirmed the sync decision steps, dirty mode, the X-UID
check and the MD5 fallback. Removed as unconfirmed: the advice to use these settings only when Dovecot and the LDA
touch the mbox.
Method: documentation only; no commands were run.
