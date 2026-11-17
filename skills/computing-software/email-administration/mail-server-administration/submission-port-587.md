---
id: computing-software.email-administration.mail-server-administration.submission-port-587
name: submission-port-587
category: computing-software
field: email-administration
product: mail-server-administration
tags: [submission-port-587, submission-relay, submission, port-587, msa, submission-service]
level: practitioner
status: draft
description: "Run an authenticated submission service on 587 (RFC 6409) separate from port 25 relay, with STARTTLS and SASL required."
sources:
  - https://www.rfc-editor.org/rfc/rfc6409
  - https://www.rfc-editor.org/rfc/rfc5321
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Submission port 587

**Goal:** users send via 587 with auth; port 25 only carries MTA-to-MTA traffic.
## Steps (Postfix master.cf)
```
submission inet n - y - - smtpd
  -o syslog_name=postfix/submission
  -o smtpd_tls_security_level=encrypt
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_tls_auth_only=yes
  -o smtpd_relay_restrictions=permit_sasl_authenticated,reject
```
Then `postfix reload`.
## Failure modes
- Missing certificate or key: the service fails to start; read the mail log.
- Leaving `permit_mynetworks` here lets any host in mynetworks relay without auth.
## Verify
- `openssl s_client -starttls smtp -connect mail.example.com:587`, then AUTH is advertised only after TLS.
- A message without credentials gets `554 5.7.1 Relay access denied`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
