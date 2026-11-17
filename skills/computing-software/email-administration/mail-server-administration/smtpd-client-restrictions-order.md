---
id: computing-software.email-administration.mail-server-administration.smtpd-client-restrictions-order
name: smtpd-client-restrictions-order
category: computing-software
field: email-administration
product: mail-server-administration
tags: [smtpd-client-restrictions-order, smtpd-client-restrictions, smtpd-helo-restrictions, smtpd-sender-restrictions, smtpd-delay-reject]
level: advanced
status: draft
description: "Use smtpd_client, helo, sender and data restrictions in the right stage order and understand smtpd_delay_reject."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smtpd client restrictions order

**Goal:** apply each check at the stage it belongs to.
## Stages (in order)
client (connect) -> helo -> sender (MAIL FROM) -> relay -> recipient -> data.
## Steps
1. `smtpd_helo_required = yes`
2. `smtpd_helo_restrictions = permit_mynetworks, reject_invalid_helo_hostname, reject_non_fqdn_helo_hostname`
3. `smtpd_sender_restrictions = reject_non_fqdn_sender, reject_unknown_sender_domain`
4. Leave `smtpd_delay_reject = yes` so every reject is logged with full context.
## Failure modes
- Strict `reject_unknown_helo_hostname` rejects legitimate misconfigured senders; use sparingly.
- `reject_unknown_sender_domain` returns 450 on DNS failure, which defers rather than blocks.
## Verify
- Replay a connection with an invalid HELO and read the exact reject line in the log.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
