---
id: computing-software.email-administration.mail-server-administration.smtpd-recipient-restrictions
name: smtpd-recipient-restrictions
category: computing-software
field: email-administration
product: mail-server-administration
tags: [smtpd-recipient-restrictions, postfix-access-control, restriction-classes]
level: advanced
status: draft
description: "Order smtpd_recipient_restrictions correctly: permit rules, reject_unauth_destination and policy checks, per SMTPD_ACCESS_README."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smtpd recipient restrictions

**Goal:** a restriction list that evaluates top down and ends with an explicit decision.
## Example
```
smtpd_recipient_restrictions =
  permit_mynetworks,
  permit_sasl_authenticated,
  reject_unauth_destination,
  reject_unknown_recipient_domain,
  reject_non_fqdn_recipient
```
## Rules
- The first matching rule wins; later rules are never evaluated.
- Since Postfix 2.10, `smtpd_relay_restrictions` handles relaying and recipient restrictions handle the rest.
- With `smtpd_delay_reject = yes` (default), checks run at RCPT time so rejects are logged with sender and recipient.
## Failure modes
- A `permit` placed above `reject_unauth_destination` that matches too much: open relay.
## Verify
- `postconf smtpd_recipient_restrictions`; test accepted and rejected cases by hand.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
