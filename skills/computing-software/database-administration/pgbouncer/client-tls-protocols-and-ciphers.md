---
id: computing-software.database-administration.pgbouncer.client-tls-protocols-and-ciphers
name: client-tls-protocols-and-ciphers
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, tls, ciphers, protocols, tls13]
level: advanced
status: docs-checked
description: "client_tls_protocols, client_tls_ciphers, client_tls13_ciphers, client_tls_ecdhcurve and client_tls_dheparams with allowed values."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune which TLS versions and ciphers clients may use.

- `client_tls_protocols` (default `secure`): allowed values tlsv1.0, tlsv1.1, tlsv1.2, tlsv1.3. Shortcuts: `all` (tlsv1.0, tlsv1.1, tlsv1.2, tlsv1.3) and `secure` (tlsv1.2, tlsv1.3).
- `client_tls_ciphers` (default `default`): OpenSSL syntax. Shortcuts default, secure, fast and normal all use system-wide OpenSSL defaults; `all` enables all ciphers and is not recommended. Affects only TLS 1.2 and lower.
- `client_tls13_ciphers` (default empty): TLS 1.3 ciphers. When empty it uses the value of client_tls_ciphers. Allowed: TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256, TLS_AES_128_GCM_SHA256, TLS_AES_128_CCM_8_SHA256, TLS_AES_128_CCM_SHA256. Affects only TLS 1.3 and higher.
- `client_tls_ecdhcurve` (default `auto`): curve for ECDH key exchange. Values: `none` (DH disabled), `auto` (256-bit ECDH) or a curve name.
- `client_tls_dheparams` (default `auto`): DHE key exchange type. Values: `none` (DH disabled), `auto` (2048-bit DH), `legacy` (1024-bit DH).

```
client_tls_protocols = tlsv1.3
client_tls13_ciphers = TLS_AES_256_GCM_SHA384
```

Any change to TLS settings triggers an automatic RECONNECT for security reasons.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: a closing sentence about PEM paths and a cross-reference.

Method: documentation only; no commands were run.
