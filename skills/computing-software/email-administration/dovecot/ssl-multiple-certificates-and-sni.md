---
id: computing-software.email-administration.dovecot.ssl-multiple-certificates-and-sni
name: ssl-multiple-certificates-and-sni
category: computing-software
field: email-administration
product: dovecot
tags: [sni, local-name, multiple-certificates, ecdsa-migration, wildcard-certificate, ssl-server]
level: advanced
status: docs-checked
description: "Serve several TLS certificates by IP or by SNI local_name filter, keep a fallback default, and handle wildcard ordering."
sources:
  - https://doc.dovecot.org/main/core/config/ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A second certificate can be offered for a different key algorithm, which helps when migrating to ECDSA. Dovecot picks the alternative if the client's algorithm differs from the primary.

Per IP or per protocol: with several IPs available this is guaranteed to work with every client. You can use a hostname instead of an IP, which gets resolved. You still need a top-level default `ssl_server_key_file` and `ssl_server_cert_file`, or you get errors.

With SNI, the client names the host it wants and you select certificates with the `local_name` filter. Caveats:
- Multiple certificates on one IP do not work with all clients, mobile ones in particular; this is a TLS SNI limitation, not a Dovecot one. The page lists clients confirmed working (Thunderbird on Linux, K-9 on Android, Apple Mail, Mutt, NeoMutt) and clients that do not (Apple Mail on Mac OS X 10.10 and lower or iOS 9.3 and lower, Outlook for Mac 15, Kindle Fire HD 8, Outlook 2013).
- A wildcard `*` covers only a single label: `*.example.org` matches `mail.example.org` but not `int.mail.example.org`.
- Ordering matters. List the wildcard filter first and more specific names afterward, because the last matching `local_name` filter wins.

Since 2.4.0 SNI can reload other settings along with the certificate, for example `login_greeting` or `postmaster_address`. This works for IMAP, SMTP and LMTP.

Keep the top-level default certificate and key, and test with each target client before relying on SNI.

## Checked

2026-11-03. Confirmed on the SSL/TLS Configuration page (Multiple SSL Certificates): ssl_server_alt_cert_file for a different algorithm (ECDSA migration), per-IP/protocol blocks that always work and may use a hostname, the required top-level default key and certificate, local_name SNI filters, the single-label wildcard rule (*.example.org versus int.mail.example.org), wildcard-first ordering with the last matching filter winning, and SNI reloading of other settings since 2.4.0 for IMAP, SMTP and LMTP. Fixed: the client list was wrong (older Apple Mail is listed as not working); removed the unconfirmed non-SNI-client advice.

Method: documentation only; no commands were run.
