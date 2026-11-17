---
id: computing-software.cybersecurity-defensive.application-security.jwt-validation
name: jwt-validation
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [session-management, jwt-validation, jwt, jws, alg-none, jwks, token-validation, audience-validation]
level: advanced
status: docs-checked
description: "Validate JWTs correctly: pin algorithms, verify the signature with the issuer's key, check iss, aud, exp, nbf and typ, and avoid alg none and key-confusion bugs."
sources: ["https://datatracker.ietf.org/doc/html/rfc8725", "https://datatracker.ietf.org/doc/html/rfc7519"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWT validation

**Goal:** a token is accepted only if it is signed by a key you trust, with the algorithm you expect, for your
audience, and still valid.

## Validation checklist (RFC 8725)
1. **Algorithm verification (section 3.1)**: keep a list of supported algorithms and use no others. Make sure the
   token's `alg` (or `enc`) header specifies the same algorithm the key is for, and use each key with exactly one
   algorithm. This blocks the two attacks of section 2.1: an attacker changing `alg` to `none` so a library skips
   the signature check, and changing `RS256` to `HS256` so a library validates the signature with the RSA public key
   as the HMAC secret (key confusion, CVE-2015-9235).
2. **`none` algorithm (section 3.2)**: libraries should not consume JWTs using `none` unless the token is
   protected by other means.
3. **Validate all cryptographic operations (3.3)** using keys and algorithms supplied by the application.
4. **Keys and entropy (3.5)**: human-memorizable passwords must not be used directly as the key for a keyed MAC
   such as `HS256`.
5. **Issuer and subject (3.8)**: when a JWT has `iss`, check that the keys used belong to that issuer. Where issuers
   are `https` URLs, a JWK Set can be retrieved from a URL in the issuer's metadata (other bindings are allowed).
   Reject the token if the issuer or subject is invalid.
6. **Audience (3.9)**: if the same issuer issues JWTs for more than one recipient, the JWT must carry `aud`, and the
   application must reject tokens whose audience is missing or not associated with it.
7. **Do not trust received claims (3.10)**: `kid` is used for key lookup, so validate or sanitize it against SQL and
   LDAP injection. Blindly following `jku` or `x5u` URLs can cause SSRF: match them against an allowlist of
   locations and send no cookies.
8. **Explicit typing (3.11) and separate rules per kind of token (3.12)**: use the `typ` header, different `aud`
   values, or different issuers for different kinds of JWT, so a token for one purpose is rejected in another.
9. **Time claims (RFC 7519 4.1.4 and 4.1.5)**: a JWT must not be accepted on or after `exp` or before `nbf`.
   Implementers may allow small leeway for clock skew, usually no more than a few minutes. These claims are
   optional, so decide whether your application requires them.

## Gotchas
- Signature verification disabled during debugging and left in place.
- JWTs cannot be revoked before `exp` without server state.
- The OWASP Session Management Cheat Sheet says not to keep JWTs in `localStorage` or `sessionStorage`, because
  any script in the origin can read them; use `HttpOnly; Secure; SameSite=Strict` cookies or a backend-for-frontend
  pattern.

## Verify
Hand-crafted tokens with `alg: none`, an HS256 signature made with the public key, a wrong `aud`, an expired `exp`
and an unknown `kid` are all rejected.

## Checked
Method: docs-checked 2026-11-09 against RFC 8725 (sections 2.1, 3.1 to 3.12 read) and RFC 7519 (sections 4.1.4 and
4.1.5). The OWASP Session Management Cheat Sheet was read for the storage advice. Removed unconfirmed claims:
library call examples (jose, PyJWT, Spring, .NET), the 60 second skew and 5-15 minute token lifetime, `at+jwt` and
RFC 9068, and the jwt_tool test suggestion. The OWASP JWT Java cheat sheet was not fetched and is no longer cited.
