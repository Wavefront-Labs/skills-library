---
id: computing-software.email-administration.mail-server-administration.tls-cipher-protocol-selection
name: tls-cipher-protocol-selection
category: computing-software
field: email-administration
product: mail-server-administration
tags: [tls-cipher-protocol-selection, smtpd-tls-protocols, tls-cipher-list, tls-1-2]
level: advanced
status: draft
description: "Pick minimum TLS protocol and cipher lists in Postfix (smtpd_tls_mandatory_protocols, tls_high_cipherlist) without breaking MTAs."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tls cipher protocol selection

**Goal:** disable obsolete TLS while staying interoperable.
## Steps
1. Mandatory (submission): `smtpd_tls_mandatory_protocols = >=TLSv1.2` (the `>=` form needs a recent Postfix; otherwise `!SSLv2, !SSLv3, !TLSv1, !TLSv1.1`).
2. Opportunistic port 25: `smtpd_tls_protocols = >=TLSv1` is a common compromise; do not lower the bar for MTA mode without a reason.
3. Leave ciphers at defaults unless a scanner demands otherwise; defaults are maintained by the Postfix project.
4. Review with `postconf -d smtpd_tls_mandatory_ciphers`.
## Failure modes
- Over-tight lists make older but legitimate senders fall back to plaintext or fail.
## Verify
- `openssl s_client -starttls smtp -connect mail.example.com:587 -tls1_2` succeeds; with `-tls1_1` it fails.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
