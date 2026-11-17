---
id: computing-software.email-administration.mail-server-administration.smtps-465-implicit-tls
name: smtps-465-implicit-tls
category: computing-software
field: email-administration
product: mail-server-administration
tags: [smtps-465-implicit-tls, smtps, port-465, implicit-tls, submissions]
level: practitioner
status: draft
description: "Enable the implicit-TLS submissions service on port 465 in Postfix alongside 587."
sources:
  - https://www.rfc-editor.org/rfc/rfc6409
  - https://www.rfc-editor.org/rfc/rfc5321
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smtps 465 implicit tls

**Goal:** support clients that expect TLS from the first byte (port 465).
## Steps
```
submissions inet n - y - - smtpd
  -o syslog_name=postfix/submissions
  -o smtpd_tls_wrappermode=yes
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_relay_restrictions=permit_sasl_authenticated,reject
```
1. Open TCP 465 in the firewall.
2. `postfix reload` and watch the log for the `postfix/submissions` tag.
## Failure modes
- Forgetting `smtpd_tls_wrappermode=yes`: clients hang waiting for a banner.
- Older Postfix may not know the `submissions` service name; use `smtps` with the same options (unconfirmed which release added it).
## Verify
- `openssl s_client -connect mail.example.com:465` shows the certificate then a 220 banner.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
