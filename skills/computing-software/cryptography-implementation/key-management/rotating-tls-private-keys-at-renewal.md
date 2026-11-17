---
id: computing-software.cryptography-implementation.key-management.rotating-tls-private-keys-at-renewal
name: rotating-tls-private-keys-at-renewal
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, tls-key-rotation, certificate-renewal, acme, private-key, key-reuse]
level: practitioner
status: draft
description: "Generate a fresh TLS private key at each certificate renewal: ACME client settings, reuse pitfalls with pinning and DANE, and reloading servers without downtime."
sources: ["https://eff-certbot.readthedocs.io/en/stable/using.html#reusing-private-keys", "https://cert-manager.io/docs/usage/certificate/#configuring-private-key-rotation", "https://www.rfc-editor.org/rfc/rfc7671"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rotating TLS private keys at renewal

Renewing a certificate with the same key extends the exposure of that key indefinitely. Rotate the key with every
renewal unless something depends on it.

## Client settings
- certbot: new key by default; `--reuse-key` keeps it (avoid unless pinned). `--new-key` forces rotation once.
- cert-manager: `spec.privateKey.rotationPolicy: Always` (default since v1.18; older default `Never`).
- acme.sh: new key unless `--always-force-new-domain-key` is absent and key exists; check `--keylength` usage.
- Caddy, Traefik: rotate automatically.

## Things that break on key change
- HPKP-style pins in mobile apps: pin the CA or SPKI of a backup key, and ship the next key's pin first.
- DANE TLSA `3 1 1` records (SPKI hash): publish the new key's TLSA record before rollover (RFC 7671 8.1).
- Mutual TLS peers that pin the server key.
- Load balancers holding a copy of the key: push the new key everywhere.

## Reload without downtime
- nginx: `nginx -s reload`; HAProxy: runtime API `set ssl cert` + `commit ssl cert`; Apache: `apachectl graceful`.
- Go: `tls.Config.GetCertificate` reading the latest pair.

## Verify
- [ ] Compare SPKI hash before and after renewal:
  `openssl x509 -in cert.pem -pubkey -noout | openssl pkey -pubin -outform der | sha256sum`.
