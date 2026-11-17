---
id: computing-software.software-engineering.go.password-hashing-with-argon2id-and-bcrypt
name: password-hashing-with-argon2id-and-bcrypt
category: computing-software
field: software-engineering
product: go
tags: [go, go-security, go-password-hashing, argon2id, bcrypt, password-hashing, scrypt]
level: practitioner
status: docs-checked
description: "Hash passwords in Go with argon2id or bcrypt, tune cost parameters, encode salts and parameters, and plan rehashing on login."
sources:
  - https://pkg.go.dev/golang.org/x/crypto/argon2
  - https://pkg.go.dev/golang.org/x/crypto/bcrypt
  - https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Password hashing: argon2id and bcrypt

**Goal:** store passwords so that a database leak does not yield them quickly.

```go
// argon2id: OWASP lists m=19456 KiB (19 MiB), t=2, p=1 as one of its minimum configurations.
// The x/crypto docs give RFC 9106's second option (t=3, 64 MiB, 4 threads) when much less than 2 GiB is available.
salt := make([]byte, 16); rand.Read(salt)
key := argon2.IDKey([]byte(pw), salt, 3, 64*1024, 4, 32)
enc := fmt.Sprintf("$argon2id$v=19$m=65536,t=3,p=4$%s$%s",
    base64.RawStdEncoding.EncodeToString(salt), base64.RawStdEncoding.EncodeToString(key))

// bcrypt (OWASP: work factor as high as the server allows, minimum 10; 72-byte input limit)
h, _ := bcrypt.GenerateFromPassword([]byte(pw), 12)
err := bcrypt.CompareHashAndPassword(h, []byte(pw))
```

Store the algorithm and parameters with the hash (OWASP suggests the modular PHC string format) so you can raise cost later: on a successful login, if the stored parameters are below current policy, re-hash and update the row.
OWASP: tune the work factor by experiment on your own servers; as a general rule a hash should take less than one second; a work factor that is too high lets login floods exhaust CPU. Argon2 memory cost `m` is in KiB per hash, so bound concurrent logins.
`bcrypt.Cost(hash)` returns the cost used for an existing hash, which lets you find hashes that need upgrading.

## Gotchas
- bcrypt has a 72-byte input limit; `GenerateFromPassword` returns `ErrPasswordTooLong` above it. OWASP says to enforce a maximum password length of 72 bytes.
- bcrypt costs: `MinCost` 4, `MaxCost` 31, `DefaultCost` 10 (a cost below `MinCost` is replaced by `DefaultCost`).
- If you pre-hash for bcrypt, OWASP warns about NUL bytes in raw digests (encode with base64) and password shucking; its recommended form is bcrypt(base64(hmac-sha384(password, pepper))) with the pepper stored outside the database.
- OWASP prefers Argon2id; bcrypt only for legacy systems where Argon2 and scrypt are unavailable.
- A pepper is secret, shared between passwords and stored separately; changing it forces affected users to reset passwords.
- Use a good random salt (the x/crypto docs say so); fast algorithms such as MD5 and SHA-1 are not suitable for password storage.

## Checked
2026-11-09. Confirmed on pkg.go.dev/golang.org/x/crypto/argon2 (`IDKey`, RFC 9106 recommended options, memory in KiB, salt), pkg.go.dev/golang.org/x/crypto/bcrypt (cost constants, `ErrPasswordTooLong`, `Cost`) and the OWASP Password Storage Cheat Sheet (Argon2id minimum configurations, bcrypt minimum 10 and legacy status, 72-byte limit, pre-hashing, PHC format, work factor under one second, pepper, upgrade on login).
Removed: the 100 to 500 ms target, the claim that bcrypt "silently truncates" in older x/crypto versions, the NUL-byte/SHA-256 shortcut, the constant-time compare line and the "never write your own KDF" rule.
Method: documentation only; no commands were run.

## Verify
Unit-test the round trip, wrong password and rehash path; benchmark `GenerateFromPassword` and `IDKey` on the deployment CPU.
