---
id: computing-software.email-administration.dovecot.ssl-key-password-chain-and-client-certificates
name: ssl-key-password-chain-and-client-certificates
category: computing-software
field: email-administration
product: dovecot
tags: [ssl-server-key-password, ssl-server-ca-file, client-certificate, certificate-chain, dh-parameters, auth-ssl-require-client-cert]
level: advanced
status: docs-checked
description: "Protect the TLS key with a password, order a certificate chain, require client certificates with CRLs and limit the requirement to one protocol."
sources:
  - https://doc.dovecot.org/main/core/config/ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Key password. SSL key files can be password protected. `dovecot -p` asks for it at start, which prevents automatic boot. Alternatively set `ssl_server_key_password`. Because `dovecot.conf` is world-readable by default, keep it in a separate file such as `/etc/dovecot-private.conf` and pull it in with `!include_try`.

Certificate chain. Put all certificates in `ssl_server_cert_file` in the required order; most CAs supply a full-chain file that already has it. Use that.

DH parameters are optional and most modern clients do not need them. Generating a new file can take a very long time.

Ciphers. The default allowed list is already sensible. Disallowing more does not strengthen connections that use better ciphers, but it prevents accidental weak use. For TLS 1.3 the page sets `ssl_server_prefer_ciphers = client`.

To log every problem seen on TLS connections, set `log_debug = category=ssl`, noting that dropped connections make it noisy.

Client certificates. Require them with `ssl_server_ca_file`, `ssl_server_request_client_cert = yes` and `auth_ssl_require_client_cert = yes`. The CA file holds certificates followed by the matching CRLs, and the CRLs must exist; for a multi-level CA the order is issuing CA cert and CRL, intermediate CA cert and CRL, then root CA cert and CRL. Both must be PEM; convert a DER CRL with `openssl crl -inform DER -outform PEM`. A client without a valid certificate cannot log in.

This breaks MTA SASL use if the MTA presents no certificate. To serve IMAP with client certificates and SASL for an MTA without, put `auth_ssl_require_client_cert = yes` inside a `protocol !smtp` block, which exempts the SMTP SASL client.

## Checked

2026-11-03. Confirmed on the SSL/TLS Configuration page: dovecot -p versus ssl_server_key_password kept in a file pulled in with !include_try, certificate chain order and full-chain files, optional DH parameters, the default cipher list note and ssl_server_prefer_ciphers = client for TLS 1.3, log_debug = category=ssl, client certificate verification (CA file with CRLs, PEM, multi-level order, openssl crl DER to PEM, protocol !smtp exemption). Fixed: named the full set of client-certificate settings, the exact exemption block, and the log_debug setting; dropped the SNI howto from sources (page returned no text).

Method: documentation only; no commands were run.
