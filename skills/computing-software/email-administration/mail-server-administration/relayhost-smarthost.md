---
id: computing-software.email-administration.mail-server-administration.relayhost-smarthost
name: relayhost-smarthost
category: computing-software
field: email-administration
product: mail-server-administration
tags: [relayhost-smarthost, smarthost-relay, relayhost, smtp-sasl-password-maps, smarthost]
level: practitioner
status: draft
description: "Send outbound mail via a smarthost with relayhost, SASL client authentication and TLS, when port 25 egress is blocked."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Relayhost smarthost

**Goal:** relay through a provider you trust.
## Steps
1. `relayhost = [smtp.relay.example.net]:587`
2. `smtp_sasl_auth_enable = yes`, `smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd`, `smtp_sasl_security_options = noanonymous`.
3. `smtp_tls_security_level = encrypt`.
4. Table: `[smtp.relay.example.net]:587  user:password`; `chmod 600`, `postmap` it.
## Failure modes
- Table key without brackets or port not matching `relayhost`: no credentials sent.
- Missing SASL client libraries.
## Verify
- Log shows `relay=smtp.relay.example.net[...]:587 ... status=sent`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
