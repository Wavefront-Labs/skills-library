---
id: computing-software.cryptography-implementation.protocol-implementation.certificate-path-building-and-cross-signs
name: certificate-path-building-and-cross-signs
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, certificate-validation, path-validation, path-building, cross-signed-roots, rfc4158, aia-chasing, expired-root, x509]
level: sme
status: docs-checked
description: "Understand how clients build certificate paths with cross-signed and expiring roots (RFC 4158 vs RFC 5280), why some libraries fail, and how to choose chains that work."
sources: ["https://datatracker.ietf.org/doc/html/rfc5280#section-6", "https://datatracker.ietf.org/doc/html/rfc4158", "https://letsencrypt.org/docs/dst-root-ca-x3-expiration-september-2021/", "https://scotthelme.co.uk/lets-encrypt-old-root-expiration/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Certificate path building and cross-signs

RFC 5280 section 6 defines how to **validate** a given path. Finding the path
(RFC 4158 path building) is left to implementations, and they differ. With
cross-signed intermediates there can be several valid paths to different
roots, some expired, and naive clients pick the wrong one.

## The classic failure: September 2021

Let's Encrypt's chain was leaf -> R3 -> ISRG Root X1 (cross-signed by
DST Root CA X3). When DST Root CA X3 expired, clients that follow the
served chain to the expired root and do not try alternatives failed, even if
they trusted ISRG Root X1 directly. Let's Encrypt told API and IoT operators
that every client must trust ISRG Root X1 (not just DST Root CA X3) and that
OpenSSL clients must be 1.1.0 or later, because OpenSSL 1.0.x has a
verification quirk here. Older Android devices kept working through a special
cross-sign that outlived DST Root CA X3 (Android only). Scott Helme's write-up
adds that OpenSSL 1.0.2 or earlier is affected and that `--trusted_first`
helps when using `openssl verify` or `s_client`.

## How implementations behave

Path-building ability varies by stack and version (older OpenSSL, some Java and embedded stacks are the
usual casualties). Look up each stack's documentation and test it; do not assume.

## What to do

- Server side: serve the chain that leads to the root your oldest important
  clients trust, without extra cross-signed certificates unless needed. Test
  with those clients (see interop matrix skill).
- Client side: keep libraries current; enable trusted-first where available;
  update the trust store (old devices with stale stores are the real long tail).
- Private PKI: when rotating roots, cross-sign the new root with the old one
  for the transition, and give clients the new root early.
- Do not assume non-browser clients fetch missing intermediates; serve the full chain.

## Diagnose

```bash
openssl s_client -connect host:443 -servername host -showcerts </dev/null   # what is served
openssl verify -show_chain -CAfile roots.pem -untrusted served-intermediates.pem leaf.pem
```

## Checked
2026-11-01. Confirmed against the Let's Encrypt DST Root CA X3 expiration page and Scott Helme's write-up (OpenSSL 1.0.x quirk, 1.1.0 or later, Android exception, trusted-first); RFC 5280 section 6 and RFC 4158 for the validation versus path-building split. Removed the per-stack table, AIA and `-no_alt_chains` claims (not confirmed in fetched pages).
Method: documentation only; no commands were run.

## Verify

- [ ] Chain validated with both modern and oldest supported client stacks.
- [ ] Root rotation plan includes cross-signing and trust store updates.
