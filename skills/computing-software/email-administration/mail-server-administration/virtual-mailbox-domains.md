---
id: computing-software.email-administration.mail-server-administration.virtual-mailbox-domains
name: virtual-mailbox-domains
category: computing-software
field: email-administration
product: mail-server-administration
tags: [virtual-mailbox-domains, virtual-mailbox-maps, virtual-transport]
level: practitioner
status: draft
description: "Host real mailboxes for virtual domains with virtual_mailbox_domains, virtual_mailbox_maps and delivery via LMTP to Dovecot."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Virtual mailbox domains

**Goal:** non-system-user mailboxes for domains you host.
## Steps
1. `virtual_mailbox_domains = example.com`
2. `virtual_mailbox_maps = hash:/etc/postfix/vmailbox` with lines like `alice@example.com  example.com/alice/`.
3. Deliver through Dovecot: `virtual_transport = lmtp:unix:private/dovecot-lmtp`.
4. `postmap /etc/postfix/vmailbox && postfix reload`.
## Failure modes
- Unknown recipient accepted then bounced: ensure `virtual_mailbox_maps` is consulted so Postfix rejects at RCPT time.
- LMTP socket missing: configure the Dovecot `service lmtp` listener inside Postfix's queue directory.
## Verify
- `postmap -q alice@example.com hash:/etc/postfix/vmailbox` returns a path.
- `swaks --to alice@example.com --server 127.0.0.1` ends with a log line `status=sent (delivered via ...)`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
