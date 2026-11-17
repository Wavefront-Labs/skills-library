---
id: computing-software.software-engineering.api-design.jwt-validation-for-apis
name: jwt-validation-for-apis
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-security, jwt-validation, jwks, oauth2, rfc-8725, bearer-tokens]
level: advanced
status: verified
description: "Validate JWT bearer tokens correctly in APIs: pinned algorithms, JWKS key rotation, iss/aud/exp/nbf checks, clock skew, and the classic alg=none and key-confusion pitfalls."
sources: ["https://www.rfc-editor.org/rfc/rfc8725", "https://www.rfc-editor.org/rfc/rfc7519", "https://www.rfc-editor.org/rfc/rfc9068", "https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWT validation for APIs

## Checklist (RFC 8725 best practices, RFC 9068 for OAuth access tokens)
1. **Algorithm allow-list** configured server-side (`RS256`/`ES256`/`EdDSA`). Never take `alg` from
   the token as truth. Rejects `alg: none` and the RS256->HS256 key-confusion attack (attacker signs
   with the public key as an HMAC secret).
2. **Signature** verified with a key from the issuer's JWKS (`/.well-known/openid-configuration` ->
   `jwks_uri`), selected by `kid`. Cache JWKS, refresh on unknown `kid` (rate-limited) to follow
   rotation. Never fetch keys from a URL inside the token (`jku`, `x5u`) unless allow-listed.
3. **`iss`** equals the expected issuer exactly.
4. **`aud`** contains *this* API's identifier. Skipping it lets a token minted for another service
   (same IdP) call yours.
5. **`exp`** in the future, **`nbf`/`iat`** not in the future, with small leeway (<= 60 s).
6. **`typ`** header `at+jwt` (or `application/at+jwt`) for access tokens: RFC 9068 says the resource server MUST verify it and reject other values, so ID tokens can't be replayed as access tokens. PyJWT 2.15 does not check `typ` for you (a token with `typ: at+jwt` and one without were both accepted), so read `jwt.get_unverified_header(t)["typ"]` yourself; jose has a `typ` option and .NET has `TokenValidationParameters.ValidTypes` (if unset, all types are accepted).
7. Then authorization: `scope`/`scp`, roles, tenant claims, and per-object checks.

## Library usage
```python
claims = jwt.decode(token, key=signing_key, algorithms=["RS256"],
                    audience="https://api.example.com", issuer="https://idp.example.com/",
                    options={"require": ["exp", "iss", "aud"]})        # PyJWT + PyJWKClient for keys
```
Node: `jose` `jwtVerify(token, createRemoteJWKSet(url), {issuer, audience, algorithms:['RS256']})` (run against a local JWKS endpoint: valid token accepted, wrong `aud` rejected with `ERR_JWT_CLAIM_VALIDATION_FAILED`).
.NET: `TokenValidationParameters` (`ValidIssuer`, `ValidAudience`, `ValidAlgorithms`).
Never "decode" without verify (`jwt.decode(..., options={"verify_signature": False})`, `jsonwebtoken.decode`) for anything
security-relevant.

The PyJWT call was run with a generated RSA key: valid accepted; expired, wrong `aud`, wrong `iss`, `alg: none`, a hand-built HS256 token keyed with the public PEM, a tampered signature, a missing `exp`, a future `nbf` and a future `iat` were all rejected, and `leeway=60` accepted a token expired 30 s ago. PyJWT also refuses to *sign* HS256 with a PEM public key. PyJWT 2.x requires `algorithms=` on `decode` and rejects `verify=False`; skipping verification is `options={"verify_signature": False}`.

## Operational points
- JWTs can't be revoked before `exp`; keep access tokens short (5-15 min) and use introspection
  (RFC 7662) for high-risk operations if you need instant revocation.
- Don't put PII or secrets in claims: JWS payloads are only base64url, readable by anyone.
- Log token `jti`/`sub`, never the token.
- Tokens in `Authorization: Bearer` header only, not query strings (they land in logs).

## Verify
Negative tests: expired, wrong `aud`, wrong `iss`, `alg: none`, HS256-signed with the public key,
unknown `kid`, tampered payload: all must return 401.
