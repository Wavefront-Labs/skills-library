---
id: computing-software.email-administration.mail-server-administration.smtpd-tls-server
name: smtpd-tls-server
category: computing-software
field: email-administration
product: mail-server-administration
tags: [smtpd-tls-server, postfix-tls, smtpd-tls-security-level, smtpd-tls-cert-file, starttls]
level: practitioner
status: draft
description: "Enable opportunistic STARTTLS on inbound SMTP with a certificate chain and key, and verify with openssl."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smtpd tls server

**Goal:** encrypt inbound sessions (TLS_README).
## Steps
1. `smtpd_tls_chain_files = /etc/ssl/mail/privkey.pem, /etc/ssl/mail/fullchain.pem` (private key first), or the older `smtpd_tls_cert_file` / `smtpd_tls_key_file` pair.
2. Port 25: `smtpd_tls_security_level = may` (do not force encryption for MTA traffic).
3. `smtpd_tls_loglevel = 1` to log the protocol and cipher.
4. `postfix reload` after each certificate renewal (use a renewal hook).
## Failure modes
- Expired certificate: encrypted-only partners (MTA-STS, DANE) will refuse to deliver.
- Incomplete chain: some senders log verification failures.
## Verify
- `openssl s_client -starttls smtp -connect mail.example.com:25 -servername mail.example.com` shows the chain and "Verify return code".
- Log shows `TLS established from ...`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
