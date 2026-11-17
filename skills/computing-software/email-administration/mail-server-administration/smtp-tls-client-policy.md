---
id: computing-software.email-administration.mail-server-administration.smtp-tls-client-policy
name: smtp-tls-client-policy
category: computing-software
field: email-administration
product: mail-server-administration
tags: [smtp-tls-client-policy, smtp-tls-security-level, smtp-tls-policy-maps, tls-policy-map]
level: advanced
status: draft
description: "Set outbound TLS policy: smtp_tls_security_level, per-destination smtp_tls_policy_maps (may, encrypt, verify, secure) and logging."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smtp tls client policy

**Goal:** encrypt outbound mail and enforce stricter policy for chosen partners.
## Steps
1. `smtp_tls_security_level = may` and `smtp_tls_loglevel = 1`.
2. `smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt` (path varies by distro).
3. Per destination: `smtp_tls_policy_maps = hash:/etc/postfix/tls_policy` with `example.net  secure match=mx.example.net` or `encrypt`.
4. `postmap` the table and reload.
## Failure modes
- `encrypt` or `verify` to a partner with a broken cert defers all mail to them.
- `smtp_tls_security_level = dane` needs a validating resolver (see dane-tlsa-records).
## Verify
- Log shows `Trusted TLS connection established` or `Untrusted`/`Verified`, per policy.
- `postqueue -p` shows no growing queue for that domain.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
