---
id: computing-software.cryptography-implementation.protocol-implementation.dual-rsa-and-ecdsa-certificates
name: dual-rsa-and-ecdsa-certificates
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, tls-configuration, dual-certificates, ecdsa-certificate, rsa-certificate, signature-algorithms, handshake-performance, nginx, haproxy]
level: advanced
status: docs-checked
description: "Serve ECDSA and RSA certificates on one TLS endpoint: legacy client compatibility, nginx and Apache config, renewing both, and testing selection."
sources: ["https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://datatracker.ietf.org/doc/html/rfc8446"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dual RSA and ECDSA certificates

ECDSA server certificates are smaller and cheaper to sign with than RSA, but some
old or embedded clients accept only RSA. Serving both lets
each client get the best one it supports.

## How selection works

The client's `signature_algorithms` (and in TLS 1.2, cipher suites
`ECDHE-ECDSA-*` vs `ECDHE-RSA-*`) tell the server which certificate types it
can verify. OpenSSL-based servers choose ECDSA when supported, RSA otherwise.

## Config

```nginx
ssl_certificate     /etc/ssl/example.ecdsa.fullchain.pem;
ssl_certificate_key /etc/ssl/example.ecdsa.key;
ssl_certificate     /etc/ssl/example.rsa.fullchain.pem;
ssl_certificate_key /etc/ssl/example.rsa.key;
```

```apache
SSLCertificateFile    /etc/ssl/example.ecdsa.fullchain.pem
SSLCertificateKeyFile /etc/ssl/example.ecdsa.key
SSLCertificateFile    /etc/ssl/example.rsa.fullchain.pem
SSLCertificateKeyFile /etc/ssl/example.rsa.key
```

nginx supports this since 1.11.0 (the directive can be repeated to load certificates of different types, for example RSA and ECDSA).

The TLS 1.2 cipher list must include both `ECDHE-ECDSA-*` and `ECDHE-RSA-*`
suites or one certificate is never used.

## Issuance

Issue one certificate per key type with your ACME client. Two certificates means two renewals and two expiry monitors; automate and alert on each separately.

## When one certificate is enough

If logs show no clients negotiating `ECDHE-RSA-*`/RSA signatures for months
(and you have no embedded/legacy clients), drop RSA. Conversely, internal
services with only modern clients should be ECDSA-only.

## Verify

- [ ] ECDSA-capable client gets the ECDSA cert; RSA-only offer gets the RSA cert.
- [ ] Both certificates monitored for expiry and renewed automatically.

## Checked
2026-11-01. Confirmed against the nginx ssl module page: ssl_certificate may be specified multiple times (since 1.11.0) to load certificates of different types, for example RSA and ECDSA. Removed: 10-30x speed figure, HAProxy file-naming claim, s_client commands (not verified), certbot flags.
Method: documentation only; no commands were run.
