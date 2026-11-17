---
id: computing-software.cryptography-implementation.protocol-implementation.jwt-library-configuration-pitfalls
name: jwt-library-configuration-pitfalls
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, pyjwt, jwt-library-config, jsonwebtoken, nimbus-jose, jjwt, jose]
level: practitioner
status: docs-checked
description: "Configure JWT libraries safely: PyJWT algorithms list, jose and Nimbus verification, audience and issuer checks, leeway and key-type binding."
sources: ["https://pyjwt.readthedocs.io/en/stable/usage.html", "https://github.com/panva/jose", "https://connect2id.com/products/nimbus-jose-jwt/examples/validating-jwt-access-tokens"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWT library configuration pitfalls

## Python PyJWT
```python
claims = jwt.decode(token, public_key, algorithms=["ES256"], audience="api://orders",
                    issuer="https://idp.example.com", leeway=30,
                    options={"require": ["exp", "iat", "sub"]})
```
- Always pass `algorithms` explicitly; never mix HS and RS/ES algorithms with the same key object.
- `options={"verify_signature": False}` skips signature and registered-claim validation: debugging only.
- Use `PyJWKClient(jwks_url).get_signing_key_from_jwt(token)` for JWKS; it looks keys up by `kid`, caches, and
  refreshes the key set when the `kid` is unknown.

## Node
- `jose` (panva): `jwtVerify` validates the signature and the claims set.

## Java
- Nimbus: `DefaultJWTProcessor` with `JWSVerificationKeySelector(JWSAlgorithm.RS256, jwkSource)` and
  `DefaultJWTClaimsVerifier` configured with the required claims.

## Checklist for any library
- [ ] Algorithm allow list tied to the key type; `none` rejected.
- [ ] `iss`, `aud`, `exp` validated; `nbf` honored; leeway no more than a few minutes (RFC 7519 wording).
- [ ] Token size limits before parsing; errors return 401 without details.

## Checked

2026-11-01. Confirmed against the PyJWT usage page (`algorithms`, `audience`, `issuer`, `leeway`, `require`,
`verify_signature`, `PyJWKClient` caching and refresh, `get_signing_key_from_jwt`), the panva/jose README (`jwtVerify`) and the
Nimbus JOSE+JWT access-token validation example (`DefaultJWTProcessor`, `JWSVerificationKeySelector`,
`DefaultJWTClaimsVerifier`). Removed: jsonwebtoken and jjwt specifics, `createRemoteJWKSet`, the "mandatory in 2.x" claim,
and the `jku`/`x5u` item (not in these sources).
Method: documentation only; no commands were run.
