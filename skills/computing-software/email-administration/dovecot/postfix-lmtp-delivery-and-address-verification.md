---
id: computing-software.email-administration.dovecot.postfix-lmtp-delivery-and-address-verification
name: postfix-lmtp-delivery-and-address-verification
category: computing-software
field: email-administration
product: dovecot
tags: [postfix, lmtp-socket, virtual-transport, reject-unverified-recipient, dynamic-address-verification]
level: practitioner
status: docs-checked
description: "Wire Postfix to Dovecot LMTP over a socket inside the Postfix spool, and use reject_unverified_recipient for dynamic address checks."
sources:
  - https://doc.dovecot.org/main/howto/lmtp/postfix.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
First enable `lmtp` in dovecot.conf. LMTP can bind to INET or Unix sockets. In the example a Unix socket is placed inside the Postfix spool with appropriate permissions, because Postfix access is limited to that directory. Enable quota and Sieve in `mail_plugins` of the `protocol lmtp` block, which also needs `postmaster_address` (marked REQUIRED).

The last step is telling Postfix to use the socket for final delivery. Set `virtual_transport = lmtp:unix:private/dovecot-lmtp` for virtual users, or `mailbox_transport` with the same value otherwise; the path is relative to the Postfix spool.

Dynamic address verification. Postfix can use LMTP with `reject_unverified_recipient` in `smtpd_recipient_restrictions`, so it does not need an external data source such as MySQL or LDAP. Postfix keeps a local database of existing and nonexistent addresses, and you can configure how long entries live. Get Dovecot delivering first, then enable this.

On each incoming mail Postfix probes the recipient. For a missing user the log shows a rejection such as `550 5.1.1 User doesn't exist` from the lmtp socket; an existing recipient reports deliverable and the mail is accepted.

Limitation: `reject_unverified_recipient` cannot be used with `pipe`, so it does not work with the Dovecot LDA `deliver` transport. That is one more reason to prefer LMTP.

## Checked

2026-11-03. Confirmed on the Postfix and Dovecot LMTP page: protocols with lmtp, the Unix socket inside the Postfix spool, plugins at protocol level (quota, sieve) with required postmaster_address, virtual_transport versus mailbox_transport with lmtp:unix:private/dovecot-lmtp, reject_unverified_recipient in smtpd_recipient_restrictions with the local result database, the 550 5.1.1 rejection log, and the pipe/LDA limitation. Made the transport settings explicit.

Method: documentation only; no commands were run.
