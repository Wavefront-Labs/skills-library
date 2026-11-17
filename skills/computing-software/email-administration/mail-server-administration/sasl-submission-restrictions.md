---
id: computing-software.email-administration.mail-server-administration.sasl-submission-restrictions
name: sasl-submission-restrictions
category: computing-software
field: email-administration
product: mail-server-administration
tags: [sasl-submission-restrictions, smtpd-tls-auth-only, smtpd-sender-login-maps, sasl-security-options]
level: advanced
status: draft
description: "Restrict SASL: smtpd_tls_auth_only, smtpd_sasl_security_options, and mapping authenticated users to allowed sender addresses."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sasl submission restrictions

**Goal:** safe auth only over TLS, and users cannot forge other senders.
## Steps
1. `smtpd_tls_auth_only = yes` (on submission).
2. `smtpd_sasl_security_options = noanonymous`.
3. `smtpd_sender_login_maps = hash:/etc/postfix/sender_login` with lines `alice@example.com  alice`.
4. In submission restrictions add `reject_sender_login_mismatch`.
## Failure modes
- Without login maps, any authenticated user can send as any address in your domain.
- Brute-force attempts: rate-limit and ban (see fail2ban-for-mail).
## Verify
- Authenticate as alice and try `MAIL FROM:<bob@example.com>`: expect a 553 5.7.1 sender mismatch.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
