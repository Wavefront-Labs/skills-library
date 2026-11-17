---
id: computing-software.email-administration.mail-server-administration.lmtp-delivery-from-postfix
name: lmtp-delivery-from-postfix
category: computing-software
field: email-administration
product: mail-server-administration
tags: [lmtp-delivery-from-postfix, dovecot-lmtp-sieve, lmtp, dovecot-lmtp, virtual-transport-lmtp]
level: practitioner
status: docs-checked
description: "Deliver from Postfix to Dovecot over LMTP using a unix socket inside the Postfix queue directory."
sources:
  - https://doc.dovecot.org/main/howto/lmtp/postfix.html
  - https://www.postfix.org/postconf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lmtp delivery from postfix

**Goal:** one delivery path that also runs Sieve and quota.
## Steps
1. Dovecot (2.3-style syntax; in 2.4 the protocols are a `protocols { lmtp = yes }` block): `protocols = imap lmtp`; in `service lmtp` add `unix_listener /var/spool/postfix/private/dovecot-lmtp { mode = 0600  user = postfix  group = postfix }`.
2. Postfix: `virtual_transport = lmtp:unix:private/dovecot-lmtp`.
3. For non-virtual users use `mailbox_transport = lmtp:unix:private/dovecot-lmtp` instead of `virtual_transport`.
## Failure modes
- Socket path or permissions wrong: Postfix cannot connect to `private/dovecot-lmtp`; the socket must sit inside the Postfix spool (`/var/spool/postfix/private/`).
- Recipient accepted by Postfix but unknown to Dovecot: Dovecot answers `550 5.1.1 ... User doesn't exist`; keep the two user sources consistent.
## Verify
- Send a test message to a real user and confirm it arrives in the mailbox.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Dovecot docs 'Postfix and Dovecot LMTP' (doc.dovecot.org howto/lmtp/postfix, source repo), Dovecot LMTP delivery page, postconf(5) virtual_transport.
Confirmed: the `service lmtp` unix_listener under /var/spool/postfix/private with mode 0600 user/group postfix, `virtual_transport` and `mailbox_transport = lmtp:unix:private/dovecot-lmtp`, the 550 5.1.1 user-unknown reply, `protocols` lmtp.
Corrected or removed: `lmtp_save_to_detail_mailbox` (a Dovecot setting, not a Postfix one, and not tied to multiple domains), the unverified connect-failure and status=sent log strings.
Method: documentation only; no commands were run.
