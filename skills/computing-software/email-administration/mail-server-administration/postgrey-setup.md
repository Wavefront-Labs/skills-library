---
id: computing-software.email-administration.mail-server-administration.postgrey-setup
name: postgrey-setup
category: computing-software
field: email-administration
product: mail-server-administration
tags: [postgrey-setup, greylisting, postgrey, greylisting-setup]
level: practitioner
status: draft
description: "Set up Postgrey as a Postfix policy service and tune delay, auto-whitelist and client allowlists."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Postgrey setup

**Goal:** temporarily reject first-time (client, sender, recipient) triplets so real MTAs retry and bots do not.
## Steps
1. Install Postgrey; run it on a unix socket, e.g. `--unix=/var/spool/postfix/postgrey/socket --delay=300`.
2. Add `check_policy_service unix:postgrey/socket` to `smtpd_recipient_restrictions` after `reject_unauth_destination`.
3. Maintain `postgrey_whitelist_clients.local` for partners who cannot retry.
4. `postfix reload`.
## Failure modes
- Delayed one-time passwords or verification emails; whitelist those senders.
- Large senders retry from different IPs, so the triplet never matches (Postgrey matches on a client subnet to mitigate; check its README).
## Verify
- Log: `action=greylist, reason=new` first, then `action=pass, reason=triplet found` on retry after the delay.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
