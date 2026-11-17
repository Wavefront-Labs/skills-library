---
id: computing-software.web-development.vapor.vapor-jwt-sign-verify
name: vapor-jwt-sign-verify
category: computing-software
field: web-development
product: vapor
tags: [vapor, vapor-jwt, jwtkit, jwt, jwtpayload, jwk, signing, claims]
level: advanced
status: docs-checked
description: "Sign and verify JWTs in Vapor: add the JWT package, key collection (HMAC, ECDSA, EdDSA, RSA, PSS), kid, claims, JWK, vendor tokens and a JWT authenticator."
sources:
  - https://docs.vapor.codes/security/jwt/
  - https://docs.vapor.codes/security/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: issue and check JSON Web Tokens with Vapor's `JWT` module (built on JWTKit/SwiftCrypto).

## Setup
Package.swift: `.package(url: "https://github.com/vapor/jwt.git", from: "5.0.0")` and target dependency `.product(name: "JWT", package: "jwt")`. Then in configure.swift (`import JWT`):
```swift
await app.jwt.keys.add(hmac: "secret", digestAlgorithm: .sha256)  // HS256
```
Replace `"secret"` with a real secret kept in config or environment. `app.jwt.keys` is a `JWTKeyCollection` actor.

## Payload, sign, verify
```swift
struct TestPayload: JWTPayload {
    enum CodingKeys: String, CodingKey {
        case subject = "sub", expiration = "exp", isAdmin = "admin"
    }
    var subject: SubjectClaim
    var expiration: ExpirationClaim
    var isAdmin: Bool
    func verify(using algorithm: some JWTAlgorithm) async throws {
        try self.expiration.verifyNotExpired()
    }
}
let token = try await req.jwt.sign(payload)
let payload = try await req.jwt.verify(as: TestPayload.self)
```
`req.jwt.verify` reads the bearer token from the `Authorization` header; a failure throws 401 Unauthorized.

## Algorithms (all via `app.jwt.keys.add`)
- HMAC HS256/384/512: `add(hmac:digestAlgorithm:)`.
- ECDSA ES256/384/512: `try ES256PublicKey(pem:)` or `ES256PrivateKey()` then `add(ecdsa: key)`.
- EdDSA (Ed25519 only): `EdDSA.PublicKey(x:curve: .ed25519)`, `EdDSA.PrivateKey(d:curve:)` or `EdDSA.PrivateKey(curve: .ed25519)`, then `add(eddsa: key)`.
- RSA RS256/384/512: keys live under `Insecure.RSA` (compatibility only; prefer ECDSA/EdDSA); no keys under 2048 bits. `add(rsa: key, digestAlgorithm: .sha256)`.
- RSA-PSS (recommended over PKCS1v1.5): same keys, `add(pss: key, digestAlgorithm: .sha256)`.

## kid
`add(hmac: "foo", digestAlgorithm: .sha256, kid: "a")`. A key without `kid` is the default and is overridden by the next kid-less key. Sign with `req.jwt.sign(payload, kid: "a")`; verification takes the kid from the header, and `iteratingKeys` lets verify try all keys if it is not found.

## Claims
`aud` AudienceClaim `verifyIntendedAudience(includes:)`; `exp` ExpirationClaim `verifyNotExpired(currentDate:)`; `nbf` NotBeforeClaim `verifyNotBefore(currentDate:)`; also `jti` IDClaim, `iat` IssuedAtClaim, `iss` IssuerClaim, `locale` LocaleClaim, `sub` SubjectClaim (no verify helper). Verify every claim in `verify`; otherwise check `value`.

## JWK
```swift
let jwk = try JWK(json: privateKey)
try await app.jwt.keys.use(jwk: jwk)
try await app.jwt.keys.use(jwksJSON: json) // {"keys": [...]}
```

## Vendors
Apple: set `app.jwt.apple.applicationIdentifier`, then `try await req.jwt.apple.verify()` (AppleIdentityToken). Google: set `app.jwt.google.applicationIdentifier` and `gSuiteDomainName`, then `req.jwt.google.verify()`. Microsoft: `app.jwt.microsoft.applicationIdentifier`, then `req.jwt.microsoft.verify()`.

## Authenticator
Make the payload `Content, Authenticatable, JWTPayload`, then `app.grouped(SessionToken.authenticator(), SessionToken.guardMiddleware())` and `try req.auth.require(SessionToken.self)` in the handler. The docs' example builds the expiry as `ExpirationClaim(value: Date().addingTimeInterval(expirationTime))` with `expirationTime` set to `60 * 15` (15 minutes).

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) security/jwt, security/authentication, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
