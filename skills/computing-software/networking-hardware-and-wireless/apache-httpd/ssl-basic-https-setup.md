---
id: computing-software.networking-hardware-and-wireless.apache-httpd.ssl-basic-https-setup
name: ssl-basic-https-setup
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, tls, mod-ssl, https, certificates, sslengine, virtualhost]
level: intro
status: docs-checked
description: "Enable HTTPS with mod_ssl: LoadModule, Listen 443, SSLEngine, certificate and key files, intermediates in the cert file, and how certificates and CAs work."
sources:
  - https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html
  - https://httpd.apache.org/docs/2.4/mod/mod_ssl.html
  - https://httpd.apache.org/docs/2.4/ssl/ssl_intro.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic HTTPS setup with mod_ssl
```apache
LoadModule ssl_module modules/mod_ssl.so
Listen 443
<VirtualHost *:443>
    ServerName www.example.com
    SSLEngine on
    SSLCertificateFile "/path/to/www.example.com.cert"
    SSLCertificateKeyFile "/path/to/www.example.com.key"
</VirtualHost>
```
`SSLEngine` is off by default.

## Files
- `SSLCertificateFile`: PEM certificate (or PKCS#11 URI). Since 2.4.8 it can also hold intermediates, leaf to root.
- `SSLCertificateKeyFile`: PEM key; each key needs a matching certificate directive. Keep the key in a separate file readable only by root.
- `SSLCertificateChainFile` became obsolete in 2.4.8.
- Files are read at startup before privileges drop, so changes need a restart.
- `SSLPassPhraseDialog` handles encrypted keys: `builtin` (default) prompts, `exec:/path/to/program` is called per encrypted key and prints the passphrase to stdout.

## Concepts
A certificate binds a public key to a distinguished name (CN, O, OU, L, ST, C) and is signed by a CA. PEM is the Base64 form between begin and end delimiter lines such as `-----BEGIN CERTIFICATE-----`. A CA can issue certificates for other CAs; the chain ends at a self-signed root. Browsers are preconfigured to trust well-known CAs; loading another CA certificate makes the browser accept every certificate that CA signed.

## Enforcing
`SSLRequireSSL` denies access unless the connection is encrypted. Without `SSLOptions +StrictRequire`, other authorization directives such as `<RequireAny>` can override the denial; with it the denial is enforced.

## Checked
2026-11-04. Confirmed against the mod_ssl reference, SSL how-to and SSL introduction: LoadModule, Listen 443 and VirtualHost example, SSLEngine default off, SSLCertificateFile intermediates (2.4.8), key and certificate pairing, separate key file advice, startup-only reads, SSLPassPhraseDialog, DN fields, PEM, self-signed roots, StrictRequire. Corrected SSLCertificateChainFile (obsolete, not deprecated). Removed the claim that the server sends its issuers to clients.
Method: documentation only; no commands were run.
