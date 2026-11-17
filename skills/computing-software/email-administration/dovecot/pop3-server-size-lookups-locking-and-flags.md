---
id: computing-software.email-administration.dovecot.pop3-server-size-lookups-locking-and-flags
name: pop3-server-size-lookups-locking-and-flags
category: computing-software
field: email-administration
product: dovecot
tags: [pop3, pop3-fast-size-lookups, pop3-lock-session, pop3-no-flag-updates, uidl, maildir-w-size]
level: practitioner
status: docs-checked
description: "Tune POP3 on Dovecot: exact message sizes with Maildir, W= filenames, mailbox locking, flag updates, index use and UIDL stability."
sources:
  - https://doc.dovecot.org/main/core/config/pop3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dovecot is designed first as an IMAP server; POP3 works but is not optimized.

Sizes. POP3 requires exact sizes counted with CR+LF line endings, but Maildir stores plain LF, so the file size is wrong. Some servers report it anyway and violate the spec. Dovecot reads each message and counts correctly, then stores the virtual size in `dovecot-uidlist`. You can skip the first calculation by appending `,W=<size>` to the base filename of newly delivered mail only, for example `...host,W=2211:2,`. Never add it to existing files. With the Dovecot LDA, uidlist and indexes update on delivery, so there is no size cost. `pop3_fast_size_lookups = yes` uses virtual sizes when available but falls back to physical sizes, which breaks the specification like many servers do.

Indexes. If users delete mail after downloading, indexes churn: updated at session start to hold all messages and again when the mailbox goes empty. Try disabling indexes for POP3-only users, or keep them and adjust `mbox_min_index_size`. Do not disable indexes if users keep mail on the server, and indexes also help fast size access with the LDA.

Locking. Multiple connections to one mailbox are allowed by default, which helps dial-up clients whose dead connections would hold a lock. `pop3_lock_session = yes` locks for the whole session, as RFC 1939 says. A blocked connection waits until the lock times out: 2 minutes for Maildir, `mbox_lock_timeout` for mbox.

Flags. RETR adds \Seen by default; `pop3_no_flag_updates = yes` skips it for performance. `pop3_client_workarounds` handles broken clients. Keep UIDLs stable: a changed UIDL makes clients re-download everything as new.

## Checked

2026-11-03. Confirmed on the POP3 page: Dovecot is IMAP-first, exact CR+LF sizes and the virtual size cached in dovecot-uidlist, appending ,W=<size> to newly delivered Maildir filenames only (example ...host,W=2211:2,), LDA updating uidlist and indexes on delivery, pop3_fast_size_lookups, mbox index guidance and mbox_min_index_size, multiple connections by default, pop3_lock_session and the 2-minute Maildir lock timeout, \Seen on RETR, pop3_no_flag_updates, pop3_client_workarounds and the UIDL warning. Nothing removed.

Method: documentation only; no commands were run.
