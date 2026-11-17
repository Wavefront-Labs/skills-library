---
id: computing-software.cybersecurity-defensive.identity-protocols.jwe-encrypted-tokens
name: jwe-encrypted-tokens
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [jwe-encrypted-tokens, jose-jwe-jwk, jwe, rfc7516, rsa-oaep, ecdh-es, a256gcm, nested-jwt, identity-protocols]
level: advanced
status: docs-checked
description: "Encrypt tokens with compact JWE: five parts, alg for key management (RSA-OAEP, ECDH-ES, dir), enc (A256GCM), and nested sign-then-encrypt."
sources:
  - https://www.rfc-editor.org/rfc/rfc7516
  - https://www.rfc-editor.org/rfc/rfc7518
  - https://www.rfc-editor.org/rfc/rfc7519
  - https://www.rfc-editor.org/rfc/rfc8725
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWE structure and algorithm choices

Goal: keep token contents confidential from carriers.

Structure: the JWE compact serialisation has five base64url parts: protected header, encrypted key, initialization vector, ciphertext and authentication tag (RFC 7516 Section 7.1). The header has `alg` (key management; RFC 7518 lists `RSA-OAEP-256`, `ECDH-ES+A256KW`, `dir`, `A256KW`) and `enc` (content encryption; RFC 7518 lists `A256GCM`, `A128GCM`, `A256CBC-HS512`).

Nested JWT: sign first, then encrypt, setting `cty` to `JWT` in the outer header (RFC 7519 Section 11.2 and its nesting steps); the recipient decrypts, then validates the inner signature.

Gotchas:
- RFC 8725: avoid all RSA-PKCS1 v1.5 encryption algorithms (that includes `RSA1_5`); prefer RSAES-OAEP.
- RFC 8725: ECDH-ES implementations that do not validate the peer's public key against the curve are open to invalid-curve attacks; use libraries that validate.
- RFC 8725: do not compress data before encryption (`SHOULD NOT`), because compression leaks information about the plaintext.

Verify: round-trip a sample JWE from RFC 7516 Appendix A with your library.

## Checked

Date: 2026-11-02. Confirmed in RFC 7516 (compact serialisation parts), RFC 7518 (algorithm names), RFC 7519 (nested JWT and `cty` value `JWT`) and RFC 8725 (RSA PKCS1 v1.5, invalid-curve, compression). Removed as not stated there: "header authenticated as additional data" wording, decompression-bomb size limit, "encryption does not replace signature and audience checks", uniform-error verification.

Method: documentation only; no commands were run.
