---
id: computing-software.web-development.vapor.vapor-password-hashing-crypto
name: vapor-password-hashing-crypto
category: computing-software
field: web-development
product: vapor
tags: [vapor, password-hasher, bcrypt, otp, hotp, totp, swiftcrypto, passwords]
level: practitioner
status: docs-checked
description: "Hash and verify passwords with app.passwords and req.password (bcrypt, async); SwiftCrypto, Bcrypt and HOTP/TOTP in Vapor."
sources:
  - https://docs.vapor.codes/security/passwords/
  - https://docs.vapor.codes/security/crypto/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: store and verify passwords with Vapor's hasher API, and use its crypto and one-time-password helpers.

## Choose the hasher
Configure on the application (usually at boot):

```swift
app.passwords.use(.bcrypt)            // default
app.passwords.use(.bcrypt(cost: 8))   // default cost is 12
```

A `.plaintext` hasher exists for tests only (insecure, never production):

```swift
switch app.environment {
case .testing:
    app.passwords.use(.plaintext)
default: break
}
```

## Hash and verify
```swift
let digest = try req.password.hash("vapor")
let bool = try req.password.verify("vapor", created: digest)
let boot = try app.password.hash("vapor")   // same API on Application, for boot time
```

## Async (do not block the event loop)
Hashing is deliberately slow and CPU heavy. `async` dispatches it to a background thread pool, freeing event loops for other requests.

```swift
let digest = try await req.password.async.hash("vapor")
let result = try await req.password.async.verify("vapor", created: digest)
// future style: req.password.async.hash("vapor").map { digest in ... }
```

## Bcrypt directly
`Bcrypt` uses a random salt, so the same password hashes differently each time and digests cannot be compared directly. Verify plaintext and digest together:

```swift
let digest = try Bcrypt.hash("test")
let pass = try Bcrypt.verify("test", created: digest)
```

Login flow: fetch the user's stored digest by email or username, then verify the supplied plaintext against it.

## SwiftCrypto
Importing Vapor exposes SwiftCrypto (a Linux-compatible port of CryptoKit), e.g. `SHA256.hash(data: Data("hello".utf8))`. It covers SHA512/384/256, HMAC, AES, ChaChaPoly, Curve25519, P521/P384/P256, and insecure SHA1 and MD5.

## One-time passwords
HOTP and TOTP work with SHA-1, SHA-256 and SHA-512 and give 6, 7 or 8 digits. The symmetric key must stay private.

```swift
let key = SymmetricKey(size: .bits128)
let hotp = HOTP(key: key, digest: .sha256, digits: .six)
let code = hotp.generate(counter: 25)

let totp = TOTP(key: key, digest: .sha256, digits: .six, interval: 60)
let tcode = totp.generate(time: Date())
```

Static forms exist: `HOTP.generate(key:digest:digits:counter:)` and `TOTP.generate(key:digest:digits:interval:time:)`. HOTP uses an agreed counter that increases after each generation; TOTP uses current time, with a code valid over an interval (commonly 30 seconds).

Validation window: `hotp.generate(counter: 25, range: 2)` returns codes for counters 23...27. A larger margin gives an attacker more time and freedom, lowering security.

## Checked
Read the whole Passwords and Crypto pages (vapor/docs, docs/4.0/security/passwords.md and crypto.md, sources of the cited pages) on 2026-11-08. Confirmed bcrypt default and cost 12, `.plaintext` for tests, hash/verify on request and application, the async API, Bcrypt salt behaviour and login flow, the SwiftCrypto algorithm list, SHA-1/256/512 and 6 to 8 digit OTPs, the HOTP and TOTP examples, and the range example (counters 23...27) with its security warning. No claims removed.
Method: docs-only read of cited pages, 2026-11-08
