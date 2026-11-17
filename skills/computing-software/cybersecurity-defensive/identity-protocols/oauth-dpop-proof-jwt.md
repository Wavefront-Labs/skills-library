---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-dpop-proof-jwt
name: oauth-dpop-proof-jwt
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-dpop-proof-jwt, oauth-dpop, dpop, rfc9449, proof-jwt, dpop+jwt, htm, htu, jkt, identity-protocols]
level: advanced
status: docs-checked
description: "Build DPoP proofs: typ dpop+jwt, jwk header, jti, htm, htu, iat and ath claims, signed per request with the client key pair."
sources:
  - https://www.rfc-editor.org/rfc/rfc9449
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DPoP proof JWT construction

Goal: prove possession of a key with each request.

Method: generate a key pair for a registered asymmetric JWS algorithm (not `none` or a MAC algorithm). For each HTTP request create a JWT: header `typ: dpop+jwt`, `alg`, `jwk` (public key); payload `jti` (unique), `htm` (HTTP method), `htu` (URL without query and fragment), `iat`, and at resource requests `ath` (base64url SHA-256 of the access token); optional `nonce`. Send in the `DPoP:` header; at the token endpoint it binds the token to the key thumbprint (`jkt` in `cnf`). At the RS use `Authorization: DPoP <token>`.

Gotchas:
- Exactly one DPoP header; reject several.
- Verifier must check `typ`, `alg`, the signature with the embedded `jwk`, `htm` and `htu` match, an acceptable `iat` window, `nonce` if one was issued, and for resource requests `ath` and that the access token is bound to the proof's key; `jti` uniqueness is a replay defence where feasible.
- Compare `htu` ignoring query and fragment, after syntax- and scheme-based normalization (RFC 3986).

Verify: reuse a proof for a different URL and expect rejection.

## Checked

2026-11-02. Confirmed against RFC 9449 sections 4.1 to 4.3 and 7.1 (header and claim names, `typ` value, `ath` hash, `nonce`, validation checklist, single DPoP header, `Authorization: DPoP`) and section 6 (`cnf` `jkt`). Removed: the ES256/EdDSA recommendation, the seconds-level `iat` figure and the non-extractable key advice (not in the RFC).
Method: documentation only; no commands were run.
