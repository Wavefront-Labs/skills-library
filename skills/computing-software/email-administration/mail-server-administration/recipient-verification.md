---
id: computing-software.email-administration.mail-server-administration.recipient-verification
name: recipient-verification
category: computing-software
field: email-administration
product: mail-server-administration
tags: [recipient-verification, local-recipient-maps, reject-unverified-recipient, backscatter]
level: practitioner
status: draft
description: "Reject unknown recipients at SMTP time with local_recipient_maps and reject_unverified_recipient to prevent backscatter."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recipient verification

**Goal:** never accept what you cannot deliver.
## Steps
1. Local users: `local_recipient_maps` (default derived from passwd and aliases) rejects unknown users.
2. For relay-domain backends: `smtpd_reject_unlisted_recipient = yes` and `reject_unverified_recipient` with `address_verify_map` caching.
3. Virtual domains: ensure the map lists every valid recipient.
## Failure modes
- Verify probes fail if the backend is down: set `unverified_recipient_defer_code`.
## Verify
- RCPT to a nonexistent address gets `550 5.1.1 ... User unknown` at SMTP time.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
