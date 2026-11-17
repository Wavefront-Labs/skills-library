---
id: computing-software.email-administration.mail-server-administration.relay-vs-submission-policy
name: relay-vs-submission-policy
category: computing-software
field: email-administration
product: mail-server-administration
tags: [relay-vs-submission-policy, smtpd-relay-restrictions, relay-policy, permit-sasl-authenticated]
level: advanced
status: draft
description: "Decide who may relay: Postfix smtpd_relay_restrictions for port 25 versus authenticated submission, and keep outbound policy separate."
sources:
  - https://www.rfc-editor.org/rfc/rfc6409
  - https://www.rfc-editor.org/rfc/rfc5321
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Relay vs submission policy

**Goal:** one rule: relay only for authenticated users or trusted networks, nobody else.
## Steps
1. Port 25: `smtpd_relay_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination`.
2. Recipient checks after that: `smtpd_recipient_restrictions = reject_non_fqdn_recipient, reject_unknown_recipient_domain`.
3. Keep `mynetworks` to loopback and your own server subnets; avoid broad ranges.
4. Prefer separate master.cf services (25 vs 587) so each has its own `-o` overrides.
## Failure modes
- `reject_unauth_destination` missing from relay restrictions: open relay.
- Auth enabled on 25 invites credential stuffing against a service meant for MTAs.
## Verify
- From an outside host: `RCPT TO:<someone@example.net>` must get `554 5.7.1 Relay access denied`.
- `postconf smtpd_relay_restrictions` shows the final `reject_unauth_destination`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
