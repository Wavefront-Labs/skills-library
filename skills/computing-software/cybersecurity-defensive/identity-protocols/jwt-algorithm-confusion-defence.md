---
id: computing-software.cybersecurity-defensive.identity-protocols.jwt-algorithm-confusion-defence
name: jwt-algorithm-confusion-defence
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [jwt-algorithm-confusion-defence, jose-jws-jwt, alg-none, algorithm-confusion, hs256, rs256, jku, kid, rfc8725, identity-protocols]
level: advanced
status: docs-checked
description: "Block JWT alg=none and RS256 to HS256 key confusion by pinning allowed algorithms per key and never selecting verification keys from untrusted header fields."
sources:
  - https://www.rfc-editor.org/rfc/rfc7515
  - https://www.rfc-editor.org/rfc/rfc7519
  - https://www.rfc-editor.org/rfc/rfc8725
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWT algorithm confusion and none

Goal: remove the classic JWT verifier bugs.

Method (RFC 8725):
- Use a library that lets the caller specify the supported set of algorithms, and configure an explicit allow-list per issuer/key; the library must ensure the `alg` header names the algorithm actually used and must not use any other (Section 3.1). Each key must be used with exactly one algorithm.
- The attack that sets `alg` to `none` is why a library must not trust a token's `alg` to skip signature validation; use `none` only where the JWT is protected end to end some other way, such as TLS.
- Do not blindly follow `jku` or `x5u` headers: match the URL against an allow-list (SSRF risk). Fetch keys from the configured source.
- Treat `kid` as a lookup key: validate or sanitise it so it cannot cause SQL or LDAP injection.
- Use maintained libraries; RFC 8725 lists the pitfalls.

Gotchas:
- A header listed in `crit` (RFC 7515 Section 4.1.11) must be understood and processed, or the JWS is invalid.
- Validate that the keys belong to the `iss` (RFC 8725 Section 3.8).

Verify: send a token with `alg` none and one HS256-signed using the RSA public key as the secret; both must fail.

## Checked

Date: 2026-11-02. Confirmed in RFC 8725 (Sections 2 and 3: algorithm verification, none, jku/x5u, kid, issuer validation) and RFC 7515 (`crit`). Removed as not stated there: the `["RS256"]` example, "multiple algs let an attacker choose the weakest", the typed-key-object advice, "ignore jwk and x5c headers" wording.

Method: documentation only; no commands were run.
