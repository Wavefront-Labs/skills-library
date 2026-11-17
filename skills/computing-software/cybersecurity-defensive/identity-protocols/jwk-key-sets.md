---
id: computing-software.cybersecurity-defensive.identity-protocols.jwk-key-sets
name: jwk-key-sets
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [jwk-key-sets, jose-jwe-jwk, jwk, jwks, rfc7517, kid, thumbprint, rfc7638, x5c, identity-protocols]
level: practitioner
status: docs-checked
description: "Represent keys as JWK and JWKS: kty, use, key_ops, alg, kid, x5c, thumbprints (RFC 7638), and how to publish rotation-safe key sets."
sources:
  - https://www.rfc-editor.org/rfc/rfc7517
  - https://www.rfc-editor.org/rfc/rfc7518
  - https://www.rfc-editor.org/rfc/rfc7638
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWK and JWKS key representation

Goal: publish and consume keys consistently.

Fields (RFC 7517): `kty`, `use` (`sig` or `enc`), `key_ops`, `alg`, `kid`, and optional `x5c` (certificate chain) and `x5t#S256` (SHA-256 certificate thumbprint). RFC 7518 defines the key-type specific members: RSA `n` and `e` (private `d`, `p`, `q`), EC `crv`, `x`, `y`, and `oct` with `k` for symmetric keys. P-256 is an ECDSA curve in RFC 7518; `OKP` keys and Ed25519 are defined in RFC 8037, not in these documents.
Thumbprint (RFC 7638): hash (for example SHA-256) of the JSON containing only the required members, in lexicographic order; the RFC says such a thumbprint might be used as a `kid`.

Gotchas:
- `kid` is used to choose among the keys of a JWK Set during key rollover; different keys in one set SHOULD use distinct `kid` values (RFC 7517).
- Do not publish private members (`d`, `p`, `q`) or an `oct` key's `k` in a public JWK Set; that follows from their being private or secret key material.

Verify: compute a thumbprint for the RFC 7638 example key and compare.

## Checked

Date: 2026-11-02. Confirmed in RFC 7517, RFC 7518 and RFC 7638 (field names, `oct`/`k`, thumbprint rule and kid use). Removed as not stated there: Ed25519/OKP details, DPoP `jkt`, CI linting and `Cache-Control` advice.

Method: documentation only; no commands were run.
