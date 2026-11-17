---
id: computing-software.cybersecurity-defensive.identity-protocols.jws-serialization-signing
name: jws-serialization-signing
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [jws-serialization-signing, jose-jws-jwt, jws, rfc7515, compact-serialization, es256, ps256, eddsa, detached-payload, identity-protocols]
level: advanced
status: docs-checked
description: "Produce and verify compact JWS: base64url header.payload.signature, signing input, detached payloads with b64 false, and algorithm choices RS256, PS256, ES256, EdDSA."
sources:
  - https://www.rfc-editor.org/rfc/rfc7515
  - https://www.rfc-editor.org/rfc/rfc7518
  - https://www.rfc-editor.org/rfc/rfc7797
  - https://www.rfc-editor.org/rfc/rfc8725
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWS compact serialisation and signing

Goal: understand what is being signed.

Method: the signing input is the base64url-encoded header, a dot, then the base64url-encoded payload; the signature is computed over that input and base64url-encoded as the third part (RFC 7515 Section 5). base64url omits trailing `=` padding (RFC 7515 Section 2). RFC 7518 lists `RS256` (RSASSA-PKCS1-v1_5), `PS256` (RSASSA-PSS), `ES256` (ECDSA P-256 and SHA-256) and `HS256`; for HS256 a key at least as large as the hash output (256 bits) MUST be used. An ES256 signature is a 64-octet sequence (R and S concatenated), not a DER structure. JSON serialisation (RFC 7515 Section 7.2) allows multiple signatures. RFC 7797 defines the `b64` header parameter (`"b64":false` with `crit`) for unencoded, possibly detached payloads.

Gotchas:
- ES256 signatures that a library emits in another encoding must be converted to the 64-octet form before use as a JWS signature.
- RFC 8725: libraries must let the caller specify the allowed algorithms and must not use `alg` from the token to pick any other.

Verify: verify the sample JWS from RFC 7515 Appendix A with your library.

## Checked

Date: 2026-11-02. Confirmed in RFC 7515, RFC 7518 (algorithm names, 64-octet ES256, HS256 key size), RFC 7797 (`b64`) and RFC 8725 (algorithm verification). Removed as not stated there: EdDSA, "PS256 preferred over RS256", "32 random bytes", whitespace-insensitivity note, constant-time comparison advice.

Method: documentation only; no commands were run.
