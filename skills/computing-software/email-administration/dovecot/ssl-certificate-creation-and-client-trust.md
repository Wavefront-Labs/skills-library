---
id: computing-software.email-administration.dovecot.ssl-certificate-creation-and-client-trust
name: ssl-certificate-creation-and-client-trust
category: computing-software
field: email-administration
product: dovecot
tags: [self-signed, mkcert, lets-encrypt, private-ca, certificate-import, openssl]
level: intro
status: docs-checked
description: "Create or obtain a certificate for Dovecot, understand the self-signed risk, and import a CA or certificate into clients."
sources:
  - https://doc.dovecot.org/main/howto/ssl/cert_create.html
  - https://doc.dovecot.org/main/howto/ssl/cert_import.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Self-signed certificates are the easiest start but weaken security. On first connect the client asks the user to trust the certificate, and users rarely check the fingerprint, so a man-in-the-middle can slip in. Later connections are safe only if the client stored the certificate; some do, others need manual setup. The fully safe route is to import the certificate into the client or operating system trust store before the first connection.

Dovecot ships `mkcert.sh`, which builds a self-signed certificate with OpenSSL using `dovecot-openssl.cnf`. Edit the config first; the CN must be the server host name. By default the certificate goes to `/etc/ssl/certs/dovecot.pem`, the key to `/etc/ssl/private/dovecot.pem`, and it expires in 365 days. Binary packages often run this at install time.

The correct approach is a CA-signed certificate, with three options:
- Buy one from an external CA that clients already trust.
- Use a free automated CA such as Let's Encrypt, which requires proving domain control.
- Run your own CA and install its certificate on every client.

When importing, you may import either the server certificate or the CA certificate. Steps differ per client:
- Apple Mail uses the OS X keychain; add the certificate to the X509 Anchors keychain.
- Thunderbird style clients use their certificate manager under Authorities.
- For pine, find `openssl version -d`, hash the certificate with `openssl x509 -in cert.pem -hash -noout`, and copy it to `$OPENSSLDIR/certs/$hash.0`. This probably works only for self-signed certificates.

## Checked

2026-11-03. Confirmed on the SSL Certificate Creation and Importing pages: self-signed trust-on-first-use weakness, importing before first connection, mkcert.sh with dovecot-openssl.cnf, CN matching the host name, default paths /etc/ssl/certs/dovecot.pem and /etc/ssl/private/dovecot.pem and 365-day expiry, the three CA options, Let's Encrypt domain proof, import of either the server or CA certificate, Thunderbird Authorities, and the pine hash procedure. Fixed: Apple Mail step now matches the page (add to the X509 Anchors keychain; no "trust for email" claim) and the pine openssl command is given in full.

Method: documentation only; no commands were run.
