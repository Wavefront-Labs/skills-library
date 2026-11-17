---
id: computing-software.cryptography-implementation.crypto-libraries.go-crypto-mlkem-and-hkdf-packages
name: go-crypto-mlkem-and-hkdf-packages
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, golang, go-crypto, go-mlkem, ml-kem, go-hkdf, hkdf, post-quantum]
level: advanced
status: verified
description: "Use Go 1.24+ crypto/mlkem and crypto/hkdf: ML-KEM-768 key generation, seed storage, encapsulate/decapsulate order, hybrid with X25519, and hkdf.Key/Extract/Expand."
sources: ["https://pkg.go.dev/crypto/mlkem", "https://pkg.go.dev/crypto/hkdf", "https://csrc.nist.gov/pubs/fips/203/final", "https://www.rfc-editor.org/rfc/rfc5869"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto/mlkem and crypto/hkdf (Go 1.24+)

## ML-KEM (FIPS 203)
```go
dk, err := mlkem.GenerateKey768()                  // decapsulation (private) key
ekBytes := dk.EncapsulationKey().Bytes()           // 1184 bytes, send to the peer
seed := dk.Bytes()                                 // 64-byte seed: the form to store

// sender
ek, err := mlkem.NewEncapsulationKey768(ekBytes)   // validates length and encoding
shared, ct := ek.Encapsulate()                     // note order: shared key, then ciphertext (1088 B)

// receiver
dk2, err := mlkem.NewDecapsulationKey768(seed)
shared2, err := dk2.Decapsulate(ct)                // err only for wrong length (`mlkem: invalid ciphertext length`)
```
- `mlkem.GenerateKey1024` / `*1024` types for Category 5 (encapsulation key 1568 bytes). 768 is the general default.
- Sizes, run on Go 1.27.3: encapsulation key 1184, seed 64, ciphertext 1088, shared key 32 bytes (the constants
  `mlkem.EncapsulationKeySize768`, `SeedSize`, `CiphertextSize768`, `SharedKeySize` exist). Wrong-length encapsulation keys
  and seeds return `invalid encapsulation key length` / `invalid seed length`.
- **Implicit rejection:** decapsulating a tampered ciphertext returns a pseudorandom key, not an
  error (checked: the tampered ciphertext gave a different 32-byte key and a nil error). Authentication comes from what you do with the key (an AEAD that fails, a MAC, a
  handshake transcript), never from `Decapsulate` succeeding.
- Store the 64-byte seed (encrypted, like any private key); expanded keys are derived from it.
- The 32-byte shared secret is uniformly random; still pass it through a KDF with context.

## Hybrid with X25519 (defence in depth)
```go
xPriv, _ := ecdh.X25519().GenerateKey(rand.Reader)
// ...exchange xPub and ML-KEM ek/ct...
xShared, _ := xPriv.ECDH(peerXPub)
ikm := append(append([]byte{}, mlkemShared...), xShared...)
key, _ := hkdf.Key(sha256.New, ikm, nil,
    "app-v1 hybrid mlkem768-x25519|"+string(transcriptHash), 32)
```
Include both public values / ciphertexts (or a transcript hash) in the KDF info so the key binds to
the exchange. For standard protocols use HPKE or TLS's `X25519MLKEM768` instead of rolling your own.

## crypto/hkdf (RFC 5869)
```go
okm, err := hkdf.Key(sha256.New, secret, salt, "myapp v1 file-encryption", 32)   // extract+expand
prk, err := hkdf.Extract(sha256.New, secret, salt)
k1, err  := hkdf.Expand(sha256.New, prk, "myapp v1 enc", 32)
k2, err  := hkdf.Expand(sha256.New, prk, "myapp v1 mac", 32)
```
- `info` is a string: put a protocol name, version and purpose in it so keys for different uses
  differ (domain separation).
- Salt: random or protocol-fixed; `nil` is allowed and gives the same output as a zero-filled salt of hash length
  (checked) when the secret is already uniformly random.
- Output length is capped at 255 * hash size (8160 bytes for SHA-256 works; 8161 returns `hkdf: requested key length too large`, checked). Under `GODEBUG=fips140=only` a key shorter than 112 bits is refused.
- HKDF is not a password KDF; use `crypto/pbkdf2` (1.24+) or `x/crypto/argon2` for passwords.
- The old `golang.org/x/crypto/hkdf` returns an `io.Reader`; the stdlib API is simpler and inside
  the FIPS module.

## Verify
- [ ] Round-trip test: both sides derive identical keys; a modified ciphertext yields a different key
      and the following AEAD open fails.
- [ ] Stored ML-KEM private keys are seeds, encrypted at rest.
- [ ] Every `hkdf` call has a distinct, versioned `info` string.
